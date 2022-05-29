from applications.view.yolo.utils import datasets
import torch
import numpy as np
# from .models.experimental import attempt_load
from .utils.general import non_max_suppression, scale_coords
from .utils.augmentations import letterbox
from .utils.torch_utils import select_device
import cv2
from random import randint
import os
from .utils import torch_utils
from .utils.datasets import LoadImages

class Detector(object):

    def __init__(self):
        self.img_size = 640
        self.threshold = 0.4
        self.max_frame = 160
        self.stride=32
        self.init_model()

    def init_model(self):
        os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/applications/view/yolo')
        self.weights = './weights/defeat_yolov5s.pt'
        self.device =  torch_utils.select_device()
        model = torch.load(self.weights, map_location=self.device)['model']
        os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/')
        model.to(self.device).float().eval()

        self.half = True and self.device.type != 'cpu'
        print('half = ' + str(self.half))

        if self.half:
            model.half()
        # torch.save(model, 'test.pt')
        self.m = model

        self.names = model.module.names if hasattr(
            model, 'module') else model.names
        self.colors = [
            (randint(0, 255), randint(0, 255), randint(0, 255)) for _ in self.names
        ]

    def preprocess(self, path):
        # img = cv2.imread(path)
        # assert img is not None, f'Image Not Found {path}'
        # img0 = img.copy()
        # img = letterbox(img, new_shape=self.img_size,stride=self.stride,auto=True)[0]
        # img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        # img = np.ascontiguousarray(img)
        dataset=LoadImages(path,self.img_size)
        img_r=''
        img0=''
        for path, img, im0, vid_cap,s in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half()  if self.half else img.float()  # 半精度
            img /= 255.0  # 图像归一化
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
            img_r=img
            img0=im0

        return img0, img

    def plot_bboxes(self, image, bboxes, line_thickness=None):
        tl = line_thickness or round(
            0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # line/font thickness
        for (x1, y1, x2, y2, cls_id, conf) in bboxes:
            color = self.colors[self.names.index(cls_id)]
            c1, c2 = (x1, y1), (x2, y2)
            cv2.rectangle(image, c1, c2, color,
                          thickness=tl, lineType=cv2.LINE_AA)
            tf = max(tl - 1, 1)  # font thickness
            t_size = cv2.getTextSize(
                cls_id, 0, fontScale=tl / 3, thickness=tf)[0]
            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
            cv2.rectangle(image, c1, c2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(image, '{} ID-{:.2f}'.format(cls_id, conf), (c1[0], c1[1] - 2), 0, tl / 3,
                        [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        return image

    def detect(self, path):

        im0, img = self.preprocess(path)

        pred = self.m(img, augment=False)[0]
        pred = pred.float()
        pred = non_max_suppression(pred, self.threshold, 0.5,
                                                    classes=None, agnostic=False)

        pred_boxes = []
        image_info = {}
        count = 0
        for det in pred:
            if det is not None and len(det):
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], im0.shape).round()

                for *x, conf, cls_id in det:
                    lbl = self.names[int(cls_id)]
                    x1, y1 = int(x[0]), int(x[1])
                    x2, y2 = int(x[2]), int(x[3])
                    pred_boxes.append(
                        (x1, y1, x2, y2, lbl, conf))
                    count += 1
                    key = '{}-{:02}'.format(lbl, count)
                    image_info[key] = {'type':key,'size':'{}×{}'.format(
                        x2-x1, y2-y1),'location':'({},{})'.format((x2+x1)/2,(y2+y1)/2),'score': np.round(float(conf), 3)}

        im = self.plot_bboxes(im0, pred_boxes)
        
        return im, image_info