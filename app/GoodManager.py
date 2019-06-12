class GoodManager:
    def __init__(self):
        self.goods = []

    def good_add(self, good):
        self.goods.append(good)

    def goods_search(self, search):
        result = []
        search_lowecased = search.strip().lower()
        for good in self.goods:
            if search_lowecased in good.name.lower():
                result.append(good)
                continue
            if search_lowecased in good.color.lower():
                result.append(good)
                continue
        return result

    def good_search_by_id(self, good_id):
        for good in self.goods:
            if good.id == good_id:
                return good

    def good_remove(self, good_id):
        result = []
        for good in self.goods:
            if good.id != good_id:
                result.append(good)
        self.goods = result

    @staticmethod
    def by_price_key(good):
        return good.price

    def sort(self, *, down):
        sorted_goods = sorted(self.goods, key=self.by_price_key)
        if not down:
            sorted_goods.reverse()
        self.goods = sorted_goods
