from flask import Flask, render_template, Response, request, redirect, url_for, flash
from camera import CameraStream
import cv2
import requests
import sqlite3

app = Flask(__name__)

cap = CameraStream().start()

console = []
directional = ""


# Main Index
@app.route('/robotControl')
def index():
    """Video streaming home page."""
    return render_template('index.html', console=console, directional=directional)


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        connection = sqlite3.connect('userdata.db')
        with connection:
            cursor = connection.cursor()
            username = request.form['uname']
            password = request.form['password']
            query = "SELECT name,password FROM users WHERE name='"+username+"' AND password='"+password+"'"
            cursor.execute(query)
            results = cursor.fetchall()
        if connection:
            connection.close()
        if len(results) == 0:
            return render_template('login.html')
        else:
            console.append("Hello, " + username + "!")
            return redirect(url_for("index"))
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        connection = sqlite3.connect('userdata.db')
        with connection:
            cursor = connection.cursor()
            username = request.form['uname']
            password = request.form['password']
            check = "SELECT name FROM users WHERE name='"+username+"'"
            cursor.execute(check)
            results = cursor.fetchall()
            if len(results) == 0:
                add = "INSERT INTO users (name, password) VALUES ('" + username + "', '" + password + "')"
                cursor.execute(add)
                connection.commit()
                flash("Success! Your username and password have been recorded!")
            else:
                flash("This username has already been taken!")
        if connection:
            connection.close()
    return render_template('signup.html')


@app.route('/robotControl', methods=['POST', 'GET'])
def handleInput():
    if request.method == 'POST':
        if 'forwardSubmit' in request.form:
            forwardEntry = int(request.form['moveForward'])
            forward(forwardEntry)
            return render_template('index.html', console=console, directional=directional)
        elif 'backwardSubmit' in request.form:
            backwardEntry = int(request.form['moveBackward'])
            backward(backwardEntry)
            return render_template('index.html', console=console, directional=directional)
        elif 'leftSubmit' in request.form:
            leftEntry = int(request.form['moveLeft'])
            left(leftEntry)
            return render_template('index.html', console=console, directional=directional)
        elif 'rightSubmit' in request.form:
            rightEntry = int(request.form['moveRight'])
            right(rightEntry)
            return render_template('index.html', console=console, directional=directional)
        elif 'exit' in request.form:
            console.clear()
            return redirect(url_for("login"))
        else:
            return render_template('index.html', console=console, directional=directional)


# Camera
def gen_frame():
    """Video streaming generator function."""
    while cap:
        frame = cap.read()
        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')  # concate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Movement
SERVER_URL = 'http://192.168.1.72:5000/%s'
FORWARD_URL = SERVER_URL % 'forward/%d'
REVERSE_URL = SERVER_URL % 'reverse/%d'
LEFT_URL = SERVER_URL % 'left/%d'
RIGHT_URL = SERVER_URL % 'right/%d'
url = ''


def forward(forwardNum):
    if forwardNum <= 0:
        console.append('Improper forward input of ' + str(forwardNum) + '. Please try again.')
    else:
        if forwardNum == 1:
            console.append('Moving forward 1 inch.')
            forwardBackwardDirection()
        else:
            console.append('Moving forward ' + str(forwardNum) + ' inches.')
            forwardBackwardDirection()
        url = FORWARD_URL % forwardNum
        try:
          response = requests.get(url)
          if response.status_code != 200:
            print("Something went wrong " + url)
        except Exception as e:
          print("Error connecting to server")
        url = "http://192.168.1.72:5000/stop"
        try:
          response = requests.get(url)
          if response.status_code != 200:
            print("Something went wrong " + url)
        except Exception as e:
          print("Error connecting to server")


