import win32com.client
from object.Cybos import Cybos
from object.MyStock import MyStock


def get_CpTd6033():
    cybos = Cybos()
    """
    계좌정보 BlockRequest한 CpTd6033 객체 return
    """
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
    return CpTd6033


def get_my_stock_balance() -> list:
    cybos = Cybos()
    CpTd6033 = get_CpTd6033()

    stock_list = []
    for index in range(CpTd6033.GetHeaderValue(7)):
        stock_list.append(MyStock(CpTd6033.GetDataValue(0, index), CpTd6033.GetDataValue(9, index),
                                  CpTd6033.GetDataValue(10, index), CpTd6033.GetDataValue(11, index),
                                  CpTd6033.GetDataValue(12, index), CpTd6033.GetDataValue(15, index),
                                  CpTd6033.GetDataValue(17, index), CpTd6033.GetDataValue(18, index)))
    return stock_list


def print_my_acc():
    cybos = Cybos()
    CpTd6033 = get_CpTd6033()

    print("계좌명", CpTd6033.GetHeaderValue(0))
    print("결제 잔고수량", CpTd6033.GetHeaderValue(1))
    print("체결 잔고 수량", CpTd6033.GetHeaderValue(2))
    print("평가 금액", CpTd6033.GetHeaderValue(3))
    print("평가 손익", CpTd6033.GetHeaderValue(4))
    print("수신개수", CpTd6033.GetHeaderValue(7))
    print("수익률", CpTd6033.GetHeaderValue(8))
    print()


# 매수 가능 금액(예수금)
def get_buyable_amount() -> int:
    cybos = Cybos()
    CpTdNew5331A = cybos.CpTdNew5331A
    CpTdUtil = cybos.CpTdUtil

    acc = CpTdUtil.AccountNumber[0]  # 계좌번호
    accFlag = CpTdUtil.GoodsList(acc, 1)  # 주식상품 구분
    CpTdNew5331A.SetInputValue(0, acc)
    CpTdNew5331A.SetInputValue(1, accFlag[0])
    CpTdNew5331A.BlockRequest()

    return CpTdNew5331A.GetHeaderValue(10)


# code 종목을 buy_cnt 만큼 시장가로 매수
def order_buy_stock(code: str, buy_cnt: int):
    cybos = Cybos()

    # 주식 매수 주문
    CpTd0311 = cybos.CpTd0311
    CpTd0311.SetInputValue(0, "2")  # 2: 매수
    CpTd0311.SetInputValue(1, cybos.CpTdUtil.AccountNumber[0])  # 계좌번호
    CpTd0311.SetInputValue(2, "01")  #
    CpTd0311.SetInputValue(3, code)  # 종목코드 - A003540 - 대신증권 종목
    CpTd0311.SetInputValue(4, buy_cnt)  # 매수수량 10주
    CpTd0311.SetInputValue(8, "03")  # 주문호가 구분코드 - 01: 보통, 03: 시장가

    # 매수 주문 요청
    nRet = CpTd0311.BlockRequest()
    if nRet != 0:  # 4면 15초 호출 제한
        print("주문요청 오류:", nRet)

    rqStatus = CpTd0311.GetDibStatus()
    print("통신상태", rqStatus, CpTd0311.GetDibMsg1())
    if rqStatus != 0:
        exit()


if __name__ == "__main__":
    print_my_acc()
    print(get_my_stock_balance())
    print(get_buyable_amount())
