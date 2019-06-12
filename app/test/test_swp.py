from app.Good import Good
from app.GoodManager import GoodManager
import uuid

huawei_p20 = None
xiaomi_redmi6 = None
manager = None

huawei_id = str(uuid.uuid4())
huawei_name = 'Huawei P20'
huawei_price = 39990
huawei_hit = True
huawei_count = 200
huawei_color = 'Black'
huawei_memory = 128
huawei_ram = 4
huawei_screen = 5.8
huawei_camera = 20
huawei_img_path = ''

xiaomi_id = str(uuid.uuid4())
xiaomi_name = 'Xiaomi Redmi 6'
xiaomi_price = 13990
xiaomi_hit = False
xiaomi_count = 12
xiaomi_color = 'Gold'
xiaomi_memory = 64
xiaomi_ram = 4
xiaomi_screen = 5.45
xiaomi_camera = 12
xiaomi_img_path = ''


def test_good_init():
    global huawei_p20, xiaomi_redmi6
    huawei_p20 = Good(huawei_id,
                      name=huawei_name,
                      price=huawei_price,
                      hit=huawei_hit,
                      count=huawei_count,
                      color=huawei_color,
                      memory=huawei_memory,
                      ram=huawei_ram,
                      screen=huawei_screen,
                      camera=huawei_camera,
                      img_path=huawei_img_path)

    xiaomi_redmi6 = Good(xiaomi_id,
                         name=xiaomi_name,
                         price=xiaomi_price,
                         hit=xiaomi_hit,
                         count=xiaomi_count,
                         color=xiaomi_color,
                         memory=xiaomi_memory,
                         ram=xiaomi_ram,
                         screen=xiaomi_screen,
                         camera=xiaomi_camera,
                         img_path=xiaomi_img_path)

    assert huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id and \
           huawei_p20.id == huawei_id


def test_good_type():
    assert isinstance(huawei_p20, Good)


def test_good_manager_init():
    global manager
    manager = GoodManager()

    assert manager.goods == []


def test_good_manager_type():
    assert isinstance(manager, GoodManager)


def test_good_add():
    manager.good_add(huawei_p20)
    manager.good_add(xiaomi_redmi6)

    assert len(manager.goods) == 2


def test_goods_search_by_name():
    expected = list()
    expected.append(huawei_p20)
    actual = manager.goods_search('Huawei')

    assert actual == expected


def test_goods_search_by_color():
    expected = list()
    expected.append(xiaomi_redmi6)
    actual = manager.goods_search('Gold')

    assert actual == expected


def test_search_by_id():
    expected = huawei_id
    good = manager.good_search_by_id(huawei_id)
    actual = good.id

    assert actual == expected


def test_by_price_key():
    expected = 39990
    actual = manager.by_price_key(huawei_p20)

    assert actual == expected


def test_sort_up():
    manager.sort(down=False)

    assert manager.goods[0].id == huawei_id


def test_sort_down():
    manager.sort(down=True)

    assert manager.goods[0].id == xiaomi_id


def test_good_remove():
    manager.good_remove(huawei_id)

    assert len(manager.goods) == 1
