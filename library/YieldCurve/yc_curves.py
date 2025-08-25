import numpy as np
from typing import List, Dict, Optional
#from yc_curve_conventions import CurveConvention
import matplotlib.pyplot as plt
from YieldCurve.yc_curve_conventions import CurveConvention

class YieldCurve:
    """
    Represents a bootstrapped yield curve with interpolation and metadata.
    """

    def __init__(
        self,
        name: str,
        tenors: List[str],
        zero_rates: List[float],
        convention: Optional[CurveConvention] = None
    ):
        """
        Args:
            name: Curve identifier (e.g., 'USD_OIS').
            tenors: List of tenor strings (e.g., ['1M', '3M', '6M', '1Y']).
            zero_rates: Corresponding zero rates (annualized).
            convention: CurveConvention object for interpolation and time conversion.
        """
        self.name = name
        self.tenors = tenors
        self.zero_rates = zero_rates
        self.convention = convention or CurveConvention()
        self.times = [self.convention.year_fraction(t) for t in tenors]

    def get_rate(self, t: float) -> float:
        """
        Returns interpolated zero rate at time t (in years).
        """
        x = self.times
        y = self.zero_rates

        if t <= x[0]:
            return y[0] if self.convention.extrapolate else np.nan
        elif t >= x[-1]:
            return y[-1] if self.convention.extrapolate else np.nan
        else:
            if self.convention.interpolation == "linear":
                return np.interp(t, x, y)
            elif self.convention.interpolation == "log-linear":
                log_y = np.log(y)
                return np.exp(np.interp(t, x, log_y))
            else:
                raise NotImplementedError(f"Interpolation '{self.convention.interpolation}' not supported.")

    def get_df(self, t: float) -> float:
        """
        Returns discount factor at time t.
        """
        r = self.get_rate(t)
        return np.exp(-r * t) if not np.isnan(r) else np.nan

    def describe(self) -> Dict:
        """
        Returns metadata and curve summary.
        """
        return {
            "name": self.name,
            "tenors": self.tenors,
            "zero_rates": self.zero_rates,
            "convention": self.convention.describe()
        }

    def __repr__(self):
        return f"<YieldCurve {self.name}, {len(self.tenors)} points>"


    def plot(self, kind: str = "rate", show: bool = True):
        """
        Plots the yield curve.

        Args:
            kind: 'rate' for zero rates, 'df' for discount factors.
            show: Whether to display the plot immediately.
        """
        x_dense = np.linspace(self.times[0], self.times[-1], 100)
        if kind == "rate":
            y_dense = [self.get_rate(t) for t in x_dense]
            label = "Zero Rate"
        elif kind == "df":
            y_dense = [self.get_df(t) for t in x_dense]
            label = "Discount Factor"
        else:
            raise ValueError("kind must be 'rate' or 'df'")

        plt.figure(figsize=(8, 4))
        plt.plot(x_dense, y_dense, label=label, color="navy")
        plt.scatter(self.times, self.zero_rates if kind == "rate" else [self.get_df(t) for t in self.times], color="red", zorder=5)
        plt.title(f"{self.name} Curve — {label}")
        plt.xlabel("Time (Years)")
        plt.ylabel(label)
        plt.grid(True)
        plt.legend()
        if show:
            plt.show()