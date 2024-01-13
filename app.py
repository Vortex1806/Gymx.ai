from flask import Flask, render_template,Response
import cv2
import mediapipe as mp
import numpy as np
app = Flask(__name__)
feed = cv2.VideoCapture(0)
WIDTH = 10000
HEIGHT = 10000
feed.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
feed.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
width = int(feed.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(feed.get(cv2.CAP_PROP_FRAME_HEIGHT))

# draw landmarks & connections to screen
mp_drawing = mp.solutions.drawing_utils
# import Pose model
mp_pose = mp.solutions.pose

def calc_angle(x, y, z):
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    radians = np.arctan2(z[1] - y[1], z[0] - y[0]) - np.arctan2(x[1] - y[1], x[0] - y[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle
# @app.route('/', endpoint='index_endpoint')
# def index():
#     return render_template('index.html')




def generate_frames():
    counter = 0
    state = 'Down'
    range_flag = True
    halfway = False
    feedback = ''
    frame_count = 0
    # Plotting variables
    frames = []
    left_angle = []
    right_angle = []
    body_angles = []
    while feed.isOpened():
        while True:
            success, frame = feed.read()
            if not success:
                break
            else:
                frame_count += 1
                frames.append(frame_count)
                # Mirror frame
                frame = cv2.flip(frame, 1)
                # Recolor image from BGR to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Pose detection
                with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                    detection = pose.process(image)
                # Recolor image from RGB back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Your exercise recognition code here...
                try:
                    landmarks = detection.pose_landmarks.landmark

                    # left arm
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

                    # right arm
                    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

                    left_elbow_angle = calc_angle(left_shoulder, left_elbow, left_wrist)
                    right_elbow_angle = calc_angle(right_shoulder, right_elbow, right_wrist)
                    # Visualize angles
                    cv2.putText(image, str(left_elbow_angle),
                                tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(image, str(right_elbow_angle),
                                tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

                    left_angle.append(left_elbow_angle)
                    right_angle.append(right_elbow_angle)

                    # down state
                    if left_elbow_angle > 160 and right_elbow_angle > 160:
                        if not range_flag:
                            feedback = 'Did not curl completely.'
                        else:
                            feedback = 'Good rep!'
                        state = 'Down'

                    # not fully curled
                    elif (left_elbow_angle > 50 and right_elbow_angle > 50) and state == 'Down':
                        range_flag = False
                        feedback = ''

                    # up state
                    elif (left_elbow_angle < 30 and right_elbow_angle < 30) and state == 'Down':
                        state = 'Up'
                        feedback = ''
                        range_flag = True
                        counter += 1

                except:
                    pass

                    # Status box setup
            cv2.rectangle(image, (0, 0), (width, int(height * 0.1)), (245, 117, 16), -1)
            cv2.putText(image, "REPS:", (int(width * 0.01), int(height * 0.025)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1,
                                cv2.LINE_AA)  # font, size, color, line width, line type
            cv2.putText(image, str(counter), (int(width * 0.01), int(height * 0.08)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, "STATE:", (int(width * 0.1), int(height * 0.025)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, state, (int(width * 0.1), int(height * 0.08)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, "FEEDBACK:", (int(width * 0.2), int(height * 0.025)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, feedback, (int(width * 0.2), int(height * 0.08)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            mp_drawing.draw_landmarks(image, detection.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2,
                                                                     circle_radius=2),
                                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2,
                                                                     circle_radius=2))

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            # Encode image to JPEG
            # _, buffer = cv2.imencode('.jpg', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            _, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/',endpoint='workoutplanner_endpoint')
def workout_planner():
    name="Shubh Vora"
    photourl="www.gmail.com"
    email="shubhvora03@gmail.com"
    firstname="Shubh"
    return render_template('workout.html',name=name,photourl=photourl,email=email,firstname=firstname)

@app.route('/recipeai',endpoint='getkhana_endpoint')
def get_khana():
    print("got request")
    name="Shubh Vora"
    photourl="www.gmail.com"
    email="shubhvora03@gmail.com"
    firstname="Shubh"
    return render_template('getkhana.html',name=name,photourl=photourl,email=email,firstname=firstname)

@app.route('/logworkout',endpoint='log_endpoint')
def log_work():
    print("got request")
    name="Shubh Vora"
    photourl="www.gmail.com"
    email="shubhvora03@gmail.com"
    firstname="Shubh"
    return render_template('workoutlog.html',name=name,photourl=photourl,email=email,firstname=firstname)

@app.route('/monitoring',endpoint='monitoring_endpoint')
def stream_page():
    return render_template('video_stream.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
