from flask import Flask, render_template, send_from_directory
import pandas as pd

app = Flask(__name__)

# 设置 360 网页的静态文件目录
app.config['app-files'] = 'app-files'  # 360 网页资源目录

# 设置 AR 网页的静态文件目录
app.config['AR'] = 'AR'  # AR 网页资源目录

# 提供 360 网页的入口文件
@app.route('/app-files/index.html')
def index():
    return send_from_directory(app.config['app-files'], 'index.html')

# 提供 360 网页的相关资源（如 JS、CSS、图片等）
@app.route('/app-files/<path:filename>')
def serve_360_resources(filename):
    return send_from_directory(app.config['app-files'], filename)

# 提供 AR 网页的入口文件
@app.route('/AR/AR1.html')
def ar1_page():
    return send_from_directory(app.config['AR'], 'AR1.html')

@app.route('/AR/AR2.html')
def ar2_page():
    return send_from_directory(app.config['AR'], 'AR2.html')

# 提供 AR 网页的相关资源（如 JS、CSS、图片等）
@app.route('/AR/<path:filename>')
def serve_ar_resources(filename):
    return send_from_directory(app.config['AR'], filename)

# 读取 CSV 文件并提取经纬度
df = pd.read_csv('details.csv')
locations = df[['經度', '緯度']].to_dict(orient='records')

# 其他路由
@app.route('/g')
def g_route():
    return render_template('map.html', locations=locations)

@app.route('/a', methods=['GET', 'POST'])
def a_route():
    return render_template("Introduce.html")

@app.route('/b', methods=['GET', 'POST'])
def b_route():
    return render_template("about-us.html")

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
def home():
    return render_template("back.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=13066, debug=True)