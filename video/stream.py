from flask import Blueprint, send_from_directory
import os

video_bp = Blueprint('video', __name__)

@video_bp.route('/video/<filename>')
def video(filename):
    video_dir = os.path.join(os.path.dirname(__file__), "dash_output")
    return send_from_directory(video_dir, filename)
