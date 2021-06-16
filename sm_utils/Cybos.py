import win32com.client


class Cybos(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):  # Foo 클래스 객체에 _instance 속성이 없다면
            cls._instance = super().__new__(cls)  # Foo 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance  # Foo._instance를 리턴

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):  # Foo 클래스 객체에 _init 속성이 없다면
            self.StockChart = win32com.client.Dispatch("CpSysDib.StockChart")
            self.CpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
            self.CpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
            self.CpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
            self.CpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")
            self.StockMst = win32com.client.Dispatch("dscbo1.StockMst")
            cls._init = True


if __name__ == "__main__":
    c = Cybos()
