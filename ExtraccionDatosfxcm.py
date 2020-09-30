import pandas as pd
import sys
import fxcmpy

def Extraccionfxcm(client, numero_de_velas, timeframe, par_de_divisas):
    try:
        numero_de_velas = numero_de_velas
        timeframe = timeframe
        par_de_divisas = par_de_divisas
        # S30, minutes M1 - M30, hours H1 - H12, days D, weeks W or months M
        if client.is_connected():
            data = client.get_candles(par_de_divisas, period=timeframe, number=numero_de_velas)
        else:
            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
            data = client.get_candles(par_de_divisas, period=timeframe, number=numero_de_velas)
        data.apply(pd.to_numeric)
        ohlc_df = pd.DataFrame()
        ohlc_df["o"] = (data.loc[:, "bidopen"] + data.loc[:, "askhigh"]) / 2
        ohlc_df["h"] = (data.loc[:, "bidhigh"] + data.loc[:, "askhigh"]) / 2
        ohlc_df["l"] = (data.loc[:, "bidlow"] + data.loc[:, "asklow"]) / 2
        ohlc_df["c"] = (data.loc[:, "bidclose"] + data.loc[:, "askclose"]) / 2
        ohlc_df["v"] = (data.loc[:, "tickqty"])
        ohlc_df.drop(ohlc_df.tail(1).index, inplace=True)
        print(ohlc_df.iloc[-1])
        pd.DataFrame.to_csv(ohlc_df, f"datos_{timeframe.replace('m', 'M')}_{par_de_divisas.replace('/', '_')}.csv")
    except Exception as e:
        print("excepcion", e, "de  tipo", type(e), "intentando resetear modulos")
        return "reset"
