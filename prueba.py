import fxcmpy
import socket
import pickle
from multiprocessing import Process, current_process
import time
from ExtraccionDatosfxcm import Extraccionfxcm
import pandas as pd
from RSI import RSI
from indicadores import ATR

#import sys
#a_del=[]
#for module in sys.modules.keys():
   # if "fxcm" in module:
  #      print(module)
 #       a_del.append(module)
#for module in a_del:
 #   del sys.modules[module]
#del fxcmpy
#for module in sys.modules.keys():
   # if "fxcm" in module:
  #      print(module)
 #   else:
#        print("no")
if __name__ == "__main__":
    print("conectando")
    client = fxcmpy.fxcmpy(config_file='fxcm.cfg')
    print("conectado")
    client.open_trade("EUR/USD", is_buy=True, amount="10", time_in_force="GTC", order_type="AtMarket", is_in_pips=False, stop=1.1840)
    tradeid = client.get_open_positions("list")[-1]["tradeId"]
    while True:
        trades = list(client.get_open_positions()["tradeId"])
        if tradeid in trades:
            print("trade activo")
        else:
            print("trade inactivo")
        time.sleep(10)
#Extraccionfxcm(client, 5000, "m5", "EUR/USD")
#Extraccionfxcm(client, 5000, "m5", "NZD/USD")
#Extraccionfxcm(client, 5000, "m5", "GBP/USD")
#Extraccionfxcm(client, 5000, "m5", "EUR/CHF")
#Extraccionfxcm(client, 5000, "m5", "EUR/CAD")
#client.close()

#data_eur_usd = pd.read_csv("datos_M5_EUR_USD.csv", index_col="date")
#data_nzd_usd = pd.read_csv("datos_M5_NZD_USD.csv", index_col="date")
#data_gbp_usd = pd.read_csv("datos_M5_GBP_USD.csv", index_col="date")
#data_eur_chf = pd.read_csv("datos_M5_EUR_CHF.csv", index_col="date")
#data_eur_cad = pd.read_csv("datos_M5_EUR_CAD.csv", index_col="date")

#rsi_eur_usd = RSI(data_eur_usd)
#rsi_nzd_usd = RSI(data_nzd_usd)
#rsi_gbp_usd = RSI(data_gbp_usd)
#rsi_eur_chf = RSI(data_eur_chf)
#rsi_eur_cad = RSI(data_eur_cad)

#atr = ATR(data_eur_usd)
#atr_gbp = ATR(data_gbp_usd)
#atr_nzd = ATR(data_nzd_usd)

#
# fichero = open("fichero de prueba", "wb")
# pickle.dump(True, fichero)
# fichero.close()
#
# fichero = open("fichero de prueba", "rb")
# lectura = pickle.load(fichero)
# print(lectura)
# fichero.close()
#
#
#
# if __name__ == '__main__':
