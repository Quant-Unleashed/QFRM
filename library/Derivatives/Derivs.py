import numpy as np
from scipy.stats import norm


# Futures and Forwards Pricing
def future_price(S0, r, T, dividends=0):
    """
    Price of a future/forward contract.
    S0: initial spot price
    r: risk-free rate
    T: time to maturity
    dividends: continuous dividend yield (for forwards on stocks)
    """
    return S0 * np.exp((r - dividends) * T)


# Vanilla Option Pricing (Black-Scholes)
def black_scholes_call(S0, K, r, sigma, T, q=0):
    """
    Price of a European call option using Black-Scholes.
    q: dividend yield
    """
    d1 = (np.log(S0 / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def black_scholes_put(S0, K, r, sigma, T, q=0):
    """
    Price of a European put option using Black-Scholes.
    """
    d1 = (np.log(S0 / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * np.exp(-q * T) * norm.cdf(-d1)


# Barrier Option Pricing (Monte Carlo for Down-and-Out Call)
def barrier_option_mc(S0, K, r, sigma, T, barrier, n_paths=10000, steps=252, option_type='call',
                      barrier_type='down_out'):
    """
    Price a barrier option using Monte Carlo simulation.
    barrier_type: 'down_out', 'up_out', etc. (simplified to down-and-out)
    """
    dt = T / steps
    paths = S0 * np.exp(
        np.cumsum((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.randn(n_paths, steps), axis=1))

    # Apply barrier condition (down-and-out)
    knocked_out = np.any(paths < barrier, axis=1)
    paths[knocked_out, -1] = 0  # Set payoff to 0 if knocked out

    if option_type == 'call':
        payoffs = np.maximum(paths[:, -1] - K, 0)
    else:
        payoffs = np.maximum(K - paths[:, -1], 0)

    price = np.exp(-r * T) * np.mean(payoffs)
    return price


# Autocallable Note Pricing (Monte Carlo)
def autocallable_mc(S0, coupon, barrier_autocall, barrier_coupon, r, sigma, T, n_coupons, n_paths=10000,
                    steps_per_coupon=252):
    """
    Price an autocallable note using Monte Carlo.
    Simplified: annual coupons, autocall if above barrier_autocall.
    """
    dt = T / (n_coupons * steps_per_coupon)
    paths = S0 * np.exp(np.cumsum(
        (r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.randn(n_paths, n_coupons * steps_per_coupon),
        axis=1))

    payoffs = np.zeros(n_paths)
    for i in range(1, n_coupons + 1):
        idx = i * steps_per_coupon - 1
        active = payoffs == 0
        S_t = paths[active, idx]

        # Autocall check
        autocall = S_t >= barrier_autocall * S0
        payoffs[active & autocall] = S0 + coupon * S0 * i  # Principal + accumulated coupons

        # Coupon payment if not autocalled
        coupon_pay = (S_t >= barrier_coupon * S0) * coupon * S0
        payoffs[active & ~autocall] += coupon_pay

    # At maturity if not autocalled
    active = payoffs == 0
    S_T = paths[active, -1]
    payoffs[active] = np.maximum(S_T, 0)  # Assuming no protection

    price = np.exp(-r * T) * np.mean(payoffs)
    return price


# Range Accrual Pricing (Monte Carlo for interest rate range accrual)
def range_accrual_mc(r0, lower, upper, coupon, T, n_paths=10000, steps=252, kappa=0.1, theta=0.05, sigma_r=0.01):
    """
    Price a range accrual note using Monte Carlo under Vasicek model.
    """
    dt = T / steps
    rates = np.zeros((n_paths, steps + 1))
    rates[:, 0] = r0

    for t in range(1, steps + 1):
        rates[:, t] = rates[:, t - 1] + kappa * (theta - rates[:, t - 1]) * dt + sigma_r * np.sqrt(
            dt) * np.random.randn(n_paths)

    in_range = (rates[:, 1:] >= lower) & (rates[:, 1:] <= upper)
    accrual_days = np.sum(in_range, axis=1) / steps
    payoffs = coupon * accrual_days * T
    price = np.mean(payoffs)
    return price


# Worst-of Put Pricing (Monte Carlo for two assets)
def worst_of_put_mc(S0_1, S0_2, K, r, sigma1, sigma2, rho, T, n_paths=10000, steps=252):
    """
    Price a worst-of put option on two assets using Monte Carlo.
    Payoff: max(K - min(S1_T/S1_0, S2_T/S2_0) * K, 0)
    """
    dt = T / steps
    z1 = np.random.randn(n_paths, steps)
    z2 = rho * z1 + np.sqrt(1 - rho ** 2) * np.random.randn(n_paths, steps)

    paths1 = S0_1 * np.exp(np.cumsum((r - 0.5 * sigma1 ** 2) * dt + sigma1 * np.sqrt(dt) * z1, axis=1))
    paths2 = S0_2 * np.exp(np.cumsum((r - 0.5 * sigma2 ** 2) * dt + sigma2 * np.sqrt(dt) * z2, axis=1))

    perf1 = paths1[:, -1] / S0_1
    perf2 = paths2[:, -1] / S0_2
    worst_perf = np.minimum(perf1, perf2)
    payoffs = np.maximum(K - worst_perf * K, 0)
    price = np.exp(-r * T) * np.mean(payoffs)
    return price


# Correlation Swap Pricing (Monte Carlo for two assets)
def correlation_swap_mc(S0_1, S0_2, K_cor, r, sigma1, sigma2, T, n_paths=10000, steps=252):
    """
    Price a correlation swap: pays realized correlation - K_cor
    """
    dt = T / steps
    z1 = np.random.randn(n_paths, steps)
    z2 = np.random.randn(n_paths, steps)

    returns1 = (r - 0.5 * sigma1 ** 2) * dt + sigma1 * np.sqrt(dt) * z1
    returns2 = (r - 0.5 * sigma2 ** 2) * dt + sigma2 * np.sqrt(dt) * (
                K_cor * z1 + np.sqrt(1 - K_cor ** 2) * z2)  # Implied cor K_cor for pricing?
    # For fair strike, set K_cor=0, price is expected cor.
    # But to price, under measure, but simplified.
    corrs = []
    for i in range(n_paths):
        ret1 = returns1[i]
        ret2 = returns2[i]
        cor = np.corrcoef(ret1, ret2)[0, 1]
        corrs.append(cor)
    realized_cor = np.mean(corrs)
    price = np.exp(-r * T) * (realized_cor - K_cor) * 100  # Notional 100 for example
    return price


# Variance Swap Pricing (Replication approximation)
def variance_swap_price(implied_vols, strikes, weights):
    """
    Approximate variance swap using portfolio of options (replication).
    Simplified: integral of implied vol^2.
    """
    var = np.sum(weights * implied_vols ** 2)
    return np.sqrt(var)  # Volatility swap, or var for variance.


# Yield Curve Models (Nelson-Siegel)
def nelson_siegel(beta0, beta1, beta2, lambda_, maturities):
    """
    Nelson-Siegel yield curve model.
    """
    factor1 = (1 - np.exp(-maturities / lambda_)) / (maturities / lambda_)
    factor2 = factor1 - np.exp(-maturities / lambda_)
    yields = beta0 + beta1 * factor1 + beta2 * factor2
    return yields


# Volatility Models (SABR example simplified)
def sabr_vol(alpha, beta, rho, nu, f, K, T):
    """
    SABR volatility model approximation for ATM.
    Simplified.
    """
    z = nu / alpha * (f * K) ** ((1 - beta) / 2) * np.log(f / K)
    x = np.log((np.sqrt(1 - 2 * rho * z + z ** 2) + z - rho) / (1 - rho))
    vol = alpha / (f * K) ** ((1 - beta) / 2) * (1 + (
                (1 - beta) ** 2 / 24 * np.log(f / K) ** 2 + (1 - beta) ** 4 / 1920 * np.log(f / K) ** 4)) ** -1 * z / x
    return vol


# Correlation Model (Simple Hierarchical)
class HierarchicalCorrelationGenerator:
    def __init__(self, n, n_clusters=5, intra_cor=0.8, inter_cor=0.2):
        self.n = n
        self.n_clusters = n_clusters
        self.intra_cor = intra_cor
        self.inter_cor = inter_cor

    def generate(self):
        cluster_size = self.n // self.n_clusters
        cor_matrix = np.full((self.n, self.n), self.inter_cor)
        for i in range(self.n_clusters):
            start = i * cluster_size
            end = min(start + cluster_size, self.n)
            cor_matrix[start:end, start:end] = self.intra_cor
        np.fill_diagonal(cor_matrix, 1.0)
        return cor_matrix


# Example usage
if __name__ == "__main__":
    # Example parameters
    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1.0

    print("Forward Price:", future_price(S0, r, T))
    print("BS Call:", black_scholes_call(S0, K, r, sigma, T))
    print("Barrier Call:", barrier_option_mc(S0, K, r, sigma, T, barrier=90))
    # Add more examples as needed