def backward(backwardNum):
    if backwardNum <= 0:
        console.append('Improper backward input of ' + str(backwardNum) + '. Please try again.')
    else:
        if backwardNum == 1:
            console.append('Moving backward 1 inch.')
            forwardBackwardDirection()
        else:
            console.append('Moving backward ' + str(backwardNum) + ' inches.')
            forwardBackwardDirection()
        url = REVERSE_URL % backwardNum
        try:
          response = requests.get(url)
          if response.status_code != 200:
            print("Something went wrong " + url)
        except Exception as e:
          print("Error connecting to server")
        url = "http://192.168.1.72:5000/stop"
        try:
          response = requests.get(url)
          if response.status_code != 200:
            print("Something went wrong " + url)
        except Exception as e:
          print("Error connecting to server")


def right(rightNum):
    if rightNum <= 0:
        console.append('Improper right input of ' + str(rightNum) + '. Please try again.')
    else:
        if rightNum == 1:
            console.append('Turning right once.')
            rightDirection(rightNum)
        else:
            console.append('Turning right ' + str(rightNum) + ' times.')
            rightDirection(rightNum)
        url = RIGHT_URL % rightNum
        try:
          response = requests.get(url)
          if response.status_code != 200:
            print("Something went wrong " + url)
        except Exception as e:
          print("Error connecting to server")
        url = "http://192.168.1.72:5000/stop"
        try:
          response = requests.get(url)
          if response.status_code != 200:
            print("Something went wrong " + url)
        except Exception as e:
          print("Error connecting to server")


def left(leftNum):
    if leftNum <= 0:
        console.append('Improper left input of ' + str(leftNum) + '. Please try again.')
    else:
        if leftNum == 1:
            console.append('Turning left once.')
            leftDirection(leftNum)
        else:
            console.append('Turning left ' + str(leftNum) + ' times.')
            leftDirection(leftNum)
        url = LEFT_URL % leftNum
        try:
          response = requests.get(url)
          if response.status_code != 200:
            print("Something went wrong " + url)
        except Exception as e:
          print("Error connecting to server")
        url = "http://192.168.1.72:5000/stop"
        try:
          response = requests.get(url)
          if response.status_code != 200:
            print("Something went wrong " + url)
        except Exception as e:
          print("Error connecting to server")


# Image Direction
def forwardBackwardDirection():
    global directional
    if directional == '':
        directional = 'icons8-up-94.png'

def rightDirection(turns):
    global directional
    if turns == 0:
        return
    if turns % 4 == 0:
        rightDirection(turns - 4)
        return
    if turns % 2 == 0:
        if directional == 'icons8-up-94.png':
            directional = 'icons8-down-94.png'
        elif directional == 'icons8-down-94.png':
            directional = 'icons8-up-94.png'
        elif directional == 'icons8-right-94.png':
            directional = 'icons8-left-94.png'
        elif directional == 'icons8-left-94.png':
            directional = 'icons8-right-94.png'
        rightDirection(turns - 2)
    else:
        if directional == 'icons8-down-94.png':
            directional = 'icons8-left-94.png'
        elif directional == 'icons8-left-94.png':
            directional = 'icons8-up-94.png'
        elif directional == 'icons8-right-94.png':
            directional = 'icons8-down-94.png'
        else:
            directional = 'icons8-right-94.png'
        leftDirection(turns - 1)

def leftDirection(turns):
    global directional
    if turns == 0:
        return
    if turns % 4 == 0:
        leftDirection(turns - 4)
        return
    if turns % 2 == 0:
        if directional == 'icons8-up-94.png':
            directional = 'icons8-down-94.png'
        elif directional == 'icons8-down-94.png':
            directional = 'icons8-up-94.png'
        elif directional == 'icons8-right-94.png':
            directional = 'icons8-left-94.png'
        elif directional == 'icons8-left-94.png':
            directional = 'icons8-right-94.png'
        leftDirection(turns - 2)
    else:
        if directional == 'icons8-down-94.png':
            directional = 'icons8-right-94.png'
        elif directional == 'icons8-left-94.png':
            directional = 'icons8-down-94.png'
        elif directional == 'icons8-right-94.png':
            directional = 'icons8-up-94.png'
        else:
            directional = 'icons8-left-94.png'
        leftDirection(turns - 1)

# General Run
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)  # Changed port to 8000 from default (5000)
