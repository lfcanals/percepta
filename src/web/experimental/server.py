import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)

cap = cv2.VideoCapture(0)


def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # YOUR TRANSFORMATIONS HERE
        frame = cv2.flip(frame, 1)

        _, buffer = cv2.imencode('.jpg', frame)
        jpg_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')


@app.route("/")
def index():
    return render_template("front-camera.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)

