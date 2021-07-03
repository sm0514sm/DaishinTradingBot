# 주식에 대한 상태 정보
from datetime import datetime
from enum import Enum

from object.Stock import Stock
from sm_api.util import dif_percent


class Status(Enum):
    WAIT = 0
    BUY_READY = 1
    BOUGHT = 2
    SELL_READY = 3


class MonitorStock(Stock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_n_days: float = 0 if 'min_n_days' not in kwargs.keys() else kwargs['min_n_days']  # N_DAYS 중 최저가
        self.max_n_days: float = 0 if 'max_n_days' not in kwargs.keys() else kwargs['max_n_days']  # N_DAYS 중 최고가
        self.status: Status = Status.WAIT  # 현재 상태
        self.last_time: datetime

        # 주문 정보
        self.profit_value: float = 0  # 매수 평균가 (손익단가)
        self.quantity: float = 0  # 매수 개수 (매도가능수량)

        # 주문 전 정보
        self.target_buy_price: float = 0  # 목표 매수 평균가 (최저점 돌파시 설정됨)
        self.target_sell_price: float = 0  # 목표 매도 평균가 (최고점 돌파시 설정됨)

    def __str__(self):
        occupy_size = len(self.name.encode()) - (len(self.name.encode()) - len(self.name)) // 2
        name = ' ' * (20 - occupy_size) + self.name
        return_str = f'{self.code} {name} ' \
                     f'{self.current_price:8} ' \
                     f'{self.min_n_days:8}({dif_percent(self.min_n_days, self.current_price):6.1f}) ' \
                     f'{self.max_n_days:8}({dif_percent(self.max_n_days, self.current_price):6.1f}) ' \
                     f'{self.status.name:>6} | '

        if self.status != Status.WAIT:
            return_str += f'손익단가:{self.profit_value:10}, quantity:{self.quantity:3}, '

        if self.status == Status.WAIT:
            return_str += f''
        elif self.status == Status.BUY_READY:
            return_str += f'target_buy_price:{self.target_buy_price:8} '
        elif self.status == Status.BOUGHT:
            return_str += f''
        elif self.status == Status.SELL_READY:
            return_str += f'target_sell_price:{self.target_sell_price:8} '

        return return_str
