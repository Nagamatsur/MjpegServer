import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

video_file = "/Users/rihito/Movies/flv/ビデオ日記.mp4"
ip_address = "192.168.2.110"
port = 8080

class VideoStreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')  # 文字エンコーディングを指定
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
