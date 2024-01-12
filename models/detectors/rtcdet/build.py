#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import torch
import torch.nn as nn

from .loss import build_criterion
from .rtcdet import RTCDet


# build object detector
def build_rtcdet(args, cfg, device, num_classes=80, trainable=False, deploy=False):
    print('==============================')
    print('Build {} ...'.format(args.model.upper()))
    
    print('==============================')
    print('Model Configuration: \n', cfg)
    
    # -------------- Build YOLO --------------
    model = RTCDet(cfg                = cfg,
                   device             = device, 
                   num_classes        = num_classes,
                   trainable          = trainable,
                   conf_thresh        = args.conf_thresh,
                   nms_thresh         = args.nms_thresh,
                   topk               = args.topk,
                   deploy             = deploy,
                   no_multi_labels    = args.no_multi_labels,
                   nms_class_agnostic = args.nms_class_agnostic
                   )

    # -------------- Initialize YOLO --------------
    for m in model.modules():
        if isinstance(m, nn.BatchNorm2d):
            m.eps = 1e-3
            m.momentum = 0.03    
            
    # -------------- Build criterion --------------
    criterion = None
    if trainable:
        # build criterion for training
        criterion = build_criterion(args, cfg, device, num_classes)
        
    return model, criterion