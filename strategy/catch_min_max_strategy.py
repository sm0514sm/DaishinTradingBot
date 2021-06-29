import time

from object.Cybos import Cybos
from object.MyStock import MyStock
from sm_api.stock_chart import get_chart_info_dict
from object.MonitorStock import MonitorStock, Status
from sm_api.now_stock_info import get_now_prices, now_stocks_infos
from sm_api.order_stock import get_my_stock_balance, get_buyable_amount, order_buy_stock
from sm_api.stock_list import get_stock_list

# INPUT_CODES = [stock[1] for stock in get_stock_list()]
INPUT_CODES = ["A005930", "A035420", "A035720", "A035510", "A036570", "A051910"]
COUNT = 30  # 최대 최소 모니터링 기준 days
DELAY = 10  # 모니터링 간격 seconds
VALUE_K = 4
BUY_AMOUNT = 500000  # 최대 구입 가격


# 주식의 정보(최소값, 최대값)을 가져옴
def get_stock_min_max(codes) -> dict:
    print("get_stock_min_max()")
    stock_dict = dict()
    for i, code in enumerate(codes):
        time.sleep(0.25)
        chart_info = get_chart_info_dict(code, COUNT, info=[0, 4, 3, 5], types='D')
        stock_dict[code] = MonitorStock(code=code,
                                        min_n_days=chart_info.get('min_n_days'),
                                        max_n_days=chart_info.get('max_n_days'))
        print(f'{code} ({i + 1}/{len(codes)}) {stock_dict[code].min_n_days}, {stock_dict[code].max_n_days}')
    return stock_dict


# 계좌에 이미 가진 주식 정보를 가져와 업데이트
def add_stock_info_in_acc(stock_dict: dict) -> None:
    print("add_stock_info_in_acc()")
    stock_infos: list[MyStock] = get_my_stock_balance()
    for stock_info in stock_infos:
        if stock_info.code not in INPUT_CODES:
            INPUT_CODES.append(stock_info.code)
        if not stock_dict.get(stock_info.code):
            chart_info = get_chart_info_dict(stock_info.code, COUNT, info=[0, 4, 3, 5], types='D')
            stock = MonitorStock(code=stock_info.code,
                                 min_n_days=chart_info.get('min_n_days'),
                                 max_n_days=chart_info.get('max_n_days'))
            stock.status = Status.BOUGHT
            stock.avg_buy_price = stock_info.book_value
            stock.buy_cnt = stock_info.quantity
            stock_dict[stock_info.code] = stock
        else:
            stock: MonitorStock = stock_dict.get(stock_info.code)
            stock.status = Status.BOUGHT
            stock.avg_buy_price = stock_info.book_value
            stock.buy_cnt = stock_info.quantity


def update_stock_min_max(stock_dict: dict):
    print("update_stock_min_max()")
    for i, stock in enumerate(stock_dict.values()):
        time.sleep(0.25)
        chart_info = get_chart_info_dict(stock.code, COUNT, info=[0, 4, 3, 5], types='D')
        before_min_n_days = stock.min_n_days
        before_max_n_days = stock.max_n_days
        stock.min_n_days = chart_info.get('min_n_days')
        stock.max_n_days = chart_info.get('max_n_days')
        print(f'{stock.code} ({i + 1}/{len(stock_dict.values())}) '
              f'{before_min_n_days}->{stock.min_n_days}, {before_max_n_days}->{stock.max_n_days}')
    return stock_dict
    pass


def run_strategy():
    cybos = Cybos()
    print(INPUT_CODES)
    # 모니터링할 주식 최소, 최대값 구함
    stock_dict: dict = get_stock_min_max(INPUT_CODES)

    # 계좌에 있는 주식 정보 추가
    add_stock_info_in_acc(stock_dict)
    # TODO 시간에 따라
    while True:
        now = time.localtime()
        print(f'{now.tm_year}-{now.tm_mon:02}-{now.tm_mday:02} {now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}')
        # if 날짜가 바뀌면:
        # 모니터링할 주식 min, max 다시 구하기
        #   update_stock_min_max(stock_dict)
        # if 주식 개장 시간이 아니면:
        #   continue
        infos: dict = now_stocks_infos(INPUT_CODES)
        for stock in stock_dict.values():
            stock.update_info(**infos[stock.code])
            print(stock)
            if stock.status == Status.WAIT and stock.current_price < stock.min_n_days \
                    and get_buyable_amount() >= BUY_AMOUNT:
                stock.status = Status.BUY_READY
            elif stock.status == Status.BUY_READY:
                stock.min_n_days = min(stock.min_n_days, stock.current_price)
                stock.target_buy_price = stock.min_n_days * (1 + VALUE_K)
                if stock.current_price > stock.target_buy_price:
                    # TODO 매수
                    order_buy_stock(stock.code, 1)
                    print("매수함")
                    # 매수 가능 수량 결정
                    time.sleep(1)
                    stock.status = Status.BOUGHT
                    # stock.avg_buy_price = 평균구입가격
            elif stock.status == Status.BOUGHT and stock.current_price > stock.max_n_days:
                stock.status = Status.SELL_READY
            elif stock.status == Status.SELL_READY:
                stock.max_n_days = max(stock.max_n_days, stock.current_price)
                stock.target_sell_price = stock.max_n_days * (1 - VALUE_K)
                if stock.current_price < stock.target_sell_price:
                    # TODO 매도
                    print("매도함")
                    # 매도 가능 수량 확인
                    time.sleep(1)
                    stock.status = Status.WAIT
                    stock.avg_sell_price = stock.current_price
                    stock = MonitorStock(min=stock.min_n_days, max=stock.max_n_days)  # 가격

        time.sleep(DELAY)


if __name__ == "__main__":
    run_strategy()
