# 주식에 대한 상태 정보
from datetime import datetime
from enum import Enum


class Status(Enum):
    WAIT = 0
    BUY_READY = 1
    BOUGHT = 2
    SELL_READY = 3


class MonitorStock(object):
    def __init__(self, *args, **kwargs):
        self.min: float = 0 if not args else args[0]  # N_DAYS 중 최저가
        self.max: float = 0 if not args else args[1]  # N_DAYS 중 최고가
        self.status: Status = Status.WAIT  # 현재 상태
        self.last_time: datetime

        # 주문 정보
        self.avg_buy_price: float = 0  # 매수 평균가
        self.avg_sell_price: float = 0  # 매도 평균가
        self.buy_volume: float = 0  # 매수 거래량
        self.sell_volume: float = 0  # 매도 거래량

        # 주문 전 정보
        self.target_buy_price: float = 0  # 목표 매수 평균가 (최저점 돌파시 설정됨)
        self.target_sell_price: float = 0  # 목표 매도 평균가 (최고점 돌파시 설정됨)

    def __str__(self):
        return f'{{min:{self.min}, max:{self.max}, status:{self.status.name}, avg_buy_price:{self.avg_buy_price},' \
               f'avg_sell_price:{self.avg_sell_price}, buy_volume:{self.buy_volume}, sell_volume:{self.sell_volume}}}'
