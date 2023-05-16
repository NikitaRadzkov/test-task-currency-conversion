from api.services import get_data, get_exchange_rate


get_exchange_rate("GBP")
print(get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP"))
