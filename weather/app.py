import datetime
import requests

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

#星期几过滤器
@app.template_filter('weeks')
def get_week_day(date):
    temp_data=datetime.datetime.strptime(date,'%Y-%m-%d')
    week_day_dict={
        0:"周一",
        1:"周二",
        2:"周三",
        3:"周四",
        4:"周五",
        5:"周六",
        6:"周日",
    }
    day=temp_data.weekday()
    return week_day_dict[day]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather')
def weather():
    city= request.args.get('c')
    if city:
        res = requests.get('http://apis.juhe.cn/simpleWeather/query?key=90703c9b141bc4c51646472973537f87&city=%s' % city)
    else:
        res = requests.get('http://apis.juhe.cn/simpleWeather/query?key=90703c9b141bc4c51646472973537f87&city=%E5%B9%BF%E5%B7%9E')
    try:
        city_a=res.json()['result']['city']
        list_a=res.json()['result']['future']
        now=res.json()['result']['realtime']

    except Exception as e:
        result = {'code': 404, 'error': 'the city is error'}
        return jsonify(result)
    return render_template('weather.html', w_city=city_a,w_now=now, w_list=list_a)


if __name__ == '__main__':
    app.run(debug=True)

