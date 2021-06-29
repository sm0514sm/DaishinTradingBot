import win32com.client


class Cybos(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):  # Foo 클래스 객체에 _instance 속성이 없다면
            cls._instance = super().__new__(cls)  # Foo 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance  # Foo._instance를 리턴

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):  # Foo 클래스 객체에 _init 속성이 없다면
            self.CpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
            self.CpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

            self.StockChart = win32com.client.Dispatch("CpSysDib.StockChart")

            self.CpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")  # 주식 주문
            self.CpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")
            self.CpTd6033 = win32com.client.Dispatch("CpTrade.CpTd6033")  # 주식 잔고 조회
            self.CpTdNew5331A = win32com.client.Dispatch("CpTrade.CpTdNew5331A")  # 매수 가능 금액

            self.StockMst = win32com.client.Dispatch("dscbo1.StockMst")
            self.StockMst2 = win32com.client.Dispatch("dscbo1.StockMst2")
            cls._init = True
            if self.CpCybos.IsConnect == 0:
                print("PLUS가 정상적으로 연결되지 않음\n"
                      "아래 내용 확인 바람\n"
                      "1. Cybos Plus가 켜져있는지\n"
                      "2. Python 32bit로 실행시키는지\n"
                      "3. 파이썬(혹은 IDE)가 관리자 권한인지")
                exit()
            if self.CpTdUtil.TradeInit(0) != 0:
                print("주문 초기화 실패")
                exit()


if __name__ == "__main__":
    c = Cybos()
