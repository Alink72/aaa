from flask import Flask, request, send_file, render_template
import matplotlib.pyplot as plt
import pandas as pd
import io

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        # 简单运算，例如计算平均值
        average = df.mean()

        # 保存运算结果为 CSV
        result_path = 'output.csv'
        average.to_csv(result_path)

        # 绘制图形
        img = io.BytesIO()
        average.plot(kind='bar')
        plt.savefig(img, format='png')
        img.seek(0)

        return send_file(img, mimetype='image/png', as_attachment=True, attachment_filename='plot.png')


@app.route('/download')
def download_file():
    return send_file('output.csv', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
