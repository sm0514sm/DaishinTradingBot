import time

from object.Cybos import Cybos
from sm_api.stock_list import get_stock_list


def get_now_price(code) -> int:
    cybos = Cybos()
    StockMst = cybos.StockMst
    StockMst.SetInputValue(0, code)
    StockMst.BlockRequest()
    return StockMst.GetHeaderValue(11)


def get_now_prices(codes) -> list[list[str, int]]:
    cybos = Cybos()
    return_result = []
    StockMst2 = cybos.StockMst2
    StockMst2.SetInputValue(0, ','.join(codes))
    StockMst2.BlockRequest()
    if len(codes) != StockMst2.GetHeaderValue(0):
        print("WARN: get_now_prices 개수가 다릅니다.")
    for i in range(len(codes)):
        return_result.append([StockMst2.GetDataValue(0, i), StockMst2.GetDataValue(3, i)])
    return return_result


def now_stocks_infos(codes) -> dict:
    cybos = Cybos()
    return_result = dict()
    StockMst2 = cybos.StockMst2
    for i in range(len(codes) // 100 + 1):
        StockMst2.SetInputValue(0, ','.join(codes[i * 100:(i + 1) * 100]))
        StockMst2.BlockRequest()
        for index in range(len(codes[i * 100:(i + 1) * 100])):
            info_dict = dict()
            info_dict['code'] = StockMst2.GetDataValue(0, index)
            info_dict['name'] = StockMst2.GetDataValue(1, index)
            info_dict['current_price'] = StockMst2.GetDataValue(3, index)
            info_dict['start_price'] = StockMst2.GetDataValue(6, index)
            info_dict['max_price'] = StockMst2.GetDataValue(7, index)
            info_dict['min_price'] = StockMst2.GetDataValue(8, index)
            info_dict['vol_cnt'] = StockMst2.GetDataValue(11, index)
            info_dict['vol_amount'] = StockMst2.GetDataValue(12, index)
            info_dict['vol_last_cnt'] = StockMst2.GetDataValue(20, index)
            return_result[info_dict['code']] = info_dict
        time.sleep(0.5)
    if len(codes) != len(return_result.items()):
        print("WARN: get_now_prices 개수가 다릅니다.")
        print(f"  └─ {len(codes)=} != {len(return_result.items())=}")

    return return_result


if __name__ == "__main__":
    # print(get_now_price("A003540"))  # 대신 증권
    # print(get_now_price("A003545"))
    print(get_now_price("A025550"))
    # print(get_now_prices(["A003540", "A003545", "A003555"]))
    print(now_stocks_infos(["A003540", "A003545", "A003555"]))
    # now_stocks_infos([stock[1] for stock in get_stock_list()])
