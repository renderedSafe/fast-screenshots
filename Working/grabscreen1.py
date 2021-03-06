# Done by Frannecklp

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
from multiprocessing import Process, Pool


def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()
    print(Process.pid)
    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    print(np.shape(img))

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

x = 0
y = 0
w = 1919
h = 1120
slice_height = int(h/3)
slice_top = (x, y, w, slice_height)
slice_middle = (x, slice_height, w, slice_height)
slice_bottom = (x, (2*slice_height), w, slice_height)

if __name__ == '__main__':
    pool = Pool(processes=3)
    slice_tuple = pool.map(grab_screen, (slice_top, slice_middle, slice_bottom,))
    stitched_image = np.vstack(slice_tuple)
    print(np.shape(stitched_image))
    cv2.imshow('window', stitched_image)
