from flask import Flask
from flask import render_template
from flask import Response
import json

from db.mongodb import mongo
from spider.mafengwo import MafengwoSpider

# 创建Flask对象
app = Flask(__name__)

@app.route('/')
def view():
    return render_template('view.html')

# 渲染数据的方法
@app.route('/echarts/<city>')
def chars(city):
    # 获取城市的景点数据量
    count = mongo.find_scenic_count(city)

    print(count)
    # 如果没有查到需要的数据, 就开启一个爬虫, 去采集需要的数据
    if not count:
        # 创建指定城市的爬虫, 抓取需要的数据
        MafengwoSpider(city).run()

    # 查询数据
    datas = mongo.find_scenics(city)
    # 返回json格式的数据
    return Response(json.dumps(datas))

# 启动服务
app.run(debug=True)