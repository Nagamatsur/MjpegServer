import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# 動画ファイルのパス
VIDEO_PATH = "/Users/rihito/Movies/flv/ビデオ日記.mp4"


def generate_frames():
    # 動画ファイルを開く
    video = cv2.VideoCapture(VIDEO_PATH)
    
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            # フレームをMJPEG形式にエンコードして返す
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # ジェネレータとしてフレームを返す
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    # 動画フレームのジェネレータをレスポンスとして返す
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.2.110', debug=True)
