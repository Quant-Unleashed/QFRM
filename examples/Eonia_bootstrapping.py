from operator import index

import QuantLib as ql
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from datetime import datetime

# Set the evaluation date to today (August 25, 2025, 03:09 AM BST)
evaluation_date = ql.Date(25, ql.August, 2025)
ql.Settings.instance().evaluationDate = evaluation_date

# Custom function to create deposit rate helpers
def create_deposit_helpers():
    """Create deposit rate helpers for the short end of the curve."""
    deposit_data = [(0.04, 0), (0.04, 1), (0.04, 2)]  # Rates (%) and fixing days from paper
    helpers = []
    for rate, fixing_days in deposit_data:
        helper = ql.DepositRateHelper(
            ql.QuoteHandle(ql.SimpleQuote(rate / 100)),
            ql.Period(1, ql.Days),
            fixing_days,
            ql.TARGET(),
            ql.Following,
            False,
            ql.Actual360()
        )
        helpers.append(helper)
    return helpers

# Custom function to create OIS rate helpers
def create_ois_helpers(eonia_index):
    """Create OIS rate helpers for various tenors based on Eonia index."""
    short_ois_data = [(0.070, (1, ql.Weeks)), (0.069, (2, ql.Weeks)),
                      (0.078, (3, ql.Weeks)), (0.074, (1, ql.Months))]
    dated_ois_data = [(0.046, ql.Date(16, ql.January, 2013), ql.Date(13, ql.February, 2013)),
                      (0.016, ql.Date(13, ql.February, 2013), ql.Date(13, ql.March, 2013)),
                      (-0.007, ql.Date(13, ql.March, 2013), ql.Date(10, ql.April, 2013)),
                      (-0.013, ql.Date(10, ql.April, 2013), ql.Date(8, ql.May, 2013)),
                      (-0.014, ql.Date(8, ql.May, 2013), ql.Date(12, ql.June, 2013))]
    long_ois_data = [(0.002, (15, ql.Months)), (0.008, (18, ql.Months)),
                     (0.021, (21, ql.Months)), (0.036, (2, ql.Years)),
                     (0.127, (3, ql.Years)), (0.274, (4, ql.Years)),
                     (0.456, (5, ql.Years)), (0.647, (6, ql.Years)),
                     (0.827, (7, ql.Years)), (0.996, (8, ql.Years)),
                     (1.147, (9, ql.Years)), (1.280, (10, ql.Years)),
                     (1.404, (11, ql.Years)), (1.516, (12, ql.Years)),
                     (1.764, (15, ql.Years)), (1.939, (20, ql.Years)),
                     (2.003, (25, ql.Years)), (2.038, (30, ql.Years))]

    helpers = []
    # Short OIS helpers
    for rate, tenor in short_ois_data:
        helper = ql.OISRateHelper(2, ql.Period(*tenor),
                                 ql.QuoteHandle(ql.SimpleQuote(rate / 100)), eonia_index)
        helpers.append(helper)
    # Dated OIS helpers
    for rate, start_date, end_date in dated_ois_data:
        helper = ql.DatedOISRateHelper(start_date, end_date,
                                      ql.QuoteHandle(ql.SimpleQuote(rate / 100)), eonia_index)
        helpers.append(helper)
    # Long OIS helpers
    for rate, tenor in long_ois_data:
        helper = ql.OISRateHelper(2, ql.Period(*tenor),
                                 ql.QuoteHandle(ql.SimpleQuote(rate / 100)), eonia_index)
        helpers.append(helper)
    return helpers

# Custom function to build the yield curve
def build_yield_curve(helpers):
    """Build a piecewise log-cubic discount curve from rate helpers."""
    curve = ql.PiecewiseLogCubicDiscount(0, ql.TARGET(), helpers, ql.Actual365Fixed())
    curve.enableExtrapolation()
    return curve

