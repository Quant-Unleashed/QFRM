from dataclasses import dataclass
from typing import Optional, List, Union
from collections import defaultdict
import pandas as pd

@dataclass
class MarketInstrument:
    """
    Represents a single market instrument used for yield curve construction.

    Attributes:
        instrument_type (str): Type of instrument (e.g., 'swap', 'deposit', 'bond').
        tenor (str): Maturity tenor (e.g., '3M', '5Y').
        rate (float): Quoted interest rate.
        maturity (Optional[str]): Optional ISO date string (e.g., '2025-12-31').
        convention (Optional[dict]): Optional dictionary of market conventions
            (e.g., {'day_count': 'ACT/360', 'calendar': 'TARGET'}).
    """
    instrument_type: str
    tenor: str
    rate: float
    maturity: Optional[str] = None
    convention: Optional[dict] = None

    def __repr__(self):
        """
        Returns a compact string representation for debugging and inspection.
        """
        return f"<{self.instrument_type} {self.tenor} @ {self.rate:.4f}>"

    def to_dict(self) -> dict:
        """
        Serializes the instrument to a dictionary.
        """
        return {
            "instrument_type": self.instrument_type,
            "tenor": self.tenor,
            "rate": self.rate,
            "maturity": self.maturity,
            "convention": self.convention
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MarketInstrument":
        """
        Creates a MarketInstrument from a dictionary.
        """
        return cls(
            instrument_type=data["instrument_type"],
            tenor=data["tenor"],
            rate=float(data["rate"]),
            maturity=data.get("maturity"),
            convention=data.get("convention")
        )


def load_instruments_from_df(df: pd.DataFrame, instrument_type: str, convention: Optional[dict] = None) -> List[MarketInstrument]:
    """
    Loads a list of MarketInstrument objects from a pandas DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with columns 'tenor' and 'rate'.
        instrument_type (str): Type of instrument to assign.
        convention (Optional[dict]): Optional convention dictionary.

    Returns:
        List[MarketInstrument]: Parsed instrument list.
    """
    required = ["tenor", "rate"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    return [
        MarketInstrument(
            instrument_type=instrument_type,
            tenor=row["tenor"],
            rate=row["rate"],
            maturity=row.get("maturity"),
            convention=convention
        )
        for _, row in df.iterrows()
    ]

def instruments_to_dataframe(instruments: List[MarketInstrument]) -> pd.DataFrame:
    """
    Converts a list of MarketInstrument objects to a pandas DataFrame.
    """
    return pd.DataFrame([inst.to_dict() for inst in instruments])

def filter_instruments(instruments: List[MarketInstrument], instrument_type: Optional[str] = None, tenor_prefix: Optional[str] = None) -> List[MarketInstrument]:
    """
    Filters instruments by type and/or tenor prefix.
    """
    result = instruments
    if instrument_type:
        result = [inst for inst in result if inst.instrument_type == instrument_type]
    if tenor_prefix:
        result = [inst for inst in result if inst.tenor.startswith(tenor_prefix)]
    return result

def apply_rate_shift(instruments: List[MarketInstrument], shift: Union[float, callable]) -> List[MarketInstrument]:
    """
    Applies a rate shift or transformation to all instruments.

    Args:
        instruments (List[MarketInstrument]): List of instruments.
        shift (float or callable): Either a fixed rate shift or a function.

    Returns:
        List[MarketInstrument]: New list with adjusted rates.
    """
    return [
        MarketInstrument(
            instrument_type=inst.instrument_type,
            tenor=inst.tenor,
            rate=shift(inst.rate) if callable(shift) else inst.rate + shift,
            maturity=inst.maturity,
            convention=inst.convention
        )
        for inst in instruments
    ]


def group_by_type(instruments: List[MarketInstrument]) -> dict:
    """
    Groups instruments by their type.

    Returns:
        dict: Keys are instrument types, values are lists of instruments.
    """
    grouped = defaultdict(list)
    for inst in instruments:
        grouped[inst.instrument_type].append(inst)
    return dict(grouped)






class InstrumentSet:
    """
    A container for managing a collection of MarketInstrument objects.

    Supports filtering, grouping, transformation, and export utilities.
    """

    def __init__(self, instruments: Optional[List[MarketInstrument]] = None):
        """
        Initializes the set with an optional list of instruments.
        """
        self.instruments = instruments or []

    def __repr__(self):
        """
        Returns a compact summary of the instrument set.
        """
        return f"<InstrumentSet: {len(self.instruments)} instruments>"

    def add(self, instrument: MarketInstrument):
        """
        Adds a single instrument to the set.
        """
        self.instruments.append(instrument)

    def extend(self, instruments: List[MarketInstrument]):
        """
        Adds multiple instruments to the set.
        """
        self.instruments.extend(instruments)

    def filter(self, instrument_type: Optional[str] = None, tenor_prefix: Optional[str] = None) -> "InstrumentSet":
        """
        Returns a new InstrumentSet filtered by type and/or tenor prefix.
        """
        filtered = filter_instruments(self.instruments, instrument_type, tenor_prefix)
        return InstrumentSet(filtered)

    def shift(self, shift: Union[float, callable]) -> "InstrumentSet":
        """
        Returns a new InstrumentSet with rates shifted or transformed.
        """
        shifted = apply_rate_shift(self.instruments, shift)
        return InstrumentSet(shifted)

    def group_by_type(self) -> dict:
        """
        Groups instruments by type and returns a dictionary.
        """
        return group_by_type(self.instruments)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the instrument set to a pandas DataFrame.
        """
        return instruments_to_dataframe(self.instruments)

    def sort_by_tenor(self, custom_order: Optional[List[str]] = None):
        """
        Sorts instruments by tenor using a custom order if provided.
        """
        if custom_order:
            order_map = {tenor: i for i, tenor in enumerate(custom_order)}
            self.instruments.sort(key=lambda inst: order_map.get(inst.tenor, float('inf')))
        else:
            self.instruments.sort(key=lambda inst: inst.tenor)

    def __iter__(self):
        """
        Allows iteration over the instrument set.
        """
        return iter(self.instruments)

    def __len__(self):
        """
        Returns the number of instruments.
        """
        return len(self.instruments)

    def __getitem__(self, index):
        """
        Enables indexing into the instrument set.
        """
        return self.instruments[index]