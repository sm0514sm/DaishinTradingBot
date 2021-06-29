class MyStock:
    def __init__(self, name, eval_amount, eval_gain, earning_rate, code, quantity, book_value, profit_value):
        self.name = name
        self.code = code
        self.eval_amount = eval_amount  # 평가금액
        self.eval_gain = eval_gain  # 평가손익
        self.earning_rate = earning_rate  # 수익률
        self.quantity = quantity  # 매도 가능 수량
        self.book_value = book_value  # 장부가: 수수료 포함 개당 거래한 가격 = (매수금액+수수료)/수량
        self.profit_value = profit_value  # 손익단가: 현재 매도시 세금등 감안해 계산 = {(장부가 * 수량) + (매도수수료 +제세금)} / 수량

    def print_info(self):
        print(f"{self.name:>15} {self.code:>8} {self.quantity:>5} {self.book_value:>10} {self.profit_value:>10}"
              f"{self.eval_amount:>10} {self.eval_gain:>10} {self.earning_rate:>5.3f}")

    def __repr__(self):
        return (f"MyStock({self.name}, {self.code}, {self.quantity}, {self.book_value}, {self.profit_value}, "
                f"{self.eval_amount}, {self.eval_gain}, {self.earning_rate})")
