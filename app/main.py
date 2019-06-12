import csv
import io
import os
import uuid

import waitress
from flask import Flask, render_template, request, url_for, make_response
from werkzeug.utils import redirect

from app.Good import Good
from app.GoodManager import GoodManager


def start():
    app = Flask(__name__)
    app.config['IMAGE_DIR'] = os.path.join('static')

    manager = GoodManager()
    huawei_p20 = Good(str(uuid.uuid4()),
                      name='Huawei P20',
                      price=39990,
                      hit=True,
                      count=20,
                      color='Black',
                      memory=128,
                      ram=4,
                      screen=5.8,
                      camera=20,
                      img_path='static\\huawei_p20.png')

    huawei_nova3 = Good(str(uuid.uuid4()),
                        name='Huawei Nova 3',
                        price=29990,
                        count=15,
                        color='Iris Blue',
                        memory=128,
                        ram=4,
                        screen=6.3,
                        camera=24,
                        img_path='static\\huawei_nova_3.png')

    xiaomi_redmi6 = Good(str(uuid.uuid4()),
                         name='Xiaomi Redmi 6',
                         price=13990,
                         count=12,
                         color='Gold',
                         memory=64,
                         ram=4,
                         screen=5.45,
                         camera=12,
                         img_path='static\\xiaomi_redmi_6.png')

    manager.good_add(huawei_p20)
    manager.good_add(huawei_nova3)
    manager.good_add(xiaomi_redmi6)

    @app.route('/')
    def index():
        search = request.args.get('search')
        if search:
            result = manager.goods_search(search)
            return render_template("index.html", goods=result, search=search)
        return render_template("index.html", goods=manager.goods)

    @app.route('/goods/<good_id>/edit')
    def good_edit(good_id):
        good = None
        if good_id == 'new':
            good = Good(good_id)
        else:
            good = manager.good_search_by_id(good_id)
        return render_template("good_edit.html", good=good)

    @app.route('/goods/<good_id>/save', methods=['POST'])
    def good_save(good_id):
        name = request.form['name']
        price = int(request.form['price'])
        hit = request.form['hit'].lower() == 'да'
        count = int(request.form['count'])
        color = request.form['color']
        memory = int(request.form['memory'])
        ram = int(request.form['ram'])
        screen = float(request.form['screen'])
        camera = int(request.form['camera'])
        img = request.files['img']
        image = img.filename
        path = os.path.join(app.config['IMAGE_DIR'], image)
        img.save(path)

        if good_id == 'new':
            good = Good(str(uuid.uuid4()), name=name, price=price, hit=hit, count=count, color=color, memory=memory, ram=ram, screen=screen, camera=camera, img_path=path)
            manager.good_add(good)
        else:
            good = manager.good_search_by_id(good_id)
            good.name = name
            good.price = price
            good.hit = hit
            good.count = count
            good.color = color
            good.memory = memory
            good.ram = ram
            good.screen = screen
            good.camera = camera
            # TODO: подумать над удалением неиспользуемых изображений
            # os.remove(good.img_path)
            good.img_path = path
        return redirect(url_for('index', goods=manager.goods))

    @app.route('/goods/<good_id>/remove', methods=['POST'])
    def good_remove(good_id):
        manager.good_remove(good_id)
        return redirect(url_for('index'))

    @app.route('/goods/sort_up')
    def sort_up():
        manager.sort(down=False)
        return redirect(url_for('index'))

    @app.route('/goods/sort_down')
    def sort_down():
        manager.sort(down=True)
        return redirect(url_for('index'))

    @app.route('/goods/<good_id>/sell', methods=['POST'])
    def good_sell(good_id):
        count = int(request.form['count'])
        good = manager.good_search_by_id(good_id)
        if good.count >= count > 0:
            good.count = good.count - count
            return redirect(url_for('index', goods=manager.goods))
        return redirect(url_for('good_selling', good_id=good_id))

    @app.route('/goods/<good_id>/selling')
    def good_selling(good_id):
        good = manager.good_search_by_id(good_id)
        return render_template('good_sell.html', good=good)

    @app.route('/goods/import-export')
    def good_imex():
        return render_template("good_imex.html")

    @app.route('/goods/import', methods=['POST'])
    def good_import():
        if 'doc' not in request.files:
            redirect(url_for('index'))
        doc = request.files['doc']
        content = io.StringIO(doc.read().decode("utf8"))
        reader = csv.DictReader(content, delimiter=';')
        for row in reader:
            name = row['name']
            price = int(row['price'])
            hit = row['hit'].lower() == 'true'
            count = int(row['count'])
            color = row['color']
            memory = int(row['memory'])
            ram = int(row['ram'])
            screen = float(row['screen'])
            camera = int(row['camera'])
            img_path = row['img_path']
            good = Good(str(uuid.uuid4()), name=name, price=price, hit=hit, count=count, color=color, memory=memory, ram=ram, screen=screen, camera=camera, img_path=img_path)
            manager.good_add(good)
        return redirect(url_for('index', goods=manager.goods))

    @app.route('/goods/export')
    def good_export():
        result = []
        goods = manager.goods
        fieldnames = ['id', 'name', 'price', 'hit', 'count', 'color', 'memory', 'ram', 'screen', 'camera', 'img_path']
        for good in goods:
            result.append(vars(good))

        content = io.StringIO()
        writer = csv.DictWriter(content, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in result:
            writer.writerow(row)

        response = make_response(content.getvalue())
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'inline; filename=goods-export.csv'
        return response

    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9877, debug=True)


if __name__ == '__main__':
    start()
