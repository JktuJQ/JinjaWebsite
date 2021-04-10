from flask import render_template, Flask

app = Flask(__name__)


@app.route('/')
def news():
    import json
    with open("test_com.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    print(news_list['ob'])
    return render_template('est1.html', news=news_list['ob'])


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')