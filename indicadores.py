import numpy as np
import pandas as pd
import statsmodels.api as sm


def slope(ser, n):
    "function to calculate the slope of n consecutive points on a plot"
    slopes = [i*0 for i in range(n-1)]
    for i in range(n,len(ser)+1):
        y = ser[i-n:i]
        x = np.array(range(n))
        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled, x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)


def MACD(DF, periodo_rapido=12, periodo_lento=26, periodo_señal=9):
    """function to calculate MACD
       typical values a = 12; b =26, c =9"""
    df = pd.DataFrame()
    df["MA_Fast"] = DF['c'].ewm(span=periodo_rapido, min_periods=periodo_rapido).mean()
    df["MA_Slow"] = DF['c'].ewm(span=periodo_lento, min_periods=periodo_lento).mean()
    df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
    df["Signal"] = df["MACD"].ewm(span=periodo_señal, min_periods=periodo_señal).mean()
    df["historigrama"] = df["MACD"] - df["Signal"]
    df.dropna(inplace=True)
    return df


def boll_bnd(ohlc, periodos=20):
    "function to calculate Bollinger Band"
    df = pd.DataFrame()
    df["MA"] = ohlc['c'].rolling(periodos).mean()
    df["BB_up"] = df["MA"] + 2 * ohlc['c'].rolling(periodos).std(ddof=0)  # ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] - 2 * ohlc['c'].rolling(periodos).std(ddof=0)  # ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df


def ATR(DF, periodo: int = 14):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df.rename(columns={"time": "date", "h": "high", "l": "low", "o": "open", "c": "close"}, inplace=True)
    df['H-L'] = abs(df['high'] - df['low'])
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(periodo).mean()
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df2


def keltner_channel(DF, periodo: int = 20, multiplicador: float = 2.0):
    df = DF.copy()
    middle = pd.Series(df['c'].ewm(span=periodo, min_periods=periodo).mean(), name="kc_middle")
    up = pd.Series(middle + (multiplicador * ATR(df, periodo=20)["ATR"]), name="kc_up")
    down = pd.Series(middle - (multiplicador * ATR(df, periodo=20)["ATR"]), name="kc_dn")
    channel = pd.concat([up, down, middle], axis=1)
    channel.dropna(inplace=True)
    return channel


def squeeze_momentum(DF, periodo: int=14):
    df = DF.copy()
    bollinger = boll_bnd(df)
    keltner = keltner_channel(df)
    comb = pd.concat([bollinger, keltner], axis=1)
    momentum = (comb["BB_up"] - comb["kc_up"]) + (comb["kc_dn"] - comb["BB_dn"])
    return momentum
