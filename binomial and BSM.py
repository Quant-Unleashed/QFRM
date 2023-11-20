import math as m
import scipy.stats as st


# import matplotlib.pyplot as plt

# Checks if input meets requirements else asks for correct input

class DataQuality:
    def __init__(self, var_value, var_name: str):
        self.x = var_value
        self.var_name = str(var_name)

    def check_data(self):
        try:
            if self.x is None:
                while True:
                    self.x = input("please enter " + self.var_name + ":")
                    if self.x is not None:
                        break
            return self.x
        except ValueError:
            print("There is some bug in the code. Kindly contact the code administrator")
        finally:
            print("Thank you for entering the " + self.var_name)


# Option's class: data loading, BSM european call pricing, delta, and vega calculation
class Option:
    def __init__(self, s0: float = None, strike: float = None, rate: float = None, expiry: float = None,
                 vol: float = None, dq: DataQuality = DataQuality):
        if callable(dq):
            self.s0 = float(dq(s0, "share price").check_data())
            self.strike = float(dq(strike, "strike").check_data())
            self.rate = float(dq(rate, "interest rate").check_data())
            self.expiry = float(dq(expiry, "expiry").check_data())
            self.vol = float(dq(vol, "volatility").check_data())

    # Black Schole Merton Model
    def bsm(self):
        d1 = (m.log(self.s0 / self.strike) + (self.rate + (0.5 * (self.vol ** 2))) * self.expiry) / (m.sqrt(self.expiry)
                                                                                                     * self.vol)
        d2 = (m.log(self.s0 / self.strike) + (self.rate - (0.5 * (self.vol ** 2))) * self.expiry) / (m.sqrt(self.expiry)
                                                                                                     * self.vol)
        call_price = self.s0 * st.norm.cdf(d1) - (self.strike * m.exp(-(self.rate * self.expiry)) * st.norm.cdf(d2))
        return call_price

    # Delta
    def bsm_delta(self):
        d1 = (m.log(self.s0 / self.strike) + (self.rate + (0.5 * (self.vol ** 2))) * self.expiry) / (m.sqrt(self.expiry)
                                                                                                     * self.vol)
        delta = st.norm.cdf(d1)
        return delta

    # Vega
    def bsm_vega(self):
        d1 = (m.log(self.s0 / self.strike) + (self.rate + (0.5 * (self.vol ** 2))) * self.expiry) / (m.sqrt(self.expiry)
                                                                                                     * self.vol)
        vega = self.s0 * st.norm.pdf(d1) * m.sqrt(self.expiry)
        return vega


# Need to fix the classes above

call = Option(100, 90, 0.07, 0.25, 0.6)
print(call.bsm())
print(call.bsm_delta())
print(call.bsm_vega())

# Old Code

# class OptionPricing:
#
#     def __init__(self, s0: float, strike: float, rate: float, time: float, vol: float):
#         self.s0 = s0
#         self.strike = strike
#         self.rate = rate
#         self.expiry = time
#         self.vol = vol
#
#     # Black Schole Merton Model
#     # def bsm(self):
#     #     d1 = (m.log(s / k) + (r + (0.5 * (sigma ** 2))) * (T)) / (m.sqrt(T) * sigma)
#     #     d2 = (m.log(s / k) + (r - (0.5 * (sigma ** 2))) * (T)) / (m.sqrt(T) * sigma)
#     #     Call = s * st.norm.cdf(d1) - (k * m.exp(-(r * (T))) * st.norm.cdf(d2))
#     #     return (Call)
#
#     # Delta
#     def bsmdelta(self):
#         d1 = (m.log(self.s0 / self.strike) + (self.rate + (0.5 * (self.vol ** 2))) * self.expiry) / (m.sqrt(self.expiry)
#                                                                                                      * self.vol)
#         delta = st.norm.cdf(d1)
#         return delta
    # def bsmdelta(self):
    #     d1 = (m.log(s / k) + (r + (0.5 * (sigma ** 2))) * (T)) / (m.sqrt(T) * sigma)
    #     delta = st.norm.cdf(d1)
    #     return (delta)

    # deltas_80 = [bsmdelta(i,80,0.05,1,0.2,1,1) for i in range(1,201,5)]
    # deltas_120 = [bsmdelta(i,120,0.05,1,0.2,1,1) for i in range(1,201,5)]

    # Vega
    # def bsmvega(self):
    #     d1 = (m.log(s / k) + (r + (0.5 * (sigma ** 2))) * (T)) / (m.sqrt(T) * sigma)
    #     vega = s * st.norm.pdf(d1) * m.sqrt(T)
    #     return (vega)

    # vegas_80 = [bsmvega(i,80,0.05,1,0.2,1,1) for i in range(1,201,5)]
    # vegas_120 = [bsmvega(i,120,0.05,1,0.2,1,1) for i in range(1,201,5)]

    # spread_delta = [deltas_80[i] - deltas_120[i] for i in range(0,len(deltas_80))]
    # spread_vega = [vegas_80[i] - vegas_120[i] for i in range(0,len(vegas_80))]

    # plt.plot(range(1,201,5), spread_vega)


# s1 = 110
# k1 = 120
# r1 = 0.05
# T1 = 0.5
# sigma1 = 0.9214
#
# op = OptionPricing(s1, k1, r1, T1, sigma1)
# print(op.bsm())
# print(op.bsmdelta())
# print(op.bsmvega())
