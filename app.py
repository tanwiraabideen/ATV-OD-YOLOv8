import argparse
import io
from PIL import Image
import datetime

import torch
import cv2
import numpy as np
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, Response
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
from subprocess import Popen
import re
import requests
import shutil
import time
import glob
import webbrowser


from ultralytics import YOLO

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/front-wheel')
def frontWheel():
    return render_template('front-wheel.html')

@app.route('/rear-wheel')
def rearWheel():
    return render_template('rear-wheel.html')

@app.route('/radiator-cap')
def radiatorCap():
    return render_template('radiator-cap.html')

@app.route('/oil-cap')
def oilCap():
    return render_template('oil-cap.html')



@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filepath = (f'uploads/{file.filename}')
    file.save(filepath)


    # SEPERATE THE BELOW INTO A SEPERATE FUNCTION-------------------


    # Loading the model
    model = YOLO('best.pt')

    # Run inference on the source
    results = model([filepath])  # list of Results objects

    # Extract class labels
    classes = ['']
    for box in results[0].boxes:
        class_id = int(box.cls)  # Get class ID
        class_label = results[0].names[class_id]  # Get class label from class ID
        print(f'Detected class: {class_label}')  # Print class label'''
        classes.append(class_label)
    front_wheel_count = 0
    rear_wheel_count = 0
    oil_cap_count = 0
    radiator_cap_count = 0
    for x in range(len(classes)):
        if classes[x] == 'front_wheel' and front_wheel_count == 0:
            webbrowser.open_new_tab('https://mail.google.com/')
            front_wheel_count = front_wheel_count + 1
        if classes[x] == 'rear_wheel' and rear_wheel_count == 0:
            webbrowser.open_new_tab('https://sites.google.com/view/classroom-workspace/')
            rear_wheel_count = rear_wheel_count + 1
        if classes[x] == 'radiator_cap' and radiator_cap_count == 0:
            webbrowser.open_new_tab('https://www.amazon.ae/')
            radiator_cap_count = radiator_cap_count + 1
        if classes[x] == 'oil_cap' and oil_cap_count == 0:
            webbrowser.open_new_tab('https://www.facebook.com/')
            oil_cap_count = oil_cap_count + 1
    return redirect('https://www.notion.so/')
