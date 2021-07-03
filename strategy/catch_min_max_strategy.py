import time
from datetime import datetime, date

from object.MyStock import MyStock
from sm_api.stock_chart import get_chart_info_dict
from object.MonitorStock import MonitorStock, Status
from sm_api.now_stock_info import get_now_prices, now_stocks_infos
from sm_api.order_stock import get_my_stock_balance, get_buyable_amount, order_buy_stock, get_my_stock, order_sell_stock
from sm_api.stock_list import get_stock_list, read_stock_list_from_txt_file

# INPUT_CODES = [stock[1] for stock in get_stock_list()]
INPUT_CODES = read_stock_list_from_txt_file()
# INPUT_CODES = ["A041830", "A096770"]
COUNT = 7  # 최대 최소 모니터링 기준 days
DELAY = 10  # 모니터링 간격 seconds
VALUE_K = 3
BUY_AMOUNT = 500000  # 종목당 최대 구입 가격


# 주식의 정보(최소값, 최대값)을 가져옴
def get_stock_min_max(codes) -> dict:
    print("* get_stock_min_max(): 주식의 정보(최소값, 최대값)을 가져옴")
    stock_dict = dict()
    for i, code in enumerate(codes):
        time.sleep(0.25)
        chart_info = get_chart_info_dict(code, COUNT, info=[0, 4, 3, 5], types='D')
        stock_dict[code] = MonitorStock(code=code,
                                        min_n_days=chart_info.get('min_n_days'),
                                        max_n_days=chart_info.get('max_n_days'))
        print(f'{code} ({i + 1:3}/{len(codes)}) {stock_dict[code].min_n_days:8}, {stock_dict[code].max_n_days:8}')
    return stock_dict


# 계좌에 이미 가진 주식 정보를 가져와 업데이트
def add_stock_info_in_acc(stock_dict: dict) -> None:
    print("* add_stock_info_in_acc(): 계좌에 이미 가진 주식 정보를 가져와 업데이트")
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
            stock.profit_value = stock_info.book_value
            stock.quantity = stock_info.quantity
            stock_dict[stock_info.code] = stock
        else:
            stock: MonitorStock = stock_dict.get(stock_info.code)
            stock.status = Status.BOUGHT
            stock.profit_value = stock_info.book_value
            stock.quantity = stock_info.quantity


def update_stock_min_max(stock_dict: dict):
    print("* update_stock_min_max(): 날짜가 바뀌어 각 종목의 최소, 최대값을 다시 계산")
    for i, stock in enumerate(stock_dict.values()):
        time.sleep(0.25)
        chart_info = get_chart_info_dict(stock.code, COUNT, info=[0, 4, 3, 5], types='D')
        before_min_n_days = stock.min_n_days
        before_max_n_days = stock.max_n_days
        stock.min_n_days = chart_info.get('min_n_days')
        stock.max_n_days = chart_info.get('max_n_days')
        print(f'{stock.code} ({i + 1:3}/{len(stock_dict.values())}) '
              f'{before_min_n_days:8}->{stock.min_n_days:8}, {before_max_n_days:8}->{stock.max_n_days:8}')
    return stock_dict


def run_strategy():
    last_date = date.today()
    print(last_date)
    # 모니터링할 주식 최소, 최대값 구함
    stock_dict: dict = get_stock_min_max(INPUT_CODES)

    # 계좌에 있는 주식 정보 추가
    add_stock_info_in_acc(stock_dict)
    while True:
        t_now = datetime.now()
        if last_date != date.today():
            print("* 날짜가 바뀌어 각 종목의 최소, 최대값을 다시 계산합니다.")
            update_stock_min_max(stock_dict)
            last_date = date.today()
        t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
        t_end = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
        if t_now.weekday() in [5, 6] or not (t_start < t_now < t_end):  # 오늘이 토, 일이거나 개장시간 아님
            # print("* 개장 시간이 아님")
            time.sleep(DELAY)
            continue
        print(f'{t_now.year}-{t_now.month:02}-{t_now.day:02} {t_now.hour:02}:{t_now.minute:02}:{t_now.second:02}')
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
                    if stock.current_price > get_buyable_amount():
                        print(f"* WARN: {stock.name}의 가격 {stock.current_price}는 {BUY_AMOUNT}보다 커서 구매 불가")
                        stock.status = Status.WAIT
                        continue
                    if order_buy_stock(stock.code, BUY_AMOUNT // stock.current_price):
                        print("* 매수완료")
                        stock.status = Status.BOUGHT
                        time.sleep(1)
                        if myStock := get_my_stock(stock.code):
                            stock.quantity = myStock.quantity
                            stock.profit_value = myStock.profit_value
                    else:
                        print("* 매수실패")
                        stock.status = Status.WAIT
                        continue
            elif stock.status == Status.BOUGHT and stock.current_price > stock.max_n_days:
                stock.status = Status.SELL_READY
            elif stock.status == Status.SELL_READY:
                stock.max_n_days = max(stock.max_n_days, stock.current_price)
                stock.target_sell_price = stock.max_n_days * (1 - VALUE_K)
                if stock.current_price < stock.target_sell_price:
                    if order_sell_stock(stock.code, stock.quantity):
                        print("* 매도완료")
                        stock.status = Status.WAIT
                        time.sleep(1)
                        # 매도 로그 표시
                    else:
                        print("* 매도실패")
                        continue
        time.sleep(DELAY)


if __name__ == "__main__":
    run_strategy()
