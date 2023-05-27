import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
<<<<<<< HEAD
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
=======

video_file = "path/to/your/video/file.mp4"
ip_address = "192.168.2.110"
port = 8080

class VideoStreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('<html><head><title>Video Stream</title></head>', 'utf-8'))
            self.wfile.write(bytes('<body><h1>こんにちは</h1><button onclick="startStream()">表示</button>', 'utf-8'))
            self.wfile.write(bytes('<img id="stream" src="" width="640" height="480" />', 'utf-8'))
            self.wfile.write(bytes('<script>', 'utf-8'))
            self.wfile.write(bytes('function startStream() {', 'utf-8'))
            self.wfile.write(bytes('var img = document.getElementById("stream");', 'utf-8'))
            self.wfile.write(bytes('img.src = "http://' + ip_address + ':' + str(port) + '/stream.mjpg";', 'utf-8'))
            self.wfile.write(bytes('}', 'utf-8'))
            self.wfile.write(bytes('</script></body></html>', 'utf-8'))
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()
            stream_video()

def stream_video():
    cap = cv2.VideoCapture(video_file)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, img_encoded = cv2.imencode('.jpg', frame)
        frame_data = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + img_encoded.tobytes() + b'\r\n'
        VideoStreamHandler.wfile.write(b'Content-Length: ' + bytes(str(len(frame_data)), 'utf-8') + b'\r\n')
        VideoStreamHandler.wfile.write(b'\r\n')
        VideoStreamHandler.wfile.write(frame_data)
        VideoStreamHandler.wfile.write(b'\r\n')

    cap.release()

def start_server():
    server_address = (ip_address, port)
    http_server = HTTPServer(server_address, VideoStreamHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    print("Server started at http://" + ip_address + ":" + str(port))

    while True:
        pass
>>>>>>> 6c8b8a4 (8)
