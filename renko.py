# =============================================================================
# Import OHLCV data and transform it to Renko
# Author : Mayank Rasu (http://rasuquant.com/wp/)

# Please report bug/issues in the Q&A section
# =============================================================================

# Import necesary libraries
from stocktrends import Renko
import pandas as pd
import pickle
################################PLEASE READ ME####################################
# Stocktrends' author has renamed get_bricks() function to get_ohlc_data()
# therefore you may get error when trying to run line 43 below
# if that is the case please comment out line 43 and remove # sign from line 44 and rerun
##################################################################################

# Download historical data for required stocks


def ATR(DF, periodo):
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


def check_renko_uptrend(renko_df):
    contador_velas_uptrend = 0
    contador_velas_downtrend = 0
    for vela in range(1, len(renko_df.index)):
        if renko_df["uptrend"].iloc[-vela]:
            if contador_velas_downtrend >= 4:
                return False, contador_velas_downtrend, renko_df.iloc[-(vela - 3)].date
            elif 3 >= contador_velas_downtrend >= 1:
                return False, contador_velas_downtrend, renko_df.iloc[-(vela - 1)].date
            contador_velas_uptrend += 1
        elif not renko_df["uptrend"].iloc[-vela]:
            if contador_velas_uptrend >= 4:
                return True, contador_velas_uptrend, renko_df.iloc[-(vela - 3)].date
            elif 3 >= contador_velas_uptrend >= 1:
                return True, contador_velas_uptrend, renko_df.iloc[-(vela - 1)].date
            contador_velas_downtrend += 1


def renko_DF(DF):
    "function to convert ohlc data into renko bricks"
    df = DF.copy()
    df.reset_index(inplace=True)
    df.rename(columns={"time": "date", "h": "high", "l": "low", "o": "open", "c": "close"}, inplace=True)
    df2 = Renko(df)
    df2.brick_size = round(ATR(df, 120)["ATR"].iloc[-1], 4)
    renko_df = df2.get_ohlc_data()  # if using older version of the library please use get_bricks() instead
    renko_df.drop_duplicates(subset="date", keep="last", inplace=True)
    pd.DataFrame.to_csv(renko_df, f"renko.csv")
    valor = open("ultimo_valor_renko", "wb")
    pickle.dump(renko_df["uptrend"].iloc[-1], valor)
    valor.close()
    return renko_df
