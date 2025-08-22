import math as m
import scipy.stats as st

import matplotlib.pyplot as plt

s = 110
k = 120
r = 0.05
T = 0.5
sigma = 0.9214
n = 1029
t = T/n

# Black Schole Merton Model
def bsm(s,k,r,T,sigma,n,t):
    d1 = (m.log(s/k) + (r + (0.5*(sigma**2)))*(n*t))/(m.sqrt(n*t)*sigma)
    d2 = (m.log(s/k) + (r - (0.5*(sigma**2)))*(n*t))/(m.sqrt(n*t)*sigma)
    Call = s * st.norm.cdf(d1) - (k * m.exp(-(r*(T))) * st.norm.cdf(d2))
    return(Call)

# Delta
def bsmdelta(s,k,r,T,sigma,n,t):
    d1 = (m.log(s/k) + (r + (0.5*(sigma**2)))*(n*t))/(m.sqrt(n*t)*sigma)
    delta = st.norm.cdf(d1)
    return(delta)
        
deltas_80 = [bsmdelta(i,80,0.05,1,0.2,1,1) for i in range(1,201,5)]
deltas_120 = [bsmdelta(i,120,0.05,1,0.2,1,1) for i in range(1,201,5)]

#Vega
def bsmvega(s,k,r,T,sigma,t,n):
    d1 = (m.log(s/k) + (r + (0.5*(sigma**2)))*(n*t))/(m.sqrt(n*t)*sigma)
    vega = s * st.norm.pdf(d1) * m.sqrt(T)
    return(vega)

vegas_80 = [bsmvega(i,80,0.05,1,0.2,1,1) for i in range(1,201,5)]
vegas_120 = [bsmvega(i,120,0.05,1,0.2,1,1) for i in range(1,201,5)]

spread_delta = [deltas_80[i] - deltas_120[i] for i in range(0,len(deltas_80))]
spread_vega = [vegas_80[i] - vegas_120[i] for i in range(0,len(vegas_80))]

plt.plot(range(1,201,5), spread_vega)
