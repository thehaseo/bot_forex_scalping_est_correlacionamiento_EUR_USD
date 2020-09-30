import time
import fxcmpy
from ExtraccionDatosfxcm import Extraccionfxcm

def calcular_rango_sop_res(ohlc, rango_velas):
    resistencia_mayor = ohlc["h"].rolling(rango_velas).max().dropna()
    resistencia_menor = ohlc["c"].rolling(rango_velas).max().dropna()
    soporte_menor = ohlc["l"].rolling(rango_velas).min().dropna()
    soporte_mayor = ohlc["c"].rolling(rango_velas).min().dropna()
    resistencia_punto_mayor = resistencia_mayor.iloc[-1]
    resistencia_punto_menor = resistencia_menor.iloc[-1]
    for data in range(-rango_velas, 0):
        precio_h = ohlc['h'].iloc[data]
        precio_o = ohlc['o'].iloc[data]
        precio_c = ohlc['c'].iloc[data]
        if precio_h > resistencia_punto_menor > precio_c:
            if precio_c >= precio_o:
                resistencia_punto_menor = precio_c
            elif precio_c < precio_o < resistencia_punto_menor:
                resistencia_punto_menor = precio_o
    soporte_punto_menor = soporte_menor.iloc[-1]
    soporte_punto_mayor = soporte_mayor.iloc[-1]
    for data in range(-rango_velas, 0):
        precio_l = ohlc['l'].iloc[data]
        precio_o = ohlc['o'].iloc[data]
        precio_c = ohlc['c'].iloc[data]
        if precio_l < soporte_punto_mayor < precio_c:
            if precio_c <= precio_o:
                soporte_punto_mayor = precio_c
            elif precio_c > precio_o > soporte_punto_mayor:
                soporte_punto_mayor = precio_o
    return resistencia_punto_mayor, resistencia_punto_menor, soporte_punto_menor, soporte_punto_mayor


def actualizar_datos(datos_5min, datos_30min, divisa, client):
    try:
        if ((int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[15:16])) == 1 or (
                int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[15:16])) == 6) and \
                (datos_5min.iloc[-1].name[
                 14:16] != f"{int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 360))[14:16]):02}"):
            try:
                Extraccionfxcm(client, 500, 'm5', divisa)
            except Exception as e:
                print(f"excepcion {e}: {type(e)}")
                client = fxcmpy.fxcmpy(config_file='fxcm.cfg')
        # actualizacion de datos 30m
        if ((int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[14:16])) == 31 or
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[14:16]) == "01" and \
                (datos_30min.iloc[-1].name[
                 14:16] != f"{int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 1860))[14:16]):02}"):
            try:
                Extraccionfxcm(client, 250, 'm30', divisa)
            except Exception as e:
                print(f"excepcion {e}: {type(e)}")
                client = fxcmpy.fxcmpy(config_file='fxcm.cfg')
    except Exception as e:
        print(f"excepcion {e}: {type(e)}")
        print("hubo error en lectura de datos csv")
