from flask import Flask, render_template, send_from_directory
import pandas as pd

app = Flask(__name__)

# 通过添加静态文件目录来提供 360 网页资源
app.config['app-files'] = 'app-files'  # 你的 360 网页资源目录

@app.route('/123')
def index():
    # 返回 360 网页的入口页面
    return send_from_directory(app.config['app-files'], 'index.html')

@app.route('/<path:filename>')
def serve_360_resources(filename):
    # 返回 360 网页的相关资源，如 JS、CSS、图片等
    return send_from_directory(app.config['app-files'], filename)

# 读取 CSV 文件并提取经纬度
df = pd.read_csv('details.csv')
locations = df[['經度', '緯度']].to_dict(orient='records')

@app.route('/g')
def g_route():
    return render_template('map.html', locations=locations)

@app.route('/a', methods=['GET', 'POST'])
def a_route():
    return render_template("Introduce.html")

@app.route('/b', methods=['GET', 'POST'])
def b_route():
    return render_template("about-us.html")

@app.route('/c', methods=['GET', 'POST'])
def c_route():
    return render_template("biodiversity.html")

@app.route('/d', methods=['GET', 'POST'])
def d_route():
    return render_template("community.html")

@app.route('/e', methods=['GET', 'POST'])
def e_route():
    return render_template("live-observation.html")

@app.route('/f', methods=['GET', 'POST'])
def f_route():
    return render_template("wetland-introduction.html")

@app.route('/', methods=['GET', 'POST'])
def _route():
    return render_template("back.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=13066, debug=True)
