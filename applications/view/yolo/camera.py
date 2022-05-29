from email.mime import image
import os

from flask import jsonify

import cv2
from .base_camera import BaseCamera
import torch
import torch.nn as nn
import torchvision
import numpy as np
import argparse
from .utils.datasets import *
from .utils.general import *
from .utils.plots import *
from .utils import torch_utils

class Camera(BaseCamera):

    video_source = 'test.mp4'

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        video=cv2.VideoCapture(0)
        while True:
            ret,frame=video.read()
            json_data=''
            yield cv2.imencode('.jpg', frame)[1].tobytes(),json_data
    @staticmethod
    def frames_video():
        os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/applications/view/yolo')
        out, weights, imgsz = \
        './inference/output', 'weights/yolov5n.pt', 640
        source = 'test.png'
        device = torch_utils.select_device()
        if os.path.exists(out):
            shutil.rmtree(out)  # delete output folder
        os.makedirs(out)  # make new output folder

        # Load model
        # google_utils.attempt_download(weights)
        model = torch.load(weights, map_location=device)['model']
        
        model.to(device).float().eval()

        # Second-stage classifier
        classify = False
        if classify:
            modelc = torch_utils.load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'])  # load weights
            modelc.to(device).eval()

        # Half precision
        # half = False and device.type != 'cpu'
        half = True and device.type != 'cpu'
        print('half = ' + str(half))

        if half:
            model.half()

        # Set Dataloader
        vid_path, vid_writer = None, None
        dataset = LoadImages(source, img_size=imgsz)
        # dataset = LoadStreams(source, img_size=imgsz)
        names = model.names if hasattr(model, 'names') else model.modules.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

        # Run inference
        t0 = time.time()
        img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
        _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
        for path, img, im0s, vid_cap,s in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            t1 = torch_utils.time_sync()
            pred = model(img, augment=False)[0]
            
            # Apply NMS
            pred =non_max_suppression(pred, 0.4, 0.5,
                               classes=None, agnostic=False)
            t2 = torch_utils.time_sync()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            for i, det in enumerate(pred):  # detections per image
                p, s, im0 = path, '', im0s
                img_size=''
                det_class=''
                save_path = str(Path(out) / Path(p).name)
                s += '%gx%g ' % img.shape[2:]  # print string
                img_size='%gx%g ' % img.shape[2:]
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  #  normalization gain whwh
                if det is not None and len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                    
                    #for c in det[:, -1].unique():  #probably error with torch 1.5
                    for c in det[:, -1].detach().unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        
                        s += '%g %s, ' % (n, names[int(c)])  # add to string
                        det_class +='%g %s, ' % (n, names[int(c)])
                        
                    for *xyxy, conf, cls in det:
                        label = '%s %.2f' % (names[int(cls)], conf)
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
                print('%sDone. (%.3fs)' % (s, t2 - t1))
                time_interval=t2-t1
            os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/applications')
            # 
            
            #base64返回为byte，需要decode得到字符串
            json_data={"output": '%sDone. (%.3fs)' % (s, t2 - t1),"size":img_size,"det_class":det_class,"detect_time":time_interval,
                        }
            json_data=json.dumps(json_data)
            # print(json_data)
            yield cv2.imencode('.jpg', im0)[1].tobytes(),json_data