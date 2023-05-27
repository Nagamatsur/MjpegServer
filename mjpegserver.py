import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import webbrowser

# 動画ファイルのパス
video_path = "/Users/rihito/Movies/flv/ビデオ日記.mp4"
ip_address = "192.168.2.110"
# mjpgサーバーのポート番号
server_port = 8000

# 動画を配信するためのMJPEGサーバーのクラス
class VideoStreamer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # ルートパスにアクセスがあった場合、「こんにちは」と「表示」ボタンを表示するHTMLを返す
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = '''
                <html>
                <head>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <h1>こんにちは</h1>
                    <button onclick="startVideo()">表示</button>
                    <br>
                    <img id="video" style="display: none;" src="/video_feed.mjpg">
                    <script>
                        function startVideo() {
                            var videoElement = document.getElementById("video");
                            videoElement.style.display = "block";
                        }
                    </script>
                </body>
                </html>
            '''
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/video_feed.mjpg':
            # /video_feed.mjpgにアクセスがあった場合、動画をフレーム単位でMJPEG形式で配信する
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--myboundary')
            self.end_headers()
            cap = cv2.VideoCapture(video_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                ret, encoded_frame = cv2.imencode('.jpg', frame)
                if not ret:
                    break
                self.wfile.write(b'--frame\r\n')
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', len(encoded_frame))
                self.end_headers()
                self.wfile.write(encoded_frame)
                self.wfile.write(b'\r\n')
            cap.release()
        else:
            self.send_response(404)

    def log_message(self, format, *args):
        # ログ出力を抑制
        return

# メインの処理
def main():
    # MJPEGサーバーを別スレッドで起動
    server_thread = threading.Thread(target=lambda: HTTPServer((ip_address, server_port), VideoStreamer).serve_forever())
    server_thread.daemon = True
    server_thread.start()

    # ブラウザでページを開く
    webbrowser.open_new_tab('http://'+str(ip_address)+':'+str(server_port))

    # メインスレッドは終了しないようにする
    while True:
        pass

if __name__ == '__main__':
    main()