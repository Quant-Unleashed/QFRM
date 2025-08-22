import numpy as np
import matplotlib.pyplot as plt


class HestonModel:
    def __init__(self, S0, v0, r, kappa, theta, sigma, rho, T, steps):
        """
        Initialize Heston Model parameters
        S0: Initial stock price
        v0: Initial volatility
        r: Risk-free rate
        kappa: Mean reversion speed
        theta: Long-term mean variance
        sigma: Volatility of volatility
        rho: Correlation between asset and volatility
        T: Time to maturity
        steps: Number of time steps
        """
        self.S0 = S0
        self.v0 = v0
        self.r = r
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho
        self.T = T
        self.steps = steps
        self.dt = T / steps

    def simulate_paths(self, n_paths, seed=None):
        """
        Simulate asset price and volatility paths using Euler discretization
        Returns: tuple of (price paths, volatility paths)
        """
        if seed is not None:
            np.random.seed(seed)

        # Initialize arrays
        S = np.zeros((self.steps + 1, n_paths))
        v = np.zeros((self.steps + 1, n_paths))
        S[0] = self.S0
        v[0] = self.v0

        # Generate correlated Brownian motions
        z1 = np.random.normal(0, 1, (self.steps, n_paths))
        z2 = np.random.normal(0, 1, (self.steps, n_paths))
        w2 = self.rho * z1 + np.sqrt(1 - self.rho ** 2) * z2

        for t in range(1, self.steps + 1):
            # Ensure variance stays positive
            v[t - 1] = np.maximum(v[t - 1], 0)

            # Asset price process
            S[t] = S[t - 1] * np.exp((self.r - 0.5 * v[t - 1]) * self.dt +
                                     np.sqrt(v[t - 1] * self.dt) * z1[t - 1])

            # Variance process (using full truncation scheme)
            v[t] = v[t - 1] + self.kappa * (self.theta - v[t - 1]) * self.dt + \
                   self.sigma * np.sqrt(np.maximum(v[t - 1], 0) * self.dt) * w2[t - 1]

        return S, v

    def price_european_call(self, K, n_paths=10000, seed=None):
        """
        Price European call option using Monte Carlo simulation
        K: Strike price
        n_paths: Number of simulation paths
        Returns: tuple of (option price, standard error)
        """
        S, _ = self.simulate_paths(n_paths, seed)

        # Calculate payoff at maturity
        payoff = np.maximum(S[-1] - K, 0)

        # Discount back to present value
        price = np.exp(-self.r * self.T) * np.mean(payoff)
        std_err = np.std(payoff) / np.sqrt(n_paths)

        return price, std_err


def plot_simulation(S, v, title="Heston Model Simulation"):
    """
    Plot sample paths for price and volatility
    """
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(S[:, :5])  # Plot first 5 price paths
    plt.title("Sample Stock Price Paths")
    plt.xlabel("Time Step")
    plt.ylabel("Stock Price")

    plt.subplot(1, 2, 2)
    plt.plot(v[:, :5])  # Plot first 5 volatility paths
    plt.title("Sample Volatility Paths")
    plt.xlabel("Time Step")
    plt.ylabel("Volatility")

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    # Model parameters
    S0 = 100.0  # Initial stock price
    v0 = 0.04  # Initial variance
    r = 0.05  # Risk-free rate
    kappa = 2.0  # Mean reversion speed
    theta = 0.04  # Long-term variance
    sigma = 0.3  # Volatility of volatility
    rho = -0.7  # Correlation
    T = 1.0  # Time to maturity
    steps = 252  # Number of time steps (daily)

    # Initialize model
    heston = HestonModel(S0, v0, r, kappa, theta, sigma, rho, T, steps)

    # Simulate paths
    n_paths = 1000
    S, v = heston.simulate_paths(n_paths, seed=42)

    # Price a European call option
    K = 100.0  # Strike price
    price, std_err = heston.price_european_call(K, n_paths)
    print(f"European Call Option Price: {price:.4f}")
    print(f"Standard Error: {std_err:.4f}")

    # Plot sample paths
    plot_simulation(S, v)