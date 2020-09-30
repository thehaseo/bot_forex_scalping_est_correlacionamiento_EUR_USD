import pandas as pd
import time
from ExtraccionDatosfxcm import Extraccionfxcm
from Estrategia import analisis_y_estrategia
from importlib import reload
import fxcmpy
import sys


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


def reset_modules(client):
    try:
        a_del = []
        print("eliminando modulos")
        for module in sys.modules.keys():
            if "fxcm" in module:
                a_del.append(module)
        for module in a_del:
            del sys.modules[module]
    except Exception as e:
        print("error al eliminar modulos importados de fxcm")
    try:
        print("eliminando cliente")
        del client
    except Exception as e:
        print("error al borrar el cliente", e)
    import fxcmpy
    from ExtraccionDatosfxcm import Extraccionfxcm


def run(tiempo_de_ejecucion_minutos, numero_noticias, horas_noticias):
    print("comenzando")
    timeout = time.time() + (tiempo_de_ejecucion_minutos * 60)
    divisa = "EUR/USD"
    client = fxcmpy.fxcmpy(config_file='fxcm.cfg')
    Extraccionfxcm(client, 500, 'm5', divisa)
    Extraccionfxcm(client, 250, 'm30', divisa)
    datos_5min = pd.read_csv(f"datos_M5_{divisa.replace('/', '_')}.csv", index_col="date")
    datos_30min = pd.read_csv(f"datos_M30_{divisa.replace('/', '_')}.csv", index_col="date")
    while time.time() <= timeout:
        if numero_noticias == 1:
            if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                time.sleep(3600)
        elif numero_noticias == 2:
            if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                time.sleep(3600)
            elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[1]:
                time.sleep(3600)
        elif numero_noticias == 3:
            if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                time.sleep(3600)
            elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[1]:
                time.sleep(3600)
            elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[2]:
                time.sleep(3600)
            # actualizacion de datos 1m
            # if (f"{(int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[14:16]) - 1):02}" != \
            #         datos_1min.iloc[-1].name[14:16]):
            #     try:
            #         ExtraccionOanda(client, 500, 'M1', divisa)
            #     except Exception as e:
            #         print(f"excepcion {e}: {type(e)}")
            #         client = oandapyV20.API(
            #             access_token="e51f5c80499fd16ae7e9ff6676b3c53f-3ac97247f6df3ad7b2b3731a4b1c2dc3",
            #             environment="practice")
            #     datos_1min = pd.read_csv("datos_M1_EUR_USD.csv", index_col="time")
            #     resistencia_punto_mayor_1m, resistencia_punto_menor_1m, soporte_punto_menor_1m, soporte_punto_mayor_1m = \
            #         calcular_rango_sop_res(datos_1min, 120)
            # actualizacion de datos 5m
        if ((int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[15:16])) == 1 or (
                int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[15:16])) == 6) and \
                (datos_5min.iloc[-1].name[
                 14:16] != f"{int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 360))[14:16]):02}"):
            try:
                valor_ext = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                if valor_ext == "reset":
                    while not client.is_connected():
                        reset_modules(client)
                        client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        time.sleep(30)
            except Exception as e:
                print(f"excepcion {e}: {type(e)}")
        # actualizacion de datos 30m
        #if ((int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[14:16])) == 31 or
         #   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[14:16]) == "01" and \
          #      (datos_30min.iloc[-1].name[
           #      14:16] != f"{int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 1860))[14:16]):02}"):
            #try:
             #   Extraccionfxcm(client, 250, 'm30', "EUR/USD")
  #          except Exception as e:
   #             print(f"excepcion {e}: {type(e)}")
    #            client = fxcmpy.fxcmpy(config_file='fxcm.cfg')
        valor_return = analisis_y_estrategia(divisa, client, timeout, numero_noticias, horas_noticias)
        print(valor_return)
        if valor_return == "reset":
            while not client.is_connected():
                reset_modules(client)
                client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                time.sleep(30)
        time.sleep(30)


if __name__ == "__main__":
    mes = input("introduzca el mes de inicio: ")
    dia = input("introduzca el dia de inicio: ")
    hora = input("introduzca la hora de inicio (militar): ")
    minuto = input("introduzca el minuto de inicio: ")
    tiempo = int(input("introduzca el tiempo de ejecucion en minutos: "))
    numero_noticias = int(input("Introduzca el numero de noticias: "))
    noticia1 = 0
    noticia2 = 0
    noticia3 = 0
    if numero_noticias == 0:
        pass
    elif numero_noticias == 1:
        hora_noticia = input("Introduzca la hora de la noticia 30 minutos antes: ")
        minuto_noticia = input("Introduzca el minuto de la noticia 30 minutos antes: ")
        noticia1 = f'2020-{mes}-{dia} {hora_noticia}:{minuto_noticia}'
    elif numero_noticias == 2:
        hora_noticia1 = input("Introduzca la hora de la primera noticia 30 minutos antes: ")
        minuto_noticia1 = input("Introduzca el minuto de la primera noticia 30 minutos antes: ")
        noticia1 = f'2020-{mes}-{dia} {hora_noticia1}:{minuto_noticia1}'
        hora_noticia2 = input("Introduzca la hora de la segunda noticia 30 minutos antes: ")
        minuto_noticia2 = input("Introduzca el minuto de la segunda noticia 30 minutos antes: ")
        noticia2 = f'2020-{mes}-{dia} {hora_noticia2}:{minuto_noticia2}'
    elif numero_noticias == 3:
        hora_noticia1 = input("Introduzca la hora de la primera noticia 30 minutos antes: ")
        minuto_noticia1 = input("Introduzca el minuto de la noticia 30 minutos antes: ")
        noticia1 = f'2020-{mes}-{dia} {hora_noticia1}:{minuto_noticia1}'
        hora_noticia2 = input("Introduzca la hora de la segunda noticia 30 minutos antes: ")
        minuto_noticia2 = input("Introduzca el minuto de la segunda noticia 30 minutos antes: ")
        noticia2 = f'2020-{mes}-{dia} {hora_noticia2}:{minuto_noticia2}'
        hora_noticia3 = input("Introduzca la hora de la tercera noticia 30 minutos antes: ")
        minuto_noticia3 = input("Introduzca el minuto de la tercera noticia 30 minutos antes: ")
        noticia3 = f'2020-{mes}-{dia} {hora_noticia1}:{minuto_noticia1}'
    while time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) != f'2020-{mes}-{dia} {hora}:{minuto}:00':
        pass
    run(tiempo, numero_noticias, (noticia2, noticia2, noticia3))
