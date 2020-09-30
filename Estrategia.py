from RSI import RSI
from SeguimientoEjecucion import seguimiento_y_ejecucion
import pandas as pd
from ExtraccionDatosfxcm import Extraccionfxcm
import time

# verifica si la vela dada es una vela decisisva
def setenta_por_ciento(ohlc_vela, alcista_o_bajista: str) -> bool:
    if alcista_o_bajista == "alcista":
        if ohlc_vela['o'] < ohlc_vela['c']:
            return ((((ohlc_vela['h'] - ohlc_vela['o']) * 70) / 100) <= (ohlc_vela['c'] - ohlc_vela['o']) and
                    (ohlc_vela['h'] - ohlc_vela['o']) > (ohlc_vela['o'] - ohlc_vela['l']))
        else:
            return False
    elif alcista_o_bajista == "bajista":
        if ohlc_vela['o'] > ohlc_vela['c']:
            return ((((ohlc_vela['l'] - ohlc_vela['o']) * 70) / 100) >= (ohlc_vela['c'] - ohlc_vela['o']) and
                    (ohlc_vela['h'] - ohlc_vela['o']) < (ohlc_vela['o'] - ohlc_vela['l']))
        else:
            return False


# Verifica si se ha cumplido la condición de una vela decisiva en el rango de velas dado
def check_flags_condition(ohlc, alcista_o_bajista: str, numero_de_velas: int) -> bool:
    numero_de_velas = numero_de_velas
    if numero_de_velas == 0:
        return False
    if alcista_o_bajista == "alcista":
        for vela in range(1, numero_de_velas):
            if setenta_por_ciento(ohlc.iloc[-vela], "alcista"):
                return True
        return False
    elif alcista_o_bajista == "bajista":
        for vela in range(1, numero_de_velas):
            if setenta_por_ciento(ohlc.iloc[-vela], "bajista"):
                return True
        return False


# Retorna el rango de velas a tomar en cuenta para verificar si se ha cumplido la condición de una vela decisiva
# en el rango de velas retornado
#
# ohlc: ohlc de todas las velas del marco de tiempo correspondiente
# index_name: el nombre del índice a detenerse para calcular cuantas velas se han recorrido hasta ese punto
def calcular_numero_velas(ohlc, index_name) -> int:
    for i in range(1, len(ohlc)):
        if ohlc.iloc[-i].name == index_name:
            return i


def analisis_y_estrategia(divisa, client, timeout, numero_de_noticias, hora_noticias):
        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
        rsi_eur_usd = RSI(datos_eur_usd)
        print("rsi eurusd:", rsi_eur_usd.iloc[-1])
        if rsi_eur_usd.iloc[-1] > 70.0:
            while time.time() <= timeout:
                Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                Extraccionfxcm(client, 500, 'm5', "GBP/USD")
                Extraccionfxcm(client, 500, 'm5', "NZD/USD")
                Extraccionfxcm(client, 500, 'm5', "EUR/CHF")
                Extraccionfxcm(client, 500, 'm5', "EUR/CAD")
                datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                datos_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv")
                datos_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv")
                datos_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv")
                datos_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv")
                rsi_eur_usd = RSI(datos_eur_usd)
                rsi_gbp_usd = RSI(datos_gbp_usd)
                rsi_nzd_usd = RSI(datos_nzd_usd)
                rsi_eur_chf = RSI(datos_eur_chf)
                rsi_eur_cad = RSI(datos_eur_cad)
                print("rsi nzdusd:", rsi_nzd_usd.iloc[-1], "gbpusd:", rsi_gbp_usd.iloc[-1], "eurchf:", rsi_eur_chf.iloc[-1],
                      "eurcad:", rsi_eur_cad.iloc[-1])
                if rsi_nzd_usd.iloc[-1] < 70.0 and rsi_gbp_usd.iloc[-1] < 70.0 and rsi_eur_chf.iloc[-1] < 70.0 and\
                        rsi_eur_cad.iloc[-1] < 70.0:
                    valor_return = seguimiento_y_ejecucion("bajista", client, divisa, None, numero_de_noticias, hora_noticias, timeout)
                    return valor_return
                elif rsi_nzd_usd.iloc[-1] > 70.0 and rsi_gbp_usd.iloc[-1] > 70.0 and rsi_eur_chf.iloc[-1] < 70.0 and\
                        rsi_eur_cad.iloc[-1] < 70.0:
                    valor_return = seguimiento_y_ejecucion("bajista", client, divisa, "USD", numero_de_noticias, hora_noticias, timeout)
                    return  valor_return
                elif rsi_nzd_usd.iloc[-1] < 70.0 and rsi_gbp_usd.iloc[-1] < 70.0 and rsi_eur_chf.iloc[-1] > 70.0 and\
                        rsi_eur_cad.iloc[-1] > 70.0:
                    valor_return = seguimiento_y_ejecucion("bajista", client, divisa, "EUR", numero_de_noticias, hora_noticias, timeout)
                    return valor_return
                elif rsi_eur_usd.iloc[-1] < 70.0:
                    break
                time.sleep(60)
        elif rsi_eur_usd.iloc[-1] < 30.0:
            while time.time() <= timeout:
                Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                Extraccionfxcm(client, 500, 'm5', "GBP/USD")
                Extraccionfxcm(client, 500, 'm5', "NZD/USD")
                Extraccionfxcm(client, 500, 'm5', "EUR/CHF")
                Extraccionfxcm(client, 500, 'm5', "EUR/CAD")
                datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                datos_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv")
                datos_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv")
                datos_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv")
                datos_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv")
                rsi_eur_usd = RSI(datos_eur_usd)
                rsi_gbp_usd = RSI(datos_gbp_usd)
                rsi_nzd_usd = RSI(datos_nzd_usd)
                rsi_eur_chf = RSI(datos_eur_chf)
                rsi_eur_cad = RSI(datos_eur_cad)
                print("rsi nzdusd:", rsi_nzd_usd.iloc[-1], "gbpusd:", rsi_gbp_usd.iloc[-1], "eurchf:",
                      rsi_eur_chf.iloc[-1],
                      "eurcad:", rsi_eur_cad.iloc[-1])
                if rsi_nzd_usd.iloc[-1] > 30.0 and rsi_gbp_usd.iloc[-1] > 30.0 and rsi_eur_chf.iloc[-1] > 30.0 and\
                        rsi_eur_cad.iloc[-1] > 30.0:
                    valor_return = seguimiento_y_ejecucion("alcista", client, divisa, None, numero_de_noticias, hora_noticias, timeout)
                    return valor_return
                elif rsi_nzd_usd.iloc[-1] < 30.0 and rsi_gbp_usd.iloc[-1] < 30.0 and rsi_eur_chf.iloc[-1] > 30.0 and\
                        rsi_eur_cad.iloc[-1] > 30.0:
                    valor_return = seguimiento_y_ejecucion("alcista", client, divisa, "USD", numero_de_noticias, hora_noticias, timeout)
                    return valor_return
                elif rsi_nzd_usd.iloc[-1] > 30.0 and rsi_gbp_usd.iloc[-1] > 30.0 and rsi_eur_chf.iloc[-1] < 30.0 and\
                        rsi_eur_cad.iloc[-1] < 30.0:
                    valor_return = seguimiento_y_ejecucion("alcista", client, divisa, "EUR", numero_de_noticias, hora_noticias, timeout)
                    return valor_return
                elif rsi_eur_usd.iloc[-1] > 30.0:
                    break
                time.sleep(60)


