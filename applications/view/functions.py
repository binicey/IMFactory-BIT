from fileinput import filename
from tkinter import Frame
import requests as RQ
from flask import render_template,Response,request,jsonify,make_response
from flask_login import login_required, current_user
from sqlalchemy import desc
from datetime import timedelta
import datetime
import shutil
from .yolo import AIDprocesser
from .yolo.core import main
import cv2

from common.utils.rights import permission_required, view_logging_required
from models import LogModel, RoleModel, UserModel
from . import index_bp
import os
from .yolo.camera import Camera
frame=''

# 称重计数
@index_bp.get('/weight/info')
@view_logging_required
@permission_required("weight:info")
def weight_and_count():
    return render_template('admin/functions/weight.html')

#缺陷检测
@index_bp.get('/defeat/info')
@view_logging_required
@permission_required("defeat:info")
def defeat_detact():
    return render_template('admin/functions/defeat.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        global frame
        frame,json = camera.get_frame()

        # print(type(frame))
        yield (b'--frame\r\n'+
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            # +
            # b'--frame\r\n'
            # b'Content-Type: application/json\r\n\r\n' + json.encode() + b'\r\n'
            )

#视频流路由
@index_bp.get('/defeat/video')
# @view_logging_required
# @permission_required("defeat:info")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    img=gen(Camera())
    return Response(img,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

ALLOWED_EXTENSIONS = set(['png', 'jpg','jpeg'])
UPLOAD_FOLDER = r'./uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#检测文件上传
@index_bp.route('/defeat/upload', methods=['GET', 'POST'])
def upload_file():
    #创建文件夹
    os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/')
    files = [
        'uploads', 'tmp/ct', 'tmp/draw',
        'tmp/image', 'tmp/mask', 'tmp/uploads'
    ]
    for ff in files:
        if not os.path.exists(ff):
            os.makedirs(ff)
    #获取文件
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(src_path)
        shutil.copy(src_path, './tmp/ct')
        os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/applications')
        return jsonify({'status': 1,
                        'filename':file.filename})

    return jsonify({'status': 200})


#远程图片下载
def getImage():
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    # }
    # r = RQ.get(img_url, stream=True)
    # print(r.raw)
    # print(r.status_code) # 返回状态码
    # print(r.content)
    # 截取图片文件名
    global frame
    img_name = str(datetime.datetime.now().isoformat())
    img_name=img_name.replace(':','-')
    img_name=img_name.replace('.','-')
    img_name+='.jpg'
    
    print(img_name)
    os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/')
    files = [
        'uploads', 'tmp/ct', 'tmp/draw',
        'tmp/image', 'tmp/mask', 'tmp/uploads'
    ]
    for ff in files:
        if not os.path.exists(ff):
            os.makedirs(ff)
    #获取文件
    if  allowed_file(img_name):
        src_path = os.path.join('./tmp/ct', img_name)
        print(src_path)
        print(os.getcwd())
        with open(src_path,'wb') as f:
            f.write(frame)
    os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/applications')
    return img_name



@index_bp.route('/defeat/result',methods=["GET"])
def detectImg():
    detectType=int(request.args.get('local'))
    detectName=request.args.get('filename')
    print(detectType)
    print(type(detectName))
    if detectType==1:
        os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/')
        image_path = os.path.join('./tmp/ct/', detectName)
        print(image_path)
        os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/applications')
        pid, image_info = main.c_main(
        image_path, AIDprocesser.Detector(), detectName.rsplit('.', 1)[1])
    elif detectType==0:
        detectName=getImage()
        os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/')
        image_path = os.path.join('./tmp/ct', detectName)
        os.chdir('/home/ros/ros/rosweb_ws/websrc/pear-admin-flask-mini/applications')
        pid, image_info = main.c_main(
        image_path, AIDprocesser.Detector(), detectName.rsplit('.', 1)[1])
    else:
        return jsonify({'status':200})
    return  jsonify({'status': 1,
                        'image_url': 'http://10.178.20.75:5000/tmp/ct/' + pid,
                        'draw_url': 'http://10.178.20.75:5000/tmp/draw/' + pid,
                        'pid':pid,
                        'image_info': image_info})


@index_bp.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response

#语音控制
@index_bp.get('/audio/info')
@view_logging_required
@permission_required("audio:info")
def audio_control():
    return render_template('admin/functions/audio.html')