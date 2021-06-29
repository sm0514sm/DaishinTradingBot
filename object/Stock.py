class Stock:
    def __init__(self, **kwargs):
        self.code = "" if 'code' not in kwargs.keys() else kwargs['code']
        self.name = "" if 'name' not in kwargs.keys() else kwargs['name']
        self.current_price = 0 if 'current_price' not in kwargs.keys() else kwargs['current_price']
        self.start_price = 0 if 'start_price' not in kwargs.keys() else kwargs['start_price']
        self.max_price = 0 if 'max_price' not in kwargs.keys() else kwargs['max_price']
        self.min_price = 0 if 'min_price' not in kwargs.keys() else kwargs['min_price']
        self.vol_cnt = 0 if 'vol_cnt' not in kwargs.keys() else kwargs['vol_cnt']
        self.vol_amount = 0 if 'vol_amount' not in kwargs.keys() else kwargs['vol_amount']
        self.vol_last_cnt = 0 if 'vol_last_cnt' not in kwargs.keys() else kwargs['vol_last_cnt']

    def update_info(self, **kwargs):
        self.code = self.code if 'code' not in kwargs.keys() else kwargs['code']
        self.name = self.name if 'name' not in kwargs.keys() else kwargs['name']
        self.current_price = self.current_price if 'current_price' not in kwargs.keys() else kwargs['current_price']
        self.start_price = self.start_price if 'start_price' not in kwargs.keys() else kwargs['start_price']
        self.max_price = self.max_price if 'max_price' not in kwargs.keys() else kwargs['max_price']
        self.min_price = self.min_price if 'min_price' not in kwargs.keys() else kwargs['min_price']
        self.vol_cnt = self.vol_cnt if 'vol_cnt' not in kwargs.keys() else kwargs['vol_cnt']
        self.vol_amount = self.vol_amount if 'vol_amount' not in kwargs.keys() else kwargs['vol_amount']
        self.vol_last_cnt = self.vol_last_cnt if 'vol_last_cnt' not in kwargs.keys() else kwargs['vol_last_cnt']
