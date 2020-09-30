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