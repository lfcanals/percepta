import cv2
import os
import sys
from flask import Flask, Response, render_template
from bus import Bus
from camera import Camera
from calibration import MetaRectification
from recording import Recorder
import threading
from queue import Queue
import logging
from flask import request

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

recordingsFolder = os.getenv("BASE_FOLDER", "../..") + "/recordings"
databaseFolder = os.getenv("BASE_FOLDER", "../..") + "/database"
print("Base folder for recordings : " + recordingsFolder)
print("Base folder for config database : " + databaseFolder)

cameraId = int(sys.argv[1])


app = Flask(__name__)
bus = Bus(["front-camera"])

rectifier = MetaRectification()


# Just a main loop for capturing frames from camera
def cameraLoop():
    cam = Camera(cameraId, -1)

    def callback(frame):
        bus.notify("front-camera", rectifier.rectify(frame))
        return

    for _ in cam.process(callback): pass


cameraThread = threading.Thread(
    target=cameraLoop,
    daemon=True
)
cameraThread.start()


def streamingFrames(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_bytes = buffer.tobytes()

    return 0,(b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')


recorder = Recorder(maxSize=50_000_000, folder=recordingsFolder)


@app.route("/")
def index():
    return render_template("index.html");

@app.route("/front-camera")
def front_camera():
   return render_template("front-camera.html")

@app.route("/calibration")
def calibration():
   return render_template("calibration.html")


@app.route("/raw_video_feed/<channel>")
def video_feed(channel):
    rectificationName = request.args.get("calibration", None)
    rectifier.set(rectificationName)

    q = Queue()

    def createStreaming(frame):
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return 0, None

        bytesFrame = jpeg.tobytes()
        q.put(bytesFrame)

    bus.subscribe(channel, createStreaming)

    def generate():
        try:
            while True:
                frame = q.get()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        finally:
            bus.unsubscribe(channel, createStreaming)

    return Response(generate(),
        mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route("/enable_record_raw_video/<channel>")
def enable_record_raw_video(channel):
    recorder.prepare()
    bus.subscribe(channel, recorder.process)
    return render_template("enabled-record.html");


@app.route("/disable_record_raw_video/<channel>")
def disable_record_raw_video(channel):
    bus.unsubscribe(channel, recorder.process)
    recorder.dump()
    return render_template("disabled-record.html");


@app.route("/status_record_raw_video/<channel>")
def status_record_raw_video(channel):
    if bus.isSubscribed(channel, recorder.process):
        return render_template("front-camera/enabled-record.html");
    else:
        return render_template("front-camera/disabled-record.html");






if __name__ == "__main__":
    print("Usage:")
    print("    " + sys.argv[0] + " cameraId")
    app.run(host="0.0.0.0", port=5000, threaded=True)

