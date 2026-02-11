import cv2
import sys
from flask import Flask, Response, render_template
from camera import Camera

app = Flask(__name__)

cameraId = int(sys.argv[1])


def streamingFrames(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_bytes = buffer.tobytes()

    return 0,(b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')


def createStreaming():
    cam = Camera(cameraId)
    yield from cam.process(streamingFrames)



@app.route("/")
def index():
    return render_template("front-camera.html")


@app.route("/video_feed")
def video_feed():
    return Response(createStreaming(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print("Usage:")
    print("    " + sys.argv[0] + " cameraId")
    app.run(host="0.0.0.0", port=5000, threaded=True)

