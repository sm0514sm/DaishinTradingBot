# 주식에 대한 상태 정보
from datetime import datetime
from enum import Enum

from object.Stock import Stock


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
        self.avg_buy_price: float = 0  # 매수 평균가
        self.avg_sell_price: float = 0  # 매도 평균가
        self.buy_cnt: float = 0  # 매수 개수
        self.sell_cnt: float = 0  # 매도 개수

        # 주문 전 정보
        self.target_buy_price: float = 0  # 목표 매수 평균가 (최저점 돌파시 설정됨)
        self.target_sell_price: float = 0  # 목표 매도 평균가 (최고점 돌파시 설정됨)

    def __str__(self):
        occupy_size = len(self.name.encode()) - (len(self.name.encode()) - len(self.name)) // 2
        name = ' ' * (20 - occupy_size) + self.name
        return f'{self.code} {name} ' \
               f'current_price:{self.current_price:8}, ' \
               f'min_n_days:{self.min_n_days:8}, max_n_days:{self.max_n_days:8}, '\
               f'status:{self.status.name:>6}, ' \
               f'avg_buy_price:{self.avg_buy_price:10}, avg_sell_price:{self.avg_sell_price:10}, ' \
               f'buy_cnt:{self.buy_cnt:3}, sell_cnt:{self.sell_cnt:3} ' \
               f'target_buy_price:{self.target_buy_price:8}, target_sell_price:{self.target_sell_price:8}'
