import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# SABR model implementation using Hagan et al. approximation
def sabr_implied_vol(f, k, t, alpha, beta, rho, nu):
    """
    Calculate SABR implied volatility.
    Parameters:
        f: Forward price (float)
        k: Strike price (float)
        t: Time to maturity (years, float)
        alpha: Initial volatility level (float, >0)
        beta: Elasticity of variance (float, 0<=beta<=1)
        rho: Correlation between asset and vol (-1<=rho<=1)
        nu: Volatility of volatility (float, >0)
    Returns:
        Implied volatility (float)
    """
    # ATM case (f == k)
    if abs(f - k) < 1e-6:
        term1 = alpha / (f ** (1 - beta))
        term2 = 1 + ((1 - beta) ** 2 / 24) * (alpha ** 2 / (f ** (2 - 2 * beta)))
        term3 = (rho * beta * nu * alpha) / (4 * f ** (1 - beta))
        term4 = (2 - 3 * rho ** 2) * nu ** 2 / 24
        return term1 * (1 + (term2 + term3 + term4) * t)

    # Non-ATM case
    z = (nu / alpha) * (f * k) ** ((1 - beta) / 2) * np.log(f / k)
    x = np.log((np.sqrt(1 - 2 * rho * z + z ** 2) + z - rho) / (1 - rho))
    numerator = alpha * (1 + ((1 - beta) ** 2 / 24) * np.log(f / k) ** 2 +
                         ((1 - beta) ** 4 / 1920) * np.log(f / k) ** 4)
    denominator = ((f * k) ** ((1 - beta) / 2)) * (
            1 + ((1 - beta) ** 2 / 24) * (alpha ** 2 / ((f * k) ** (1 - beta))) +
            (rho * beta * nu * alpha) / (4 * (f * k) ** ((1 - beta) / 2)) +
            (2 - 3 * rho ** 2) * nu ** 2 / 24) * t
    return (numerator / denominator) * (z / x) if x != 0 else np.nan


# Plot volatility smile for varying parameters
def plot_sabr_smile(f=100, t=1.0, alpha=0.2, beta=0.5, rho=-0.5, nu=0.5):
    """
    Plot volatility smile and show effect of tweaking parameters.
    """
    strikes = np.linspace(50, 150, 100)  # Strike prices around forward (100)

    # Base case
    base_vols = [sabr_implied_vol(f, k, t, alpha, beta, rho, nu) for k in strikes]

    # Tweaked parameters
    alpha_vols = [sabr_implied_vol(f, k, t, alpha * 1.5, beta, rho, nu) for k in strikes]  # Increase alpha
    rho_vols = [sabr_implied_vol(f, k, t, alpha, beta, 0.0, nu) for k in strikes]  # Zero rho
    nu_vols = [sabr_implied_vol(f, k, t, alpha, beta, rho, nu * 1.5) for k in strikes]  # Increase nu

    plt.figure(figsize=(10, 6))
    plt.plot(strikes, base_vols, label=f'Base (α={alpha}, β={beta}, ρ={rho}, ν={nu})', linewidth=2)
    plt.plot(strikes, alpha_vols, label=f'Higher α ({alpha * 1.5})', linestyle='--')
    plt.plot(strikes, rho_vols, label=f'Zero ρ (0.0)', linestyle='-.')
    plt.plot(strikes, nu_vols, label=f'Higher ν ({nu * 1.5})', linestyle=':')
    plt.axvline(f, color='red', linestyle='--', label='Forward Price')
    plt.title('SABR Volatility Smile: Parameter Sensitivity')
    plt.xlabel('Strike Price')
    plt.ylabel('Implied Volatility')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Explanation of parameter effects
    print("Parameter Effects on Volatility Smile:")
    print("- Alpha (α): Controls overall volatility level. Increasing α shifts the smile upward.")
    print("- Beta (β): Determines asset price dynamics (0=normal, 1=lognormal). Fixed here for simplicity.")
    print(
        "- Rho (ρ): Correlation between asset and vol. Negative ρ creates downward skew; zero ρ makes smile symmetric.")
    print("- Nu (ν): Vol of vol. Higher ν increases curvature of the smile, raising wings.")


# Plot 3D volatility surface
def plot_sabr_surface(f=100, alpha=0.2, beta=0.5, rho=-0.5, nu=0.5):
    """
    Plot 3D volatility surface over strikes and maturities.
    """
    strikes = np.linspace(50, 150, 20)
    maturities = np.linspace(0.1, 2.0, 20)
    K, T = np.meshgrid(strikes, maturities)
    vols = np.array([[sabr_implied_vol(f, k, t, alpha, beta, rho, nu)
                      for k in strikes] for t in maturities])

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(K, T, vols, cmap='viridis')
    ax.set_title('SABR Volatility Surface')
    ax.set_xlabel('Strike Price')
    ax.set_ylabel('Maturity (Years)')
    ax.set_zlabel('Implied Volatility')
    fig.colorbar(surf, ax=ax, label='Implied Vol')
    plt.show()

    print("Volatility Surface shows how implied vol varies with strike and maturity.")
    print("SABR captures smile and term structure; surface shape depends on parameters.")


# Run the model
if __name__ == "__main__":
    # Base parameters
    f = 100  # Forward price
    t = 1.0  # Time to maturity
    alpha = 0.2  # Initial volatility
    beta = 0.5  # Elasticity (0 to 1)
    rho = -0.5  # Correlation
    nu = 0.5  # Vol of vol

    print("SABR Model: Generates implied volatility smile for option pricing.")
    print("Key Parameters:")
    print("- f: Forward price, sets the center of the smile.")
    print("- t: Time to maturity, affects term structure.")
    print("- alpha: Sets volatility level.")
    print("- beta: Controls asset dynamics (fixed at 0.5 here).")
    print("- rho: Drives skew (negative = downward skew).")
    print("- nu: Controls smile curvature.")

    # Plot smile with parameter tweaks
    plot_sabr_smile(f, t, alpha, beta, rho, nu)

    # Plot 3D volatility surface
    plot_sabr_surface(f, alpha, beta, rho, nu)