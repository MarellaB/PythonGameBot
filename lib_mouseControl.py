import win32api, win32con
import time

tempX = 984
tempY = 230

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    #Output click location
    #print "Click at {}".format(get_cords())


def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print "Left Down"


def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print "Left Release"

def clickAt(xPos, yPos):
    mousePos((xPos+tempX, yPos+tempY))
    time.sleep(.1)
    leftClick()


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))