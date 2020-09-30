import pandas as pd
from indicadores import ATR
from RSI import RSI
import time
from ExtraccionDatosfxcm import Extraccionfxcm
from importlib import reload
import sys
import fxcmpy


def seguimiento_y_ejecucion(alcista_o_bajista: str, client, divisa: str, divisa_predominante,
                            numero_de_noticias, hora_noticias, timeout):
    if divisa_predominante is None:
        print("haciendo seguimiento al EUR/USD sin divisa de importancia")
        while time.time() < timeout:
            valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
            if valor_extraccion == "reset":
                reload(fxcmpy)
                reload(Extraccionfxcm)
                client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
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
            print("rsi eurusd:", rsi_eur_usd.iloc[-1], "rsi nzdusd:", rsi_nzd_usd.iloc[-1], "gbpusd:", rsi_gbp_usd.iloc[-1], "eurchf:", rsi_eur_chf.iloc[-1],
                  "eurcad:", rsi_eur_cad.iloc[-1])
            if alcista_o_bajista == "bajista":
                if rsi_eur_usd.iloc[-1] < 70.0 and rsi_gbp_usd.iloc[-1] < 70.0 and rsi_nzd_usd.iloc[-1] < 70.0 \
                        and rsi_eur_chf.iloc[-1] < 70.0 and rsi_eur_cad.iloc[-1] < 70.0:
                    crear_operacion(divisa, alcista_o_bajista, client, datos_eur_usd, numero_de_noticias,
                                    hora_noticias)
                    print("se sale del seguimiento")
                    return
                elif rsi_eur_usd.iloc[-1] < 70.0 and (rsi_gbp_usd.iloc[-1] > 70.0 or rsi_nzd_usd.iloc[-1] > 70.0
                                                      or rsi_eur_chf.iloc[-1] > 70.0 or rsi_eur_cad.iloc[-1] > 70.0):
                    print("Se sale del seguimiento")
                    return
            elif alcista_o_bajista == "alcista":
                if rsi_eur_usd.iloc[-1] > 30.0 and rsi_gbp_usd.iloc[-1] > 30.0 and rsi_nzd_usd.iloc[-1] > 30.0 \
                        and rsi_eur_chf.iloc[-1] > 30.0 and rsi_eur_cad.iloc[-1] > 30.0:
                    crear_operacion(divisa, alcista_o_bajista, client, datos_eur_usd, numero_de_noticias,
                                    hora_noticias)
                    print("se sale del seguimiento")
                    return
                elif rsi_eur_usd.iloc[-1] > 30.0 and (rsi_gbp_usd.iloc[-1] < 30.0 or rsi_nzd_usd.iloc[-1] < 30.0
                                                      or rsi_eur_chf.iloc[-1] < 30.0 or rsi_eur_cad.iloc[-1] < 30.0):
                    print("Se sale del seguimiento")
                    return
            time.sleep(60)
    elif divisa_predominante == "USD":
        print("Haciendo seguimiento a divisa de importancia USD")
        while time.time() < timeout:
            valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
            if valor_extraccion == "reset":
                reload(fxcmpy)
                reload(Extraccionfxcm)
                client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
            Extraccionfxcm(client, 500, 'm5', "GBP/USD")
            Extraccionfxcm(client, 500, 'm5', "NZD/USD")
            datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
            datos_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv")
            datos_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv")
            rsi_eur_usd = RSI(datos_eur_usd)
            rsi_gbp_usd = RSI(datos_gbp_usd)
            rsi_nzd_usd = RSI(datos_nzd_usd)
            print("rsi nzdusd:", rsi_nzd_usd.iloc[-1], "gbpusd:", rsi_gbp_usd.iloc[-1])
            if alcista_o_bajista == "bajista":
                if rsi_eur_usd.iloc[-1] > 70.0 and rsi_gbp_usd.iloc[-1] < 70.0 and rsi_nzd_usd.iloc[-1] < 70.0:
                    print("seguimiento para abrir operacion en eurusd a la baja")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "GBP/USD")
                        Extraccionfxcm(client, 500, 'm5', "NZD/USD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv")
                        datos_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_gbp_usd = RSI(datos_gbp_usd)
                        rsi_nzd_usd = RSI(datos_nzd_usd)
                        print("rsi eurusd:", rsi_eur_usd.iloc[-1], "rsi nzdusd:", rsi_nzd_usd.iloc[-1],
                              "gbpusd:", rsi_gbp_usd.iloc[-1])
                        if rsi_gbp_usd.iloc[-1] > 70.0 or rsi_nzd_usd.iloc[-1] > 70.0:
                            break
                        elif rsi_eur_usd.iloc[-1] < 70.0:
                            crear_operacion(divisa, alcista_o_bajista, client, datos_eur_usd, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] < 70.0 and rsi_gbp_usd.iloc[-1] > 70.0 and rsi_nzd_usd.iloc[-1] < 70.0:
                    print("seguimiento para abrir operacion en gbpusd a la baja")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "GBP/USD")
                        Extraccionfxcm(client, 500, 'm5', "NZD/USD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv")
                        datos_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_gbp_usd = RSI(datos_gbp_usd)
                        rsi_nzd_usd = RSI(datos_nzd_usd)
                        print("rsi eurusd:", rsi_eur_usd.iloc[-1], "rsi nzdusd:", rsi_nzd_usd.iloc[-1],
                              "gbpusd:", rsi_gbp_usd.iloc[-1])
                        if rsi_eur_usd.iloc[-1] > 70.0 or rsi_nzd_usd.iloc[-1] > 70.0:
                            break
                        elif rsi_gbp_usd.iloc[-1] < 70.0:
                            crear_operacion("GBP/USD", alcista_o_bajista, client, datos_gbp_usd, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] < 70.0 and rsi_gbp_usd.iloc[-1] < 70.0 and rsi_nzd_usd.iloc[-1] > 70.0:
                    print("seguimiento para abrir operacion en nzdusd a la baja")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "GBP/USD")
                        Extraccionfxcm(client, 500, 'm5', "NZD/USD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv")
                        datos_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_gbp_usd = RSI(datos_gbp_usd)
                        rsi_nzd_usd = RSI(datos_nzd_usd)
                        print("rsi eurusd:", rsi_eur_usd.iloc[-1], "rsi nzdusd:", rsi_nzd_usd.iloc[-1],
                              "gbpusd:", rsi_gbp_usd.iloc[-1])
                        if rsi_eur_usd.iloc[-1] > 70.0 or rsi_gbp_usd.iloc[-1] > 70.0:
                            break
                        elif rsi_nzd_usd.iloc[-1] < 70.0:
                            crear_operacion("NZD/USD", alcista_o_bajista, client, datos_nzd_usd, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] < 70.0 and rsi_gbp_usd.iloc[-1] < 70.0 and rsi_nzd_usd.iloc[-1] < 70.0:
                    print("todos los pares salieron de la zona de sobrecompra al mismo tiempo")
                    return
            if alcista_o_bajista == "alcista":
                if rsi_eur_usd.iloc[-1] < 30.0 and rsi_gbp_usd.iloc[-1] > 30.0 and rsi_nzd_usd.iloc[-1] > 30.0:
                    print("haciendo seguimiento para abrir operacion en eurusd al alza")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "GBP/USD")
                        Extraccionfxcm(client, 500, 'm5', "NZD/USD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv")
                        datos_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_gbp_usd = RSI(datos_gbp_usd)
                        rsi_nzd_usd = RSI(datos_nzd_usd)
                        print("rsi eurusd:", rsi_eur_usd.iloc[-1], "rsi nzdusd:", rsi_nzd_usd.iloc[-1],
                              "gbpusd:", rsi_gbp_usd.iloc[-1])
                        if rsi_gbp_usd.iloc[-1] < 30.0 or rsi_nzd_usd.iloc[-1] < 30.0:
                            break
                        elif rsi_eur_usd.iloc[-1] > 30.0:
                            crear_operacion(divisa, alcista_o_bajista, client, datos_eur_usd, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] > 30.0 and rsi_gbp_usd.iloc[-1] < 30.0 and rsi_nzd_usd.iloc[-1] > 30.0:
                    print("haciendo seguimiento para abrir operacion en gbpusd al alza")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "GBP/USD")
                        Extraccionfxcm(client, 500, 'm5', "NZD/USD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv")
                        datos_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_gbp_usd = RSI(datos_gbp_usd)
                        rsi_nzd_usd = RSI(datos_nzd_usd)
                        print("rsi eurusd:", rsi_eur_usd.iloc[-1], "rsi nzdusd:", rsi_nzd_usd.iloc[-1],
                              "gbpusd:", rsi_gbp_usd.iloc[-1])
                        if rsi_eur_usd.iloc[-1] < 30.0 or rsi_nzd_usd.iloc[-1] < 30.0:
                            break
                        elif rsi_gbp_usd.iloc[-1] > 30.0:
                            crear_operacion("GBP/USD", alcista_o_bajista, client, datos_gbp_usd, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] > 30.0 and rsi_gbp_usd.iloc[-1] > 70.0 and rsi_nzd_usd.iloc[-1] < 30.0:
                    print("haciendo seguimiento para abrir operacion en nzd al alza")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "GBP/USD")
                        Extraccionfxcm(client, 500, 'm5', "NZD/USD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv")
                        datos_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_gbp_usd = RSI(datos_gbp_usd)
                        rsi_nzd_usd = RSI(datos_nzd_usd)
                        print("rsi eurusd:", rsi_eur_usd.iloc[-1], "rsi nzdusd:", rsi_nzd_usd.iloc[-1],
                              "gbpusd:", rsi_gbp_usd.iloc[-1])
                        if rsi_eur_usd.iloc[-1] < 30.0 or rsi_gbp_usd.iloc[-1] < 30.0:
                            break
                        elif rsi_nzd_usd.iloc[-1] > 30.0:
                            crear_operacion("NZD/USD", alcista_o_bajista, client, datos_nzd_usd, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] > 30.0 and rsi_gbp_usd.iloc[-1] > 30.0 and rsi_nzd_usd.iloc[-1] > 30.0:
                    print("todos los pares salieron de la zona de sobreventa al mismo tiempo")
                    crear_operacion("EUR/USD", alcista_o_bajista, client, datos_nzd_usd, numero_de_noticias,
                                    hora_noticias)
                    return
            time.sleep(60)
    elif divisa_predominante == "EUR":
        print("Haciendo seguimiento a divisa de importancia EUR")
        while time.time() < timeout:
            valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
            if valor_extraccion == "reset":
                reload(fxcmpy)
                reload(Extraccionfxcm)
                client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
            Extraccionfxcm(client, 500, 'm5', "EUR/CHF")
            Extraccionfxcm(client, 500, 'm5', "EUR/CAD")
            datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
            datos_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv")
            datos_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv")
            rsi_eur_usd = RSI(datos_eur_usd)
            rsi_eur_chf = RSI(datos_eur_chf)
            rsi_eur_cad = RSI(datos_eur_cad)
            print("eurusd:", rsi_eur_usd.iloc[-1], "eurchf:", rsi_eur_chf.iloc[-1], "eurcad:", rsi_eur_cad.iloc[-1])
            if alcista_o_bajista == "bajista":
                if rsi_eur_usd.iloc[-1] > 70.0 and rsi_eur_chf.iloc[-1] < 70.0 and rsi_eur_cad.iloc[-1] < 70.0:
                    print("haciendo seguimiento para abrir operacion a la baja en eurusd")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CHF")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CAD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv")
                        datos_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_eur_chf = RSI(datos_eur_chf)
                        rsi_eur_cad = RSI(datos_eur_cad)
                        print("eurusd:", rsi_eur_usd.iloc[-1],"eurchf:", rsi_eur_chf.iloc[-1], "eurcad:", rsi_eur_cad.iloc[-1])
                        if rsi_eur_chf.iloc[-1] > 70.0 or rsi_eur_cad.iloc[-1] > 70.0:
                            break
                        elif rsi_eur_usd.iloc[-1] < 70.0:
                            crear_operacion(divisa, alcista_o_bajista, client, datos_eur_usd, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] < 70.0 and rsi_eur_chf.iloc[-1] > 70.0 and rsi_eur_cad.iloc[-1] < 70.0:
                    print("haciendo seguimiento para abrir operacion a la baja en eurchf")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CHF")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CAD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv")
                        datos_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_eur_chf = RSI(datos_eur_chf)
                        rsi_eur_cad = RSI(datos_eur_cad)
                        print("eurusd:", rsi_eur_usd.iloc[-1],"eurchf:", rsi_eur_chf.iloc[-1], "eurcad:", rsi_eur_cad.iloc[-1])
                        if rsi_eur_usd.iloc[-1] > 70.0 or rsi_eur_cad.iloc[-1] > 70.0:
                            break
                        elif rsi_eur_chf.iloc[-1] < 70.0:
                            crear_operacion("EUR/CHF", alcista_o_bajista, client, datos_eur_chf, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] < 70.0 and rsi_eur_chf.iloc[-1] < 70.0 and rsi_eur_cad.iloc[-1] > 70.0:
                    print("haciendo seguimniento para abrir operacion a la baja en eurcad")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CHF")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CAD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv")
                        datos_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_eur_chf = RSI(datos_eur_chf)
                        rsi_eur_cad = RSI(datos_eur_cad)
                        print("eurusd:", rsi_eur_usd.iloc[-1],"eurchf:", rsi_eur_chf.iloc[-1], "eurcad:", rsi_eur_cad.iloc[-1])
                        if rsi_eur_usd.iloc[-1] > 70.0 or rsi_eur_chf.iloc[-1] > 70.0:
                            break
                        elif rsi_eur_cad.iloc[-1] < 70.0:
                            crear_operacion("EUR/CAD", alcista_o_bajista, client, datos_eur_cad, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] < 70.0 and rsi_eur_chf.iloc[-1] < 70.0 and rsi_eur_cad.iloc[-1] < 70.0:
                    print("todos los pares salieron de la zona de sobrecompra al mismo tiempo")
                    return
            if alcista_o_bajista == "alcista":
                if rsi_eur_usd.iloc[-1] < 30.0 and rsi_eur_chf.iloc[-1] > 30.0 and rsi_eur_cad.iloc[-1] > 30.0:
                    print("haciendo seguimiento para abrir operacion al alza en eurusd")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CHF")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CAD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv")
                        datos_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_eur_chf = RSI(datos_eur_chf)
                        rsi_eur_cad = RSI(datos_eur_cad)
                        print("eurusd:", rsi_eur_usd.iloc[-1], "eurchf:", rsi_eur_chf.iloc[-1], "eurcad:",
                              rsi_eur_cad.iloc[-1])
                        if rsi_eur_chf.iloc[-1] < 30.0 or rsi_eur_cad.iloc[-1] < 30.0:
                            break
                        elif rsi_eur_usd.iloc[-1] > 30.0:
                            crear_operacion(divisa, alcista_o_bajista, client, datos_eur_usd, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] > 30.0 and rsi_eur_chf.iloc[-1] < 30.0 and rsi_eur_cad.iloc[-1] > 30.0:
                    print("haciendo seguimiento para abrir operacion al alza en eurchf")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CHF")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CAD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv")
                        datos_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_eur_chf = RSI(datos_eur_chf)
                        rsi_eur_cad = RSI(datos_eur_cad)
                        print("eurusd:", rsi_eur_usd.iloc[-1], "eurchf:", rsi_eur_chf.iloc[-1], "eurcad:",
                              rsi_eur_cad.iloc[-1])
                        if rsi_eur_usd.iloc[-1] < 30.0 or rsi_eur_cad.iloc[-1] < 30.0:
                            break
                        elif rsi_eur_chf.iloc[-1] > 30.0:
                            crear_operacion("EUR/CHF", alcista_o_bajista, client, datos_eur_chf, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] > 30.0 and rsi_eur_chf.iloc[-1] > 30.0 and rsi_eur_cad.iloc[-1] < 30.0:
                    print("haciendo seguimiento para abrir operacion al alza en eurcad")
                    while time.time() < timeout:
                        valor_extraccion = Extraccionfxcm(client, 500, 'm5', "EUR/USD")
                        if valor_extraccion == "reset":
                            reload(fxcmpy)
                            reload(Extraccionfxcm)
                            client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CHF")
                        Extraccionfxcm(client, 500, 'm5', "EUR/CAD")
                        datos_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv")
                        datos_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv")
                        datos_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv")
                        rsi_eur_usd = RSI(datos_eur_usd)
                        rsi_eur_chf = RSI(datos_eur_chf)
                        rsi_eur_cad = RSI(datos_eur_cad)
                        print("eurusd:", rsi_eur_usd.iloc[-1], "eurchf:", rsi_eur_chf.iloc[-1], "eurcad:",
                              rsi_eur_cad.iloc[-1])
                        if rsi_eur_usd.iloc[-1] < 30.0 or rsi_eur_chf.iloc[-1] < 30.0:
                            break
                        elif rsi_eur_cad.iloc[-1] > 30.0:
                            crear_operacion("EUR/CAD", alcista_o_bajista, client, datos_eur_cad, numero_de_noticias,
                                            hora_noticias)
                            print("se sale del seguimiento")
                            return
                        time.sleep(60)
                elif rsi_eur_usd.iloc[-1] > 30.0 and rsi_eur_chf.iloc[-1] > 30.0 and rsi_eur_cad.iloc[-1] > 30.0:
                    print("todos los pares salieron de la zona de sobreventa al mismo tiempo")
                    return
            time.sleep(60)


