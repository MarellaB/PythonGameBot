import ImageGrab
import win32api, win32con
import os
import time

# GLOBALS
# -------
x_pad = 984
y_pad = 230
# -------

def screenGrab():
    box = ()
    im = ImageGrab.grab([x_pad+1,y_pad+1,x_pad+640,y_pad+479])
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print "Click!"

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print "Left Down"

def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print "Left Release"

def mousePos(cord):
    win32api.SetCursorPos(x_pad + cord[0], y_pad + cord[1])

def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print x,y


def main():
    clicks = 0
    while clicks < 2 :
        get_cords()
        

if __name__ == '__main__':
    main()
