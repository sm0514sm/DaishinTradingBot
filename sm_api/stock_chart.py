from object.Cybos import Cybos


class Candle:
    def __init__(self, date_str, high_price, low_price, close_price):
        self.date_str = date_str  # 날짜
        self.low_price = low_price  # 저가
        self.high_price = high_price  # 고가
        self.close_price = close_price  # 종가

    def print(self):
        print(self.date_str, self.low_price, self.high_price, self.close_price)


def get_chart_info_dict(code: str, count: int, info: list, types: str):
    cybos = Cybos()
    StockChart = cybos.StockChart
    StockChart.SetInputValue(0, code)  # 종목코드
    StockChart.SetInputValue(1, ord('2'))  # 기간요청시 1, 개수요청시 2 (ASCII 변환필요)
    StockChart.SetInputValue(4, count)  # 요청 개수
    StockChart.SetInputValue(5, info)  # [날짜, 시간, 시가, 고가, 저가, 종가, 전일대비, 거래량, 거래대금, ...]
    StockChart.SetInputValue(6, ord(types))  # 데이터 차트 종류 일D, 주W, 월M, 분m, 틱T

    StockChart.BlockRequest()

    chart_info_dict = dict()
    candles = []
    for i in range(StockChart.GetHeaderValue(3)):
        candles.append(Candle(StockChart.GetDataValue(0, i), StockChart.GetDataValue(1, i),
                              StockChart.GetDataValue(2, i), StockChart.GetDataValue(3, i)))
    chart_info_dict['candles'] = candles
    chart_info_dict['min_n_days'] = min(candle.low_price for candle in candles)
    chart_info_dict['max_n_days'] = max(candle.high_price for candle in candles)
    return chart_info_dict


if __name__ == "__main__":
    chart_info = get_chart_info_dict(code="A000020", count=100, info=[0, 4, 3, 5], types='D')
    print(chart_info.get('min_n_days'))
    print(chart_info.get('max_n_days'))
