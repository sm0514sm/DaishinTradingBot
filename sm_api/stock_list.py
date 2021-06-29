from object.Cybos import Cybos

"""
https://cybosplus.github.io/ 참고
"""


def get_stock_list(stock_type: int = 0, is_only_st=True) -> list:
    cybos = Cybos()
    """ stock_type에 맞는 주식 종목 리스트를 반환
      :arg: stock_type: 0 모든 종목, 1 코스피, 2 코스닥
      :rtype: list
      """
    return_list = []
    # 종목코드 리스트 구하기
    CpCodeMgr = cybos.CpCodeMgr
    # print(CpCodeMgr.GetMarketStartTime())  # 장 시작 시간
    # print(CpCodeMgr.GetMarketEndTime())  # 장 마감 시간
    if stock_type == 0:
        code_tuple = CpCodeMgr.GetStockListByMarket(1) + CpCodeMgr.GetStockListByMarket(2)
    else:
        code_tuple = CpCodeMgr.GetStockListByMarket(stock_type)
    for i, code in enumerate(code_tuple):
        secondCode = CpCodeMgr.GetStockSectionKind(code)
        stdPrice = CpCodeMgr.GetStockStdPrice(code)  # 1 주식, 10, ETF
        name = CpCodeMgr.CodeToName(code)
        if is_only_st and secondCode != 1:
            continue
        return_list.append([i, code, secondCode, stdPrice, name])
    return return_list


if __name__ == "__main__":
    stock_list = get_stock_list(0, is_only_st=True)
    for stock in stock_list:
        print(stock)
