import ImageGrab
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

def main():
    screenGrab()

if __name__ == '__main__':
    main()
