import talib as ta
import pandas as pd

periods = 10
tafunc = "EMA"
major = "general"


def TaLib(major, x, Open, close, high, low, volume,  periods):
    if major == "general":
        if x == "BANDS":
            #BBANDS - Bollinger Bands
            upperband, middleband, lowerband = ta.ta.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
            return(upperband, middleband, lowerband)
        
        elif x == "MAMA":
            #MAMA - MESA Adaptive Moving Average
            #NOTE: The MAMA function has an unstable period.
            mama, fama = ta.MAMA(close, fastlimit=0, slowlimit=0)
            return(mama, fama)

        elif x == "DEMA":
            #DEMA - Double Exponential Moving Average
            real = ta.DEMA(close, timeperiod=30)
            return(real)

        elif x == "EMA":
            #EMA - Exponential Moving Average
            #NOTE: The EMA function has an unstable period.
            real = ta.EMA(close, timeperiod=30)
            return(real)

        elif x == "HT_TRENDLINE":
            #HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
            #NOTE: The HT_TRENDLINE function has an unstable period.
            real = ta.HT_TRENDLINE(close)
            return(real)

        elif x == "KAMA":
            #KAMA - Kaufman Adaptive Moving Average
            #NOTE: The KAMA function has an unstable period.
            real = ta.KAMA(close, timeperiod=30)
            return(real)

        elif x == "MA":
            #MA - Moving average
            real = ta.MA(close, timeperiod=14, matype=0)
            return(real)

        elif x == "MAVP":
            #MAVP - Moving average with variable period
            real = ta.MAVP(close, periods, minperiod=2, maxperiod=30, matype=0)
            return(real)

        elif x == "MIDPOINT":
            #MIDPOINT - MidPoint over period
            real = ta.MIDPOINT(close, timeperiod=14)
            return(real)

        elif x == "MIDPRICE":
            #MIDPRICE - Midpoint Price over period
            real = ta.MIDPRICE(high, low, timeperiod=14)
            return(real)

        elif x == "SAR":
            #SAR - Parabolic SAR
            real = ta.SAR(high, low, acceleration=0, maximum=0)
            return(real)

        elif x == "SAREXT":
            #SAREXT - Parabolic SAR - Extended
            real = ta.SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)
            return(real)

        elif x == "SMA":
            #SMA - Simple Moving Average
            real = ta.SMA(close, timeperiod=30)
            return(real)

        elif x == "T3":
            #T3 - Triple Exponential Moving Average (T3)
            #NOTE: The T3 function has an unstable period.
            real = ta.T3(close, timeperiod=5, vfactor=0)
            return(real)

        elif x == "TEMA":
            #TEMA - Triple Exponential Moving Average
            real = ta.TEMA(close, timeperiod=30)
            return(real)

        elif x == "TRIMA":
            #TRIMA - Triangular Moving Average
            real = ta.TRIMA(close, timeperiod=30)
            return(real)

        elif x == "WMA":
            #WMA - Weighted Moving Average
            real = ta.WMA(close, timeperiod=30)
            return(real)

        else:
            real = "No coverage or wrong option selected"
            return real

    #Momentum Indicator Functions
    elif major == "Momentum":

        if x == "ADX":        
            #ADX - Average Directional Movement Index
            #NOTE: The ADX function has an unstable period.
            real = ta.ADX(high, low, close, timeperiod=14)
            return(real)

        elif x == "ADXR":
            #ADXR - Average Directional Movement Index Rating
            #NOTE: The ADXR function has an unstable period.
            real = ta.ADXR(high, low, close, timeperiod=14)
            return(real)

        elif x == "APO":
            #APO - Absolute Price Oscillator
            real = ta.APO(close, fastperiod=12, slowperiod=26, matype=0)
            return(real)

        elif x == "AROON":
            #AROON - Aroon
            aroondown, aroonup = ta.AROON(high, low, timeperiod=14)
            return(real)

        elif x == "AROONOSC":
            #AROONOSC - Aroon Oscillator
            real = ta.AROONOSC(high, low, timeperiod=14)
            return(real)

        elif x == "BOP":
            #BOP - Balance Of Power
            real = ta.BOP(open, high, low, close)
            return(real)

        elif x == "CCI":
            #CCI - Commodity Channel Index
            real = ta.CCI(high, low, close, timeperiod=14)
            return(real)

        elif x == "CMO":
            #CMO - Chande Momentum Oscillator
            #NOTE: The CMO function has an unstable period.
            real = ta.CMO(close, timeperiod=14)
            return(real)

        elif x == "DX":
            #DX - Directional Movement Index
            #NOTE: The DX function has an unstable period.
            real = ta.DX(high, low, close, timeperiod=14)
            return(real)

        elif x == "MACD":
            #MACD - Moving Average Convergence/Divergence
            macd, macdsignal, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
            return(macd, macdsignal, macdhist)

        elif x == "MACDEXT":
            #MACDEXT - MACD with controllable MA type
            macd, macdsignal, macdhist = ta.MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
            return(macd, macdsignal, macdhist)

        elif x == "MACDFIX":
            #MACDFIX - Moving Average Convergence/Divergence Fix 12/26
            macd, macdsignal, macdhist = ta.MACDFIX(close, signalperiod=9)
            return(macd, macdsignal, macdhist)

        elif x == "MFI":
            #MFI - Money Flow Index
            #NOTE: The MFI function has an unstable period.
            real = ta.MFI(high, low, close, volume, timeperiod=14)
            return(real)

        elif x == "MINUS_DI":
            #MINUS_DI - Minus Directional Indicator
            #NOTE: The MINUS_DI function has an unstable period.
            real = ta.MINUS_DI(high, low, close, timeperiod=14)
            return(real)

        elif x == "MINUS_DM":
            #MINUS_DM - Minus Directional Movement
            #NOTE: The MINUS_DM function has an unstable period.
            real = ta.MINUS_DM(high, low, timeperiod=14)
            return(real)

        elif x == "MOM":
            #MOM - Momentum
            real = ta.MOM(close, timeperiod=10)
            return(real)

        elif x == "PLUS_DI":
            #PLUS_DI - Plus Directional Indicator
            #NOTE: The PLUS_DI function has an unstable period.
            real = ta.PLUS_DI(high, low, close, timeperiod=14)
            return(real)

        elif x == "PLUS_DM":
            #PLUS_DM - Plus Directional Movement
            #NOTE: The PLUS_DM function has an unstable period.
            real = ta.PLUS_DM(high, low, timeperiod=14)
            return(real)

        elif x == "PPO":
            #PPO - Percentage Price Oscillator
            real = ta.PPO(close, fastperiod=12, slowperiod=26, matype=0)
            return(real)

        elif x == "ROC":
            #ROC - Rate of change : ((price/prevPrice)-1)*100
            real = ta.ROC(close, timeperiod=10)
            return(real)

        elif x == "ROCP":
            #ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
            real = ta.ROCP(close, timeperiod=10)
            return(real)

        elif x == "ROCR":
            #ROCR - Rate of change ratio: (price/prevPrice)
            real = ta.ROCR(close, timeperiod=10)
            return(real)

        elif x == "ROCR100":
            #ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100
            real = ta.ROCR100(close, timeperiod=10)
            return(real)

        elif x == "RSI":
            #RSI - Relative Strength Index
            #NOTE: The RSI function has an unstable period.
            real = ta.RSI(close, timeperiod=14)
            return(real)

        elif x == "STOCH":
            #STOCH - Stochastic
            slowk, slowd = ta.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
            return(slowk, slowd)

        elif x == "STOCHF":
            #STOCHF - Stochastic Fast
            fastk, fastd = ta.STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
            return(fastk, fastd)

        elif x == "STOCHRSI":
            #STOCHRSI - Stochastic Relative Strength Index
            #NOTE: The STOCHRSI function has an unstable period.
            fastk, fastd = ta.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
            return(fastk, fastd)

        elif x == "TRIX":
            #TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
            real = ta.TRIX(close, timeperiod=30)
            return(real)

        elif x == "ULTOSC":
            #ULTOSC - Ultimate Oscillator
            real = ta.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
            return(real)

        elif x == "WILLR":
            #WILLR - Williams' %R
            real = ta.WILLR(high, low, close, timeperiod=14)
            return(real)
            
        else:
            real = "No coverage or wrong option selected"
            return real

    #Volume Indicator Functions
    elif major == "Volume":

        if x == "WILLR":
            #AD - Chaikin A/D Line
            real = ta.AD(high, low, close, volume)
            return(real)

        elif x == "WILLR":
            #ADOSC - Chaikin A/D Oscillator
            real = ta.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
            return(real)

        elif x == "WILLR":
            #OBV - On Balance Volume
            real = ta.OBV(close, volume)
            return(real)

        else:
            real = "No coverage or wrong option selected"
            return real


    #Volatility Indicator Functions
    elif major == "Volatility":

        if x == "WILLR":
            #ATR - Average True Range
            #NOTE: The ATR function has an unstable period.
            real = ta.ATR(high, low, close, timeperiod=14)
            return(real)

        elif x == "WILLR":
            #NATR - Normalized Average True Range
            #NOTE: The NATR function has an unstable period.
            real = ta.NATR(high, low, close, timeperiod=14)
            return(real)

        elif x == "WILLR":
            #TRANGE - True Range
            real = ta.TRANGE(high, low, close)
            return(real)

        else:
            real = "No coverage or wrong option selected"
            return real

    #Pattern Recognition Functions
    elif major == "Pattern":
        if x == "CDL2CROWS":
            #CDL2CROWS - Two Crows
            integer = ta.CDL2CROWS(open, high, low, close)
            return(integer)

        if x == "CDL3BLACKCROWS":
            #CDL3BLACKCROWS - Three Black Crows
            integer = ta.CDL3BLACKCROWS(open, high, low, close)
            return(integer)

        if x == "CDL3INSIDE":
            #CDL3INSIDE - Three Inside Up/Down
            integer = ta.CDL3INSIDE(open, high, low, close)
            return(integer)

        if x == "CDL3LINESTRIKE":
            #CDL3LINESTRIKE - Three-Line Strike
            integer = ta.CDL3LINESTRIKE(open, high, low, close)
            return(integer)

        if x == "CDL3OUTSIDE":
            #CDL3OUTSIDE - Three Outside Up/Down
            integer = ta.CDL3OUTSIDE(open, high, low, close)
            return(integer)

        if x == "CDL3STARSINSOUTH":
            #CDL3STARSINSOUTH - Three Stars In The South
            integer = ta.CDL3STARSINSOUTH(open, high, low, close)
            return(integer)

        if x == "CDL3WHITESOLDIERS":
            #CDL3WHITESOLDIERS - Three Advancing White Soldiers
            integer = ta.CDL3WHITESOLDIERS(open, high, low, close)
            return(integer)

        if x == "CDLABANDONEDBABY":
            #CDLABANDONEDBABY - Abandoned Baby
            integer = ta.CDLABANDONEDBABY(open, high, low, close, penetration=0)
            return(integer)

        if x == "CDLADVANCEBLOCK":
            #CDLADVANCEBLOCK - Advance Block
            integer = ta.CDLADVANCEBLOCK(open, high, low, close)
            return(integer)

        if x == "CDLBELTHOLD":
            #CDLBELTHOLD - Belt-hold
            integer = ta.CDLBELTHOLD(open, high, low, close)
            return(integer)

        if x == "CDLBREAKAWAY":
            #CDLBREAKAWAY - Breakaway
            integer = ta.CDLBREAKAWAY(open, high, low, close)
            return(integer)

        if x == "CDLCLOSINGMARUBOZU":
            #CDLCLOSINGMARUBOZU - Closing Marubozu
            integer = ta.CDLCLOSINGMARUBOZU(open, high, low, close)
            return(integer)

        if x == "CDLCONCEALBABYSWALL":
            #CDLCONCEALBABYSWALL - Concealing Baby Swallow
            integer = ta.CDLCONCEALBABYSWALL(open, high, low, close)
            return(integer)

        if x == "CDLCOUNTERATTACK":
            #CDLCOUNTERATTACK - Counterattack
            integer = ta.CDLCOUNTERATTACK(open, high, low, close)
            return(integer)

        if x == "CDLDARKCLOUDCOVER":
            #CDLDARKCLOUDCOVER - Dark Cloud Cover
            integer = ta.CDLDARKCLOUDCOVER(open, high, low, close, penetration=0)
            return(integer)

        if x == "CDLDOJI":
            #CDLDOJI - Doji
            integer = ta.CDLDOJI(open, high, low, close)
            return(integer)

        if x == "CDLDOJISTAR":
            #CDLDOJISTAR - Doji Star
            integer = ta.CDLDOJISTAR(open, high, low, close)
            return(integer)

        if x == "CDLDRAGONFLYDOJI":
            #CDLDRAGONFLYDOJI - Dragonfly Doji
            integer = ta.CDLDRAGONFLYDOJI(open, high, low, close)
            return(integer)

        if x == "CDLENGULFING":
            #CDLENGULFING - Engulfing Pattern
            integer = ta.CDLENGULFING(open, high, low, close)
            return(integer)

        if x == "CDLEVENINGDOJISTAR":
            #CDLEVENINGDOJISTAR - Evening Doji Star
            integer = ta.CDLEVENINGDOJISTAR(open, high, low, close, penetration=0)
            return(integer)

        if x == "CDLEVENINGSTAR":
            #CDLEVENINGSTAR - Evening Star
            integer = ta.CDLEVENINGSTAR(open, high, low, close, penetration=0)
            return(integer)

        if x == "CDLGAPSIDESIDEWHITE":
            #CDLGAPSIDESIDEWHITE - Up/Down-gap side-by-side white lines
            integer = ta.CDLGAPSIDESIDEWHITE(open, high, low, close)
            return(integer)

        if x == "CDLGRAVESTONEDOJI":
            #CDLGRAVESTONEDOJI - Gravestone Doji
            integer = ta.CDLGRAVESTONEDOJI(open, high, low, close)
            return(integer)

        if x == "CDLHAMMER":
            #CDLHAMMER - Hammer
            integer = ta.CDLHAMMER(open, high, low, close)
            return(integer)

        if x == "CDLHANGINGMAN":
            #CDLHANGINGMAN - Hanging Man
            integer = ta.CDLHANGINGMAN(open, high, low, close)
            return(integer)

        if x == "CDLHARAMI":
            #CDLHARAMI - Harami Pattern
            integer = ta.CDLHARAMI(open, high, low, close)
            return(integer)

        if x == "CDLHARAMICROSS":
            #CDLHARAMICROSS - Harami Cross Pattern
            integer = ta.CDLHARAMICROSS(open, high, low, close)
            return(integer)

        if x == "CDLHIGHWAVE":
            #CDLHIGHWAVE - High-Wave Candle
            integer = ta.CDLHIGHWAVE(open, high, low, close)
            return(integer)

        if x == "CDLHIKKAKE":
            #CDLHIKKAKE - Hikkake Pattern
            integer = ta.CDLHIKKAKE(open, high, low, close)
            return(integer)

        if x == "CDLHIKKAKEMOD":
            #CDLHIKKAKEMOD - Modified Hikkake Pattern
            integer = ta.CDLHIKKAKEMOD(open, high, low, close)
            return(integer)

        if x == "CDLHOMINGPIGEON":
            #CDLHOMINGPIGEON - Homing Pigeon
            integer = ta.CDLHOMINGPIGEON(open, high, low, close)
            return(integer)

        if x == "CDLIDENTICAL3CROWS":
            #CDLIDENTICAL3CROWS - Identical Three Crows
            integer = ta.CDLIDENTICAL3CROWS(open, high, low, close)
            return(integer)

        if x == "CDLINNECK":
            #CDLINNECK - In-Neck Pattern
            integer = ta.CDLINNECK(open, high, low, close)
            return(integer)

        if x == "CDLINVERTEDHAMMER":
            #CDLINVERTEDHAMMER - Inverted Hammer
            integer = ta.CDLINVERTEDHAMMER(open, high, low, close)
            return(integer)

        if x == "CDLKICKING":
            #CDLKICKING - Kicking
            integer = ta.CDLKICKING(open, high, low, close)
            return(integer)

        if x == "CDLKICKINGBYLENGTH":
            #CDLKICKINGBYLENGTH - Kicking - bull/bear determined by the longer marubozu
            integer = ta.CDLKICKINGBYLENGTH(open, high, low, close)
            return(integer)

        if x == "CDLLADDERBOTTOM":
            #CDLLADDERBOTTOM - Ladder Bottom
            integer = ta.CDLLADDERBOTTOM(open, high, low, close)
            return(integer)

        if x == "CDLLONGLEGGEDDOJI":
            #CDLLONGLEGGEDDOJI - Long Legged Doji
            integer = ta.CDLLONGLEGGEDDOJI(open, high, low, close)
            return(integer)

        if x == "CDLLONGLINE":
            #CDLLONGLINE - Long Line Candle
            integer = ta.CDLLONGLINE(open, high, low, close)
            return(integer)

        if x == "CDLMARUBOZU":
            #CDLMARUBOZU - Marubozu
            integer = ta.CDLMARUBOZU(open, high, low, close)
            return(integer)

        if x == "CDLMATCHINGLOW":
            #CDLMATCHINGLOW - Matching Low
            integer = ta.CDLMATCHINGLOW(open, high, low, close)
            return(integer)

        if x == "CDLMATHOLD":
            #CDLMATHOLD - Mat Hold
            integer = ta.CDLMATHOLD(open, high, low, close, penetration=0)
            return(integer)

        if x == "CDLMORNINGDOJISTAR":
            #CDLMORNINGDOJISTAR - Morning Doji Star
            integer = ta.CDLMORNINGDOJISTAR(open, high, low, close, penetration=0)
            return(integer)

        if x == "CDLMORNINGSTAR":
            #CDLMORNINGSTAR - Morning Star
            integer = ta.CDLMORNINGSTAR(open, high, low, close, penetration=0)
            return(integer)

        if x == "CDLONNECK":
            #CDLONNECK - On-Neck Pattern
            integer = ta.CDLONNECK(open, high, low, close)
            return(integer)

        if x == "CDLPIERCING":
            #CDLPIERCING - Piercing Pattern
            integer = ta.CDLPIERCING(open, high, low, close)
            return(integer)

        if x == "CDLRICKSHAWMAN":
            #CDLRICKSHAWMAN - Rickshaw Man
            integer = ta.CDLRICKSHAWMAN(open, high, low, close)
            return(integer)

        if x == "CDLRISEFALL3METHODS":
            #CDLRISEFALL3METHODS - Rising/Falling Three Methods
            integer = ta.CDLRISEFALL3METHODS(open, high, low, close)
            return(integer)

        if x == "CDLSEPARATINGLINES":
            #CDLSEPARATINGLINES - Separating Lines
            integer = ta.CDLSEPARATINGLINES(open, high, low, close)
            return(integer)

        if x == "CDLSHOOTINGSTAR":
            #CDLSHOOTINGSTAR - Shooting Star
            integer = ta.CDLSHOOTINGSTAR(open, high, low, close)
            return(integer)

        if x == "CDLSHORTLINE":
            #CDLSHORTLINE - Short Line Candle
            integer = ta.CDLSHORTLINE(open, high, low, close)

        if x == "CDLSPINNINGTOP":
            #CDLSPINNINGTOP - Spinning Top
            integer = ta.CDLSPINNINGTOP(open, high, low, close)
            return(integer)

        if x == "CDLSTALLEDPATTERN":
            #CDLSTALLEDPATTERN - Stalled Pattern
            integer = ta.CDLSTALLEDPATTERN(open, high, low, close)
            return(integer)

        if x == "CDLSTICKSANDWICH":
            #CDLSTICKSANDWICH - Stick Sandwich
            integer = ta.CDLSTICKSANDWICH(open, high, low, close)
            return(integer)

        if x == "CDLTAKURI":
            #CDLTAKURI - Takuri (Dragonfly Doji with very long lower shadow)
            integer = ta.CDLTAKURI(open, high, low, close)
            return(integer)

        if x == "CDLTASUKIGAP":
            #CDLTASUKIGAP - Tasuki Gap
            integer = ta.CDLTASUKIGAP(open, high, low, close)
            return(integer)

        if x == "CDLTHRUSTING":
            #CDLTHRUSTING - Thrusting Pattern
            integer = ta.CDLTHRUSTING(open, high, low, close)
            return(integer)

        if x == "CDLTRISTAR":
            #CDLTRISTAR - Tristar Pattern
            integer = ta.CDLTRISTAR(open, high, low, close)
            return(integer)

        if x == "CDLUNIQUE3RIVER":
            #CDLUNIQUE3RIVER - Unique 3 River
            integer = ta.CDLUNIQUE3RIVER(open, high, low, close)
            return(integer)

        if x == "CDLUPSIDEGAP2CROWS":
            #CDLUPSIDEGAP2CROWS - Upside Gap Two Crows
            integer = ta.CDLUPSIDEGAP2CROWS(open, high, low, close)
            return(integer)

        if x == "CDLXSIDEGAP3METHODS":
            #CDLXSIDEGAP3METHODS - Upside/Downside Gap Three Methods
            integer = ta.CDLXSIDEGAP3METHODS(open, high, low, close)
            return(integer)

        else:
            real = "No coverage or wrong option selected"
            return real


    #Cycle Indicator Functions
    elif major == "cycle":
            
        if x =="HT_DCPERIOD":
            #HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period
            #NOTE: The HT_DCPERIOD function has an unstable period.
            real = ta.HT_DCPERIOD(close)
            return(real)
        
        if x =="HT_DCPHASE":
            #HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase
            #NOTE: The HT_DCPHASE function has an unstable period.
            real = ta.HT_DCPHASE(close)
            return(real)

        if x =="HT_PHASOR":
            #HT_PHASOR - Hilbert Transform - Phasor Components
            #NOTE: The HT_PHASOR function has an unstable period.
            inphase, quadrature = ta.HT_PHASOR(close)
            return(inphase, quadrature)

        if x =="HT_SINE":
            #HT_SINE - Hilbert Transform - SineWave
            #NOTE: The HT_SINE function has an unstable period.
            sine, leadsine = ta.HT_SINE(close)
            return(sine, leadsine)

        if x =="HT_TRENDMODE":
            #HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode
            #NOTE: The HT_TRENDMODE function has an unstable period.
            integer = ta.HT_TRENDMODE(close)
            return(integer)

        else:
            real = "No coverage or wrong option selected"
            return real


    #Price Transform Functions
    elif major == "price":

        if x =="AVGPRICE":
            #AVGPRICE - Average Price
            real = ta.AVGPRICE(open, high, low, close)
            return(real)

        if x =="MEDPRICE":
            #MEDPRICE - Median Price
            real = ta.MEDPRICE(high, low)
            return(real)

        if x =="TYPPRICE":
            #TYPPRICE - Typical Price
            real = ta.TYPPRICE(high, low, close)
            return(real)

        if x =="WCLPRICE":
            #WCLPRICE - Weighted Close Price
            real = ta.WCLPRICE(high, low, close)
            return(real)

        else:
            real = "No coverage or wrong option selected"
            return real


