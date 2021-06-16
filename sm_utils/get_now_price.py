import win32com.client
inStockMst = win32com.client.Dispatch("dscbo1.StockMst")
inStockMst.SetInputValue(0, "A003540")
while True:
    inStockMst.BlockRequest()
    current = inStockMst.GetHeaderValue(11)         # 현재가
    print(current)