import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time

# 動画ファイルのパス
VIDEO_FILE = "/Users/rihito/Movies/flv/ビデオ日記.mp4"

# mjpgサーバーの設定
MJPG_SERVER_PORT = 8080
MJPG_SERVER_ADDRESS = ("", MJPG_SERVER_PORT)


class MJPGServerHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video_capture = cv2.VideoCapture(VIDEO_FILE)
        self.frame_lock = threading.Lock()

    def do_GET(self):
        if self.path.endswith(".mjpg"):
            self.send_response(200)
            self.send_header("Content-type", "multipart/x-mixed-replace; boundary=--jpgboundary")
            self.end_headers()
            while True:
                ret, frame = self.video_capture.read()
                if not ret:
                    break
                _, img_encoded = cv2.imencode(".jpg", frame)
                jpg_data = b"--jpgboundary\r\n"
                jpg_data += b"Content-type: image/jpeg\r\n\r\n"
                jpg_data += bytearray(img_encoded)
                jpg_data += b"\r\n\r\n"
                with self.frame_lock:
                    self.wfile.write(jpg_data)
                time.sleep(0.03)  # サーバーのフレームレート調整（0.03秒ごとにフレームを送信）

    def log_message(self, format, *args):
        # ログメッセージを表示しないようにオーバーライド
        pass


def run_mjpg_server():
    httpd = HTTPServer(MJPG_SERVER_ADDRESS, MJPGServerHandler)
    print("MJPG Server started on http://localhost:{}/".format(MJPG_SERVER_PORT))
    httpd.serve_forever()


# MJPGサーバーを別スレッドで実行
mjpg_server_thread = threading.Thread(target=run_mjpg_server)
mjpg_server_thread.daemon = True
mjpg_server_thread.start()

# メインスレッドでは他の処理を実行
while True:
    # 任意の処理を実行する
    time.sleep(1)
