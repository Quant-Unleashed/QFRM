import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator


class LocalVolModel:
    def __init__(self, S0, r, T, steps):
        """
        Initialize Local Volatility Model parameters
        S0: Initial stock price
        r: Risk-free rate
        T: Time to maturity
        steps: Number of time steps
        """
        self.S0 = S0
        self.r = r
        self.T = T
        self.steps = steps
        self.dt = T / steps

    def local_vol_surface(self, S, t, strikes, maturities, implied_vols):
        """
        Construct local volatility surface using Dupire's formula
        S: Current stock price
        t: Current time
        strikes: Array of strike prices
        maturities: Array of maturities
        implied_vols: 2D array of implied volatilities
        Returns: Interpolated local volatility function
        """
        # Create grid for interpolation
        local_vols = np.zeros_like(implied_vols)

        for i, T in enumerate(maturities):
            for j, K in enumerate(strikes):
                # Simplified Dupire formula approximation
                sigma = implied_vols[i, j]
                # Numerical derivatives (simplified for demonstration)
                d1 = (np.log(S / K) + (self.r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
                d2 = d1 - sigma * np.sqrt(T)

                # Local volatility approximation
                local_vols[i, j] = sigma * (1 + 0.1 * d1 * d2)  # Simplified adjustment

        # Interpolate local volatility surface using RegularGridInterpolator
        interp_func = RegularGridInterpolator((maturities, strikes), local_vols,
                                              method='cubic', bounds_error=False, fill_value=None)

        def local_vol(S, t):
            if t >= max(maturities):
                t = max(maturities) - 0.01
            if S <= min(strikes) or S >= max(strikes):
                S = np.clip(S, min(strikes), max(strikes))
            return interp_func([t, S])[0]

        return local_vol

    def simulate_paths(self, n_paths, strikes, maturities, implied_vols, seed=None):
        """
        Simulate asset price paths using local volatility
        Returns: Price paths
        """
        if seed is not None:
            np.random.seed(seed)

        S = np.zeros((self.steps + 1, n_paths))
        S[0] = self.S0

        # Get local volatility function
        local_vol = self.local_vol_surface(self.S0, 0, strikes, maturities, implied_vols)

        for t in range(1, self.steps + 1):
            current_time = t * self.dt
            # Get local volatility for each path
            sigmas = np.array([local_vol(S[t - 1, i], current_time) for i in range(n_paths)])
            # Ensure positive volatility
            sigmas = np.maximum(sigmas, 1e-6)
            # Simulate next step
            dW = np.random.normal(0, np.sqrt(self.dt), n_paths)
            S[t] = S[t - 1] * np.exp((self.r - 0.5 * sigmas ** 2) * self.dt + sigmas * dW)

        return S

    def price_european_call(self, K, n_paths, strikes, maturities, implied_vols, seed=None):
        """
        Price European call option using Monte Carlo simulation
        K: Strike price
        n_paths: Number of simulation paths
        Returns: tuple of (option price, standard error)
        """
        S = self.simulate_paths(n_paths, strikes, maturities, implied_vols, seed)
        payoff = np.maximum(S[-1] - K, 0)
        price = np.exp(-self.r * self.T) * np.mean(payoff)
        std_err = np.std(payoff) / np.sqrt(n_paths)
        return price, std_err


def plot_simulation(S, title="Local Volatility Model Simulation"):
    """
    Plot sample price paths
    """
    plt.figure(figsize=(8, 6))
    plt.plot(S[:, :5])  # Plot first 5 paths
    plt.title(title)
    plt.xlabel("Time Step")
    plt.ylabel("Stock Price")
    plt.grid(True)
    plt.show()


# Example usage
if __name__ == "__main__":
    # Model parameters
    S0 = 100.0  # Initial stock price
    r = 0.05  # Risk-free rate
    T = 1.0  # Time to maturity
    steps = 252  # Number of time steps (daily)

    # Market data for implied volatility surface
    strikes = np.linspace(80, 120, 10)
    maturities = np.linspace(0.1, 1.0, 5)
    implied_vols = np.ones((len(maturities), len(strikes))) * 0.2  # Flat 20% vol for simplicity

    # Initialize model
    model = LocalVolModel(S0, r, T, steps)

    # Simulate paths
    n_paths = 1000
    S = model.simulate_paths(n_paths, strikes, maturities, implied_vols, seed=42)

    # Price a European call option
    K = 100.0
    price, std_err = model.price_european_call(K, n_paths, strikes, maturities, implied_vols)
    print(f"European Call Option Price: {price:.4f}")
    print(f"Standard Error: {std_err:.4f}")

    # Plot sample paths
    plot_simulation(S)