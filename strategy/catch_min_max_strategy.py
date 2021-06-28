import time

from object.Cybos import Cybos
from api.get_chart import get_chart_info_dict
from object.MonitorStock import MonitorStock

INPUT_CODES = []
COUNT = 30  # 최대 최소 모니터링 기준 days


# 주식의 정보(최소값, 최대값)을 가져옴
def get_stcok_min_max(codes, cnt) -> dict:
    print("get_stock_min_max")
    stock_dict = dict()
    for code in codes:
        chart_info = get_chart_info_dict(Cybos(), code, COUNT, info=[0, 4, 3, 5], types='D')
        stock_dict[code] = MonitorStock(chart_info.get('min'), chart_info.get('max'))
    return stock_dict


def run_strategy(cybos: Cybos):
    # 모니터링할 주식 최소, 최대값 구함
    # 계좌에 있는 주식 정보 추가
    # TODO 시간에 따라
    while True:
        # if 날짜가 바뀌면:
        # 모니터링할 주식 min, max 다시 구하기
        time.sleep(3)
        """
        for stock_name, current_price in get_now_prices(INPUT_CODES):
            stock = stock_dict[stock_name]
            if stock.status == Status.WAIT and current_price < stock.min and 현재 거래가능 잔고 >= BUY_AMOUNT:
                stock.status = Status.BUY_READY
            elif stock.status == Status.BUY_READY:
                stock.min = min(stock.min, current_price)
                stock.target_buy_price = stock.min * (1 + VALUE_K)
                if current_price > stock.target_buy_price:
                    # TODO 매수
                    # 매수 가능 수량 결정
                    
                    time.sleep(1)
                    stock.status = Status.BOUGHT
                    # stock.avg_buy_price = 평균구입가격
            elif stock.sttus == Status.BOUGHT and current_price > stock.max:
                stock.status = Status.SELL_READY
            elif stock.status == Status.SELL_READY:
                stock.max = max(stock.max, current_price)
                stock.target_sell_price = stock.max * (1 - VALUE_K)
                if current_price < stock.target_sell_price:
                    # TODO 매도
                    # 매도 가능 수량 확인
                    
                    time.sleep(1)
                    stock.status = Status.WAIT
                    stock.avg_sell_price = current_price
                    stock = MonitorStock(stock.min, stock.max)  # 초기화
        """


if __name__ == "__main__":
    run_strategy(Cybos())
