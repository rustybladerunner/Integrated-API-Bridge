# Flask: A Python micro web framework that allows you to create a web application.
# jsonify: A helper function from Flask that converts Python dictionaries (or lists) into JSON-formatted responses, which are commonly used in REST APIs.
# request: This object holds the incoming HTTP request data (query parameters, headers, etc.).
from flask import Flask, jsonify, request

# Here, an instance of the Flask class is created. The __name__ argument tells Flask how to locate resources (static files, templates, etc.).
# This instance (app) will serve as the main object through which routes and other configurations are registered.
app = Flask(__name__)

# Simulate a video surveillance system log
video_logs = [
    {"camera_id": 1, "timestamp": "2024-09-04 10:00:00", "event": "motion detected"},
    {"camera_id": 2, "timestamp": "2024-09-04 10:15:00", "event": "no motion"},
]

# Create a route for fetching all video logs
# @app.route('/api/logs'): Defines a URL route for the API. When an HTTP GET request is made to /api/logs, this function will handle the request.
# methods=['GET']: Specifies that this route should only respond to GET requests.
# get_logs(): This is the function that gets called when the /api/logs route is accessed. 
#  It returns the video_logs list in JSON format using the jsonify() function.
@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify(video_logs)

# Create another route for fetching logs by camera_id.
# app.route('/api/logs/<int:camera_id>'): This defines a dynamic route, where <int:camera_id> is a variable URL component. 
# Flask will capture this part of the URL and pass it as an argument to the get_log_by_camera() function.
#  Inside the function, a list comprehension is used to filter the video_logs list based on the camera_id.
# jsonify(filtered_logs): Converts the filtered logs to JSON format and returns them in the response.
@app.route('/api/logs/<int:camera_id>', methods=['GET'])
def get_log_by_camera(camera_id):
    filtered_logs = [log for log in video_logs if log['camera_id'] == camera_id]
    return jsonify(filtered_logs)

# Run the Flask app.
# This block ensures that the Flask application only runs when the script is executed directly.
#  The debug=True option enables development features like auto-reloading when the code changes and helpful error messages.
if __name__ == '__main__':
    app.run(debug=True)