from typing import Literal

class CurveConvention:
    """
    Defines interpolation, extrapolation, and time conversion rules for yield curves.
    """

    def __init__(
        self,
        interpolation: Literal["linear", "log-linear", "cubic"] = "linear",
        extrapolate: bool = True,
        day_count: str = "ACT/360",
        calendar: str = "TARGET"
    ):
        """
        Args:
            interpolation: Method used for curve interpolation.
            extrapolate: Whether to allow extrapolation beyond known tenors.
            day_count: Day count convention (e.g., 'ACT/360', '30/360').
            calendar: Calendar used for business day adjustments.
        """
        self.interpolation = interpolation
        self.extrapolate = extrapolate
        self.day_count = day_count
        self.calendar = calendar

    def year_fraction(self, tenor: str) -> float:
        """
        Converts a tenor string to a year fraction.

        Examples:
            '3M' → 0.25, '1Y' → 1.0
        """
        if tenor.endswith("D"):
            return int(tenor[:-1]) / 365
        elif tenor.endswith("W"):
            return int(tenor[:-1]) * 7 / 365
        elif tenor.endswith("M"):
            return int(tenor[:-1]) / 12
        elif tenor.endswith("Y"):
            return int(tenor[:-1])
        else:
            raise ValueError(f"Unknown tenor format: {tenor}")

    def tenor_order(self, tenor: str) -> float:
        """
        Returns a numeric value for sorting tenors chronologically.
        """
        return self.year_fraction(tenor)

    def year_fraction_between(self, t1: str, t2: str) -> float:
        """
        Computes the year fraction between two tenors.
        Assumes t2 > t1.
        """
        return self.year_fraction(t2) - self.year_fraction(t1)

    def describe(self) -> dict:
        """
        Returns a dictionary summary of the convention.
        """
        return {
            "interpolation": self.interpolation,
            "extrapolate": self.extrapolate,
            "day_count": self.day_count,
            "calendar": self.calendar
        }

    def __repr__(self):
        return f"<CurveConvention {self.interpolation}, {self.day_count}, extrapolate={self.extrapolate}>"