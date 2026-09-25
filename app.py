"""Independent REST teaching example with synthetic camera events."""
from flask import Flask, jsonify

app = Flask(__name__)
video_logs = [
    {"camera_id": 1, "timestamp": "2024-09-04 10:00:00", "event": "motion detected"},
    {"camera_id": 2, "timestamp": "2024-09-04 10:15:00", "event": "no motion"},
]

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify(video_logs)

@app.route('/api/logs/<int:camera_id>', methods=['GET'])
def get_log_by_camera(camera_id):
    return jsonify([log for log in video_logs if log['camera_id'] == camera_id])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