def crear_operacion(divisa, alcista_o_bajista: str, client, datos_par_divisas, numero_noticias,
                    horas_noticias):
    if alcista_o_bajista == "alcista":
        atr = ATR(datos_par_divisas, 14)
        digito_a_redondear = calcular_rendondeo(atr["ATR"].iloc[-1])
        # el stop se fija de manera de que si el precio actual es menor a los low de las 2 velas anteriores
        # entonces el stop será el precio restado con el valor del atr * 2
        client.subscribe_market_data(divisa)
        stop = ((float(client.get_last_price(divisa)["Bid"]) -
                 (round(atr["ATR"].iloc[-1], digito_a_redondear) * 2)))
        tp = ((float(client.get_last_price(divisa)["Ask"]) +
               (round(atr["ATR"].iloc[-1], digito_a_redondear) * 2)))
        # """recordar colocar el tp una vez abran los mercados"""
        client.open_trade(divisa, is_buy=True, amount='10', time_in_force="GTC", order_type="AtMarket",
                          is_in_pips=False, stop=stop, limit=tp)
        try:
            if client.is_connected():
                tradeid = client.get_open_positions('list')
            else:
                client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                time.sleep(30)
                tradeid = client.get_open_positions("list")
            print(tradeid)
            if len(tradeid) > 0:
                tradeid = tradeid[-1]["tradeId"]
                print(tradeid)
            elif len(tradeid) == 0:
                client.open_trade(divisa, is_buy=True, amount="10", time_in_force="GTC", order_type="AtMarket", is_in_pips=False, stop=stop, limit=tp)
                tradeid = client.get_open_positions("list")
                print(tradeid)
                if len(tradeid) > 0:
                    tradeid = tradeid[-1]["tradeId"]
                    print(tradeid)
                elif len(tradeid) == 0:
                    print("No se puede abrir la operacion, esperar a la proxima señal")
                    return
        except Exception as e:
            print("exception al solicitar el tradeid de la operacion", e, "de tipo", type(e), "saliendo del seguimiento")
            return
        print("operación abierta en:", divisa, "al alza")
        with open("operaciones.txt", "at") as operaciones:
            operaciones.write(f"operacion abierta con id {tradeid}")
        while True:
            try:
                if client.is_connected():
                    trades = list(client.get_open_positions()["tradeId"])
                    print(trades)
                else:
                    try:
                        client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                    except ServerError:
                        print("hubo un error al intentar reconectar el cliente, reseteando sistema de modulos")
                        return "reset"
                    time.sleep(30) 
                    trades = list(client.get_open_positions()["tradeId"])
                    print(trades)
                if tradeid in trades:
                    print("trade activo")
                else:
                    print("trade inactivo")
                    return
            except KeyError as e:
                print("hubo una exception keyerror", e, type(e), "no hay trades activos, saliendo del seguimiento")
                return
            if numero_noticias == 1:
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
            elif numero_noticias == 2:
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
                elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[1]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
            elif numero_noticias == 3:
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
                elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[1]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
                elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[2]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
            time.sleep(10)
    if alcista_o_bajista == "bajista":
        print("seguimiento a la baja")
        atr = ATR(datos_par_divisas, 14)
        digito_a_redondear = calcular_rendondeo(atr["ATR"].iloc[-1])
        # el stop se fija de manera de que si el precio actual es menor a los low de las 2 velas anteriores
        # entonces el stop será el precio restado con el valor del atr * 2
        client.subscribe_market_data(divisa)
        stop = ((float(client.get_last_price(divisa)["Bid"]) +
                 (round(atr["ATR"].iloc[-1], digito_a_redondear) * 2)))
        tp = ((float(client.get_last_price(divisa)["Ask"]) -
               (round(atr["ATR"].iloc[-1], digito_a_redondear) * 2)))
        # """recordar colocar el tp una vez abran los mercados"""
        client.open_trade(divisa, is_buy=False, amount='10', time_in_force="GTC", order_type="AtMarket",
                          is_in_pips=False,
                          stop=stop, limit=tp)
        try:
            if client.is_connected():
                tradeid = client.get_open_positions('list')
                print(tradeid)
            else:
                client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                tradeid = client.get_open_positions("list")
                print(tradeid)
            if len(tradeid) > 0:
                tradeid = tradeid[-1]["tradeId"]
            elif len(tradeid) == 0:
                client.open_trade(divisa, is_buy=False, amount="10", time_in_force="GTC", order_type="AtMarket", is_in_pips=False, stop=stop, limit=tp)
                tradeid = client.get_open_positions("list")
                if len(tradeid) > 0:
                    tradeid = tradeid[-1]["tradeId"]
                elif len(tradeid) == 0:
                    print("No se puede abrir la operacion, esperar a la proxima señal")
                    return
        except Exception as e:
            print("error al solicitar el tradeid de la operacion", e, "de tipo", type(e), "saliendo del seguimiento")
            return
        print("operación abierta en:", divisa, "a la baja")
        with open("operaciones.txt", "at") as operaciones:
            operaciones.write(f"operacion abierta con id {tradeid}")
        while True:
            try:
                if client.is_connected():
                    trades = list(client.get_open_positions()["tradeId"])
                    print(trades)
                else:
                    time.sleep(30)
                    try:
                        client = fxcmpy.fxcmpy(config_file="fxcm.cfg")
                    except ServerError:
                        print("hubo un error al intentar reconectar el cliente, reseteando sistema de modulos")
                        return "reset"
                    trades = list(client.get_open_positions()["tradeId"])
                    print(trades)
                if tradeid in trades:
                    print("trade activo")
                else:
                    print("trade inactivo")
                    return
            except KeyError as e:
                print("error keyerror", e, type(e), "no hay trades activos, saliendo de seguimiento")
                return
            if numero_noticias == 1:
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
            elif numero_noticias == 2:
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
                elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[1]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
            elif numero_noticias == 3:
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
                elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[1]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
                elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[2]:
                    client.close_trade(trade_id=tradeid, amount='10')
                    return
            time.sleep(10)


def calcular_rendondeo(number: float) -> int:
    return 3 if number >= 0.001 else 4