'''
#Statistic Functions

#BETA - Beta
real = BETA(high, low, timeperiod=5)

#CORREL - Pearson's Correlation Coefficient (r)
real = CORREL(high, low, timeperiod=30)

#LINEARREG - Linear Regression
real = LINEARREG(close, timeperiod=14)

#LINEARREG_ANGLE - Linear Regression Angle
real = LINEARREG_ANGLE(close, timeperiod=14)

LINEARREG_INTERCEPT - Linear Regression Intercept
real = LINEARREG_INTERCEPT(close, timeperiod=14)

LINEARREG_SLOPE - Linear Regression Slope
real = LINEARREG_SLOPE(close, timeperiod=14)

STDDEV - Standard Deviation
real = STDDEV(close, timeperiod=5, nbdev=1)

TSF - Time Series Forecast
real = TSF(close, timeperiod=14)

VAR - Variance
real = VAR(close, timeperiod=5, nbdev=1)

Math Transform Functions

ACOS - Vector Trigonometric ACos
real = ACOS(close)

ASIN - Vector Trigonometric ASin
real = ASIN(close)

ATAN - Vector Trigonometric ATan
real = ATAN(close)

CEIL - Vector Ceil
real = CEIL(close)

COS - Vector Trigonometric Cos
real = COS(close)

COSH - Vector Trigonometric Cosh
real = COSH(close)

EXP - Vector Arithmetic Exp
real = EXP(close)

FLOOR - Vector Floor
real = FLOOR(close)

LN - Vector Log Natural
real = LN(close)

LOG10 - Vector Log10
real = LOG10(close)

SIN - Vector Trigonometric Sin
real = SIN(close)

SINH - Vector Trigonometric Sinh
real = SINH(close)

SQRT - Vector Square Root
real = SQRT(close)

TAN - Vector Trigonometric Tan
real = TAN(close)

TANH - Vector Trigonometric Tanh
real = TANH(close)


Math Operator Functions

ADD - Vector Arithmetic Add
real = ADD(high, low)

DIV - Vector Arithmetic Div
real = DIV(high, low)

MAX - Highest value over a specified period
real = MAX(close, timeperiod=30)

MAXINDEX - Index of highest value over a specified period
integer = MAXINDEX(close, timeperiod=30)

MIN - Lowest value over a specified period
real = MIN(close, timeperiod=30)

MININDEX - Index of lowest value over a specified period
integer = MININDEX(close, timeperiod=30)

MINMAX - Lowest and highest values over a specified period
min, max = MINMAX(close, timeperiod=30)

MINMAXINDEX - Indexes of lowest and highest values over a specified period
minidx, maxidx = MINMAXINDEX(close, timeperiod=30)

MULT - Vector Arithmetic Mult
real = MULT(high, low)

SUB - Vector Arithmetic Substraction
real = SUB(high, low)

SUM - Summation
real = SUM(close, timeperiod=30)


Learn more about the Variance at tadoc.org.

'''