from flask import Flask, render_template, Response, request, redirect
from exercises.pose_left import generate_frames
from exercises.pose_right import generate_frames
from exercises.pose_pushup import pushup
from exercises.pose_squat import squat
from exercises.pose_kneetaps import kneetaps
from exercises.pose_op import op
from exercises.pose_lunges import lunges
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

# Redirect '/' to '/api'
@app.route('/')
def home():
    return redirect('/api')

@app.route('/api', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form.get('exercise')
        target_reps = request.form.get('reps', type=int, default=10)
        target_sets = request.form.get('sets', type=int, default=3)
        return redirect(f'/video_feed_{subject}?reps={target_reps}&sets={target_sets}')
    
    return render_template('request_page.html')

# Generalized route function
def generate_video_feed(exercise_func):
    target_reps = request.args.get('reps', default=10, type=int)
    target_sets = request.args.get('sets', default=3, type=int)
    return Response(exercise_func(target_reps=target_reps, target_sets=target_sets), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Exercise routes
@app.route('/video_feed_left')
def video_feed_left():
    return generate_video_feed(generate_frames)

@app.route('/video_feed_right')
def video_feed_right():
    return generate_video_feed(generate_frames)

@app.route('/video_feed_pushup')
def video_feed_pushup():
    return generate_video_feed(pushup)

@app.route('/video_feed_squat')
def video_feed_squat():
    return generate_video_feed(squat)

@app.route('/video_feed_kneetaps')
def video_feed_kneetaps():
    return generate_video_feed(kneetaps)

@app.route('/video_feed_op')
def video_feed_op():
    return generate_video_feed(op)

@app.route('/video_feed_lunges')
def video_feed_lunges():
    return generate_video_feed(lunges)

@app.route('/show')
def show():
    subject = request.args.get('sub')
    target_reps = request.args.get('reps', default=10, type=int)
    target_sets = request.args.get('sets', default=3, type=int)
    return redirect(f'/video_feed_{subject}?reps={target_reps}&sets={target_sets}')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
