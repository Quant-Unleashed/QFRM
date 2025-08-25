from typing import List, Dict, Optional, Union
from YieldCurve.yc_instruments import MarketInstrument
from YieldCurve.yc_curve_conventions import CurveConvention
from YieldCurve.yc_curves import YieldCurve
#from YieldCurve.yc_utils import log_debug
#from YieldCurve.yc_error_tree import ErrorTree
#from YieldCurve.yc_instrument_validator import InstrumentValidator
#from YieldCurve.yc_bootstrap_registry import BootstrapRegistry

"""
These imports cover:

•  Instrument structure
•  Curve conventions and interpolation rules
•  Curve object for output
•  Logging and error handling
•  Validation and registry hooks
"""

class BootstrapEngine:
    """
    Bootstraps a yield curve using a specified algorithm and conventions.
    """

    def __init__(
        self,
        instruments: List[MarketInstrument],
        convention: CurveConvention,
        algorithm: Optional["BootstrapAlgorithm"] = None
    ):
        """
        Args:
            instruments: List of instruments to bootstrap from.
            convention: CurveConvention object with interpolation rules.
            algorithm: Optional BootstrapAlgorithm instance.
        """
        self.instruments = instruments
        self.convention = convention
        self.algorithm = algorithm or SimpleDepositBootstrap()
        self.results: Dict[str, float] = {}

    def run(self):
        """
        Executes the bootstrapping algorithm.
        """
        validator = InstrumentValidator(self.instruments)
        if not validator.validate():
            ErrorTree.print(validator.errors)
            raise ValueError("Instrument validation failed.")

        self.results = self.algorithm.bootstrap(self.instruments, self.convention)
        log_debug(f"Bootstrapped {len(self.results)} tenors.")

    def get_curve(self) -> YieldCurve:
        """
        Returns a YieldCurve object from the bootstrapped results.
        """
        return YieldCurve(self.results, self.convention)


class BootstrapAlgorithm:
    """
    Abstract base class for bootstrapping algorithms.
    """

    def bootstrap(self, instruments: List[MarketInstrument], convention: CurveConvention) -> Dict[str, float]:
        raise NotImplementedError("Subclasses must implement bootstrap()")

class SimpleDepositBootstrap(BootstrapAlgorithm):
    """
    Bootstraps discount factors from deposit instruments using simple interest.
    """

    def bootstrap(self, instruments: List[MarketInstrument], convention: CurveConvention) -> Dict[str, float]:
        results = {}
        for inst in instruments:
            if inst.instrument_type != "deposit":
                continue
            year_frac = convention.year_fraction(inst.tenor)
            df = 1 / (1 + inst.rate * year_frac)
            results[inst.tenor] = df
        return results




class ForwardRateBootstrap(BootstrapAlgorithm):
    """
    Bootstraps discount factors using forward rate logic.
    This version assumes:

    • Instruments are ordered by tenor
    • Each instrument provides a forward rate for a specific period
    • We recursively compute discount factors using forward rates

    """

    def bootstrap(self, instruments: List[MarketInstrument], convention: CurveConvention) -> Dict[str, float]:
        results = {}
        sorted_instruments = sorted(instruments, key=lambda inst: convention.tenor_order(inst.tenor))

        for i, inst in enumerate(sorted_instruments):
            tenor = inst.tenor
            rate = inst.rate
            year_frac = convention.year_fraction(tenor)

            if i == 0:
                # First tenor: assume spot rate
                df = 1 / (1 + rate * year_frac)
            else:
                # Use forward rate logic:
                # DF_t = DF_prev / (1 + fwd_rate * delta_t)
                prev_tenor = sorted_instruments[i - 1].tenor
                prev_df = results[prev_tenor]
                delta = convention.year_fraction_between(prev_tenor, tenor)
                df = prev_df / (1 + rate * delta)

            results[tenor] = df

        return results