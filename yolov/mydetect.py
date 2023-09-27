import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import sys
sys.path.insert(0, './yolov')

from .models.experimental import attempt_load
from .utils.datasets import LoadStreams, LoadImages
from .utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from .utils.plots import plot_one_box
from .utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel


def detect(image,model):

    torch.no_grad()
    save_img=False
    print(image)
    source="./media/"+str(image)
    weights='./best.pt'
    view_img=True
    save_txt=False
    imgsz=640
    device=''
    conf_thres=0.6
    iou_thres=0.7
    #trace = 

    # Initialize
    set_logging()
    device = select_device(device) #default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    
    #model = attempt_load(weights, map_location=device)  # load FP32 model
    
    stride = int(model.stride.max())  # model stride
    
    imgsz = check_img_size(imgsz, s=stride)  # check img_size

    #if trace:
     #   model = TracedModel(model, device, opt.img_size)
    classify = False
    if half:
        model.half()  # to FP16

    dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    names=[ 'luminaria','postacion'] #invierto las classes por que se entreno mal
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
    colors = [[255, 51, 51], [155, 153, 51]]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Warmup
        if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            for i in range(3):
                model(img, augment=False)[0]

        # Inference
        t1 = time_synchronized()
        with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
            pred = model(img, augment=False)[0]
        t2 = time_synchronized()

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False)
        t3 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, model, img, im0s)

        origen=[]
        fin=[]
        objectlabel=[]
        # Process detections
        for i, det in enumerate(pred):  # detections per image
            #if webcam:  # batch_size >= 1
             #   p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            #else:
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            #
            gn = torch.tensor((1,1,3))[[1, 0, 1, 0]]  # normalization gain whwh
    
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xyxy, conf) if False else (cls, *xyxy)  # label format
                        print(xyxy)
                        #with open(txt_path + '.txt', 'a') as f:
                         #   print(('%g ' * len(line)).rstrip() % line + '\n')
                          #  f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or view_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        labelOnly =f'{names[int(cls)]}'
                        tuplaOrigen,tuplaFin=plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=5)
                        origen+=[tuplaOrigen]
                        fin+=[tuplaFin]
                        objectlabel+=[labelOnly]
                        print (im0.shape)

            print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')

 
            #alto=1000
            #ancho=1333
            #cv2.namedWindow('ObjetoDetectado',cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('ObjetoDetectado',alto,ancho)
            #cv2.imshow("ObjetoDetectado", im0)
            #cv2.waitKey()  # 1 millisecond
    #print(origen,fin)
    objects = []
    for tuplaOrigen,tuplaFin in zip(origen,fin):
        y_origen,x_origen =tuplaOrigen
        y_fin,x_fin =tuplaFin
        y = x_origen  # Primer elemento de la tupla
        x = y_origen  # Segundo elemento de la tupla
        h= round(abs(x_fin-x_origen))
        w=round(abs(y_fin-y_origen))
        #print(x,y,w,h)
        obj = MyObjectRois(x,y,w,h)
        objects.append(obj)
  
    return im0,objects,objectlabel   

class MyObjectRois:
    def __init__(self, x, y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

                

