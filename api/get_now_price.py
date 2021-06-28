from object.Cybos import Cybos


def get_now_price(cybos: Cybos, code) -> int:
    StockMst = cybos.StockMst
    StockMst.SetInputValue(0, code)
    StockMst.BlockRequest()
    return StockMst.GetHeaderValue(11)


def get_now_prices(cybos: Cybos, codes) -> list:
    StockMst2 = cybos.StockMst2
    StockMst2.SetInputValue(0, ','.join(codes))
    StockMst2.BlockRequest()


if __name__ == "__main__":
    print(get_now_price(Cybos(), "A003540"))  # 대신 증권
    print(get_now_price(Cybos(), "A003545"))
    print(get_now_price(Cybos(), "A003555"))
