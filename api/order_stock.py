import win32com.client
from object.Cybos import Cybos
from object.MyStock import MyStock


def get_my_stock_balance(cybos: Cybos) -> list:
    CpTdUtil = cybos.CpTdUtil
    CpTd6033 = cybos.CpTd6033

    acc = CpTdUtil.AccountNumber[0]  # 계좌번호
    accFlag = CpTdUtil.GoodsList(acc, 1)  # 주식상품 구분

    CpTd6033.SetInputValue(0, acc)
    CpTd6033.SetInputValue(1, accFlag[0])
    CpTd6033.SetInputValue(2, 50)  # 요청 건수 (최대 50)

    nRet = CpTd6033.BlockRequest()
    if nRet != 0:  # 4면 15초 호출 제한
        print("주문요청 오류:", nRet)

    print("계좌명", CpTd6033.GetHeaderValue(0))
    print("결제 잔고수량", CpTd6033.GetHeaderValue(1))
    print("체결 잔고 수량", CpTd6033.GetHeaderValue(2))
    print("평가 금액", CpTd6033.GetHeaderValue(3))
    print("평가 손익", CpTd6033.GetHeaderValue(4))
    print("수신개수", CpTd6033.GetHeaderValue(7))
    print("수익률", CpTd6033.GetHeaderValue(8))
    print()
    stock_list = []
    for index in range(CpTd6033.GetHeaderValue(7)):
        stock_list.append(MyStock(CpTd6033.GetDataValue(0, index), CpTd6033.GetDataValue(9, index),
                                  CpTd6033.GetDataValue(10, index), CpTd6033.GetDataValue(11, index),
                                  CpTd6033.GetDataValue(12, index), CpTd6033.GetDataValue(15, index),
                                  CpTd6033.GetDataValue(17, index), CpTd6033.GetDataValue(18, index)))
    print(stock_list[0].print_info())
    return stock_list


def order_stock():
    # 주문 초기화
    CpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")

    # 주식 매수 주문
    acc = CpTdUtil.AccountNumber[0]  # 계좌번호

    objStockOrder = win32com.client.Dispatch("CpTrade.CpTd0311")
    objStockOrder.SetInputValue(0, "2")  # 2: 매수
    objStockOrder.SetInputValue(1, acc)  # 계좌번호
    objStockOrder.SetInputValue(2, "01")  #
    objStockOrder.SetInputValue(3, "A003540")  # 종목코드 - A003540 - 대신증권 종목
    objStockOrder.SetInputValue(4, 1)  # 매수수량 10주
    # objStockOrder.SetInputValue(5, 14100)  # 주문단가  - 14,100원
    objStockOrder.SetInputValue(8, "03")  # 주문호가 구분코드 - 01: 보통, 03: 시장가

    # 매수 주문 요청
    nRet = objStockOrder.BlockRequest()
    if nRet != 0:  # 4면 15초 호출 제한
        print("주문요청 오류:", nRet)

    rqStatus = objStockOrder.GetDibStatus()
    rqRet = objStockOrder.GetDibMsg1()
    print("통신상태", rqStatus, rqRet)
    if rqStatus != 0:
        exit()


if __name__ == "__main__":
    get_my_stock_balance(Cybos())
