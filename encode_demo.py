#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# FIXME, we the encode of cv2 is surprisingly quick, 

import sys
import cv2
import time
import numpy as np

sys.path.append('./build')
import GPUJPEG_Encoder

in_f='./images/a.png'

im = cv2.imread(in_f)

# gpu_encoder = GPUJPEG_Encoder.Encoder()
# gpu_encoder = GPUJPEG_Encoder.Encoder(1280, 720, 0)
# gpu_encoder = GPUJPEG_Encoder.Encoder(width=1280, height=720, device_id=0)
gpu_encoder = GPUJPEG_Encoder.Encoder(height=720, width=1280)

N = 100

t0 = time.perf_counter()
for _ in range(N):
    buf = gpu_encoder.encode(im)
print(f'GPU time used:{(time.perf_counter()-t0)*1000: .2f} ms')

print(type(buf[0]))

buf_npy = np.array(buf, dtype=np.uint8, copy=False).reshape(-1, 1)
# im_b2 = cv2.imdecode(buf_npy, cv2.IMREAD_COLOR)
im_b2 = cv2.imdecode(buf_npy, cv2.IMREAD_UNCHANGED)
im_b2 = cv2.cvtColor(im_b2, cv2.COLOR_RGB2BGR)
cv2.imwrite('gpu_im.jpg', im_b2)

t0 = time.perf_counter()
for _ in range(N):
    buf_npy = cv2.imencode('.jpg', im)[1]
print(f'CV2 time used:{(time.perf_counter()-t0)*1000: .2f} ms')

buf_npy = np.array(buf_npy)
# im_b = cv2.imdecode(buf_npy, cv2.IMREAD_COLOR)
im_b = cv2.imdecode(buf_npy, cv2.IMREAD_UNCHANGED)
cv2.imwrite('cv2_im.jpg', im_b)

# print(im_b.shape)
# print(im_b2.shape)