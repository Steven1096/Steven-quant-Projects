# -*- coding: utf-8 -*-


import backtrader as bt

class MovingAverageStrategy(bt.Strategy):
    params = (
        ('ma_period', 15),
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = 17
        self.buy_price = None
        self.buy_comm = None

        # Ajouter une moyenne mobile simple
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.ma_period)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'ACHETÉ au prix {order.executed.price}')
            elif order.issell():
                self.log(f'VENDU au prix {order.executed.price}')

        self.order = None

    def log(self, text):
        print(f'{self.datas[0].datetime.date(0)} {text}')

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.data_close[0] > self.sma[0]:
                self.log(f'ACHAT CRÉÉ au prix {self.data_close[0]}')
                self.order = self.buy()
        else:
            if self.data_close[0] < self.sma[0]:
                self.log(f'VENTE CRÉÉE au prix {self.data_close[0]}')
                self.order = self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MovingAverageStrategy)

  
