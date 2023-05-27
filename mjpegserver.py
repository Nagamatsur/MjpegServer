import cv2
from flask import Flask, Response, render_template
import time

app = Flask(__name__)
video_path = "/Users/rihito/Movies/flv/ビデオ日記.mp4"  # 動画ファイルのパス


def generate_frames():
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # フレームの処理（サイズ変更など）
        frame = cv2.resize(frame, (640, 360))  # サイズを変更する場合は適宜調整

        # フレームをバイナリデータに変換して配信
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 20])  # JPEG品質を80に設定
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.015)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.2.110', debug=True)