# Custom function to generate forward rates for plotting
def generate_forward_rates(curve, start_date, end_period):
    """Generate forward rates over a date range for visualization."""
    dates = [ql.Date(serial) for serial in range(start_date.serialNumber(),
                                                (start_date + end_period).serialNumber() + 1)]
    forward_rates = [curve.forwardRate(d, ql.TARGET().advance(d, 1, ql.Days),
                                      ql.Actual360(), ql.Simple).rate()
                     for d in dates]
    return dates, forward_rates

# Custom function to plot the yield curve
def plot_yield_curve(dates, rates, title, label):
    """Plot the forward rates of the yield curve."""
    fig, ax = plt.subplots(figsize=(12, 6))
    times = [ql.Actual365Fixed().yearFraction(dates[0], d) for d in dates]
    ax.plot(times, rates, '-', label=label)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=2))
    ax.set_title(title)
    ax.legend(loc='best')
    plt.show()

# Custom function to create a floating-rate bond
def create_floating_rate_bond(start_date, maturity_date, index, face_amount=100.0):
    """Create a floating-rate bond with the given index and schedule."""
    schedule = ql.MakeSchedule(start_date, maturity_date, ql.Period(6, ql.Months))
    bond = ql.FloatingRateBond(0, face_amount, schedule, index,
                              ql.ActualActual(ql.ActualActual.ISMA))
    return bond

# Custom function to set pricing engine and forecast cash flows
def setup_bond_pricing(start_date, bond, yield_curve_handle):
    """Set the pricing engine and forecast cash flows for the bond."""
    bond.setPricingEngine(ql.DiscountingBondEngine(yield_curve_handle))
    ql.setCouponPricer(bond.cashflows(), ql.BlackIrsPricer())  # Simple pricer for forecasting
    # Add an example fixing for the start date (adjust with real data if available)
    index.addFixing(start_date, 0.003)  # Example 0.3% fixing

# Custom function to calculate bond yield
def calculate_bond_yield(bond, clean_price):
    """Calculate the yield of the bond given its clean price."""
    try:
        yield_value = bond.yield(clean_price, ql.Actual365Fixed(), ql.Compounded, ql.Semiannual)
        return yield_value
    except RuntimeError as e:
        print(f"Yield calculation failed: {e}. Ensure cash flows are fully forecasted.")
        return None

# Main execution
if __name__ == "__main__":
    # Initialize Eonia index
    eonia_index = ql.Eonia()

    # Create rate helpers
    deposit_helpers = create_deposit_helpers()
    ois_helpers = create_ois_helpers(eonia_index)
    all_helpers = deposit_helpers + ois_helpers

    # Build the Eonia yield curve
    eonia_curve = build_yield_curve(all_helpers)
    eonia_handle = ql.RelinkableYieldTermStructureHandle(eonia_curve)

    # Create Euribor6M index with Eonia as discounting curve
    euribor6m_index = ql.Euribor6M(eonia_handle)

    # Generate and plot forward rates for Eonia curve
    short_end_date = eonia_curve.referenceDate()
    short_end_period = ql.Period(2, ql.Years)
    dates, forward_rates = generate_forward_rates(eonia_curve, short_end_date, short_end_period)
    plot_yield_curve(dates, forward_rates, "Eonia Forward Rates (Short Term)", "Cubic Interpolation")

    # Long-term plot
    long_end_period = ql.Period(40, ql.Years)
    dates, forward_rates = generate_forward_rates(eonia_curve, short_end_date, long_end_period)
    plot_yield_curve(dates, forward_rates, "Eonia Forward Rates (Long Term)", "Cubic Interpolation")

    # Create and price a floating-rate bond
    bond_start_date = ql.Date(25, ql.August, 2025)  # Start today
    bond_maturity_date = bond_start_date + ql.Period(5, ql.Years)
    bond = create_floating_rate_bond(bond_start_date, bond_maturity_date, euribor6m_index)
    setup_bond_pricing(bond, eonia_handle)

    # Calculate and print bond details
    bond_npv = bond.NPV()
    print(f"Bond NPV: {bond_npv:.2f}")
    bond_yield = calculate_bond_yield(bond, bond_npv)
    if bond_yield is not None:
        print(f"Bond Yield: {bond_yield * 100:.4f}%")