import cv2
import threading
from mjpeg_server import MJPEGServer

# 動画ファイルのパス
video_file = 'path/to/your/video.mp4'

# ローカルでのIPアドレスとポート番号
ip_address = '192.168.2.110'
port = 8000

# サーバーの起動
server = MJPEGServer(ip_address, port)
server.start()

# 動画ストリーミング処理のスレッド
def video_streaming():
    # OpenCVを使用して動画を開く
    cap = cv2.VideoCapture(video_file)
    
    while True:
        # フレームの読み込み
        ret, frame = cap.read()
        
        if ret:
            # フレームをサーバーに送信
            server.send_frame(frame)
        else:
            # 動画の最後まで再生した場合はループを抜ける
            break
    
    # クリーンアップ
    cap.release()
    server.stop()

# 動画ストリーミング処理のスレッドを開始
thread = threading.Thread(target=video_streaming)
thread.start()

# ブラウザからアクセスすると表示されるHTML
html = '''
<html>
<head>
    <script>
        function displayVideo() {
            // ビデオ要素を作成
            var video = document.createElement('video');
            video.src = 'http://{}:{}/stream.mjpg';
            video.autoplay = true;
            video.style.width = '100%';
            
            // ビデオを表示する要素に追加
            var videoContainer = document.getElementById('video-container');
            videoContainer.appendChild(video);
            
            // 表示ボタンを非表示にする
            var displayButton = document.getElementById('display-button');
            displayButton.style.display = 'none';
        }
    </script>
</head>
<body>
    <h1>こんにちは</h1>
    <button id="display-button" onclick="displayVideo()">表示</button>
    <div id="video-container"></div>
</body>
</html>
'''.format(ip_address, port)

# サーバーにHTMLを登録
server.register_html(html)

# サーバーの待機
server.wait()
