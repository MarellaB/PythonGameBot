import ImageGrab
import ImageOps
import lib_mouseControl
import time
from numpy import *

# WEBSITE =====
# http://www.miniclip.com/games/sushi-go-round/en/
# =============

# Variables
# -------
#The padding on left and top to know where the game is.
#MUST ALWAYS BE SET CORRECTLY AND MANUALLY!
x_pad = 984
y_pad = 230

#DEBUG FILE
debugLogFile = open("DEBUG_LOG.txt", 'w')
debugPostFile = open("DEBUG_POST.txt", 'w')

#Coordinates of materials
class Cord:
    f_shrimp = (34, 336)
    f_rice = (91, 334)
    f_nori = (43, 383)
    f_roe = (92, 391)
    f_salmon = (43, 442)
    f_unagi = (111, 812)

#What there is in stock, to know when to order and when not to
class Stock:
    shrimp = 5
    rice = 10
    nori = 10
    roe = 10
    salmon = 5
    unagi = 5

#Holds greyscale value of item, and name
sushiTypes = {1453:'onigiri',
              1710:'caliroll',
              1428:'salmonroll',
              1875:'shrimpsushi',
              1380:'maki'}
#What the background looks like, to know if there is a customer or not
Blank = [6108, 3307, 8555, 6666, 3881, 6399]
# -------

#Should be used for all output as logs to both debug file and the console
def debugLog(msg):
    print str(msg)
    debugLogFile.write(str(msg) + '\n')


def getPhoneAvail(x, y):
    box = (x_pad+x, y_pad+y, x_pad+x+2, y_pad+y+2)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    debugLog('Phone Check ({}, {}) = {}'.format(x, y, a))
    if a > 400:
        return 1
    else:
        return 0


#Checks if the mat is clear to add ingredients
def getMatClear():
    box = (x_pad+130, y_pad+309, x_pad+272, y_pad+460)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    if a == 22649:
        return 1
    else:
        return 0

#Checks if there is an order on the seat
def getSeat(seatNumber):
    #Where the bubble is that needs to be checked
    box = ((100*seatNumber)+11+26+x_pad, 17+y_pad+45, (100*seatNumber)+11+16+45+x_pad, 31+y_pad+45)
    #Sets image to greyscale to remove complications and allow same value to be parsed
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    debugLog(a)
    #Output Image
    #im.save(os.getcwd() + '\\seat_{}__'.format(seatNumber) + str(int(time.time())) + '.png')
    return a

#Used to order new stock when running low
def orderItem(item):
    delay = 0.2
    #Open Phone
    lib_mouseControl.clickAt(569, 366)
    time.sleep(0.2)
    debugLog('Ordered %s' % item)
    #Select Item and place order
    if item != 'rice':
        lib_mouseControl.clickAt(525,271)
        time.sleep(delay)
        if item == 'shrimp':
            if getPhoneAvail(457, 200) == 1:
                Stock.shrimp = Stock.shrimp + 5
                lib_mouseControl.clickAt(493,221)
            else:
                debugLog('Attempted order, unnavailable - shrimp')
        if item == 'unagi':
            if getPhoneAvail(539, 200) == 1:
                Stock.unagi += 5
                lib_mouseControl.clickAt(577,221)
            else:
                debugLog('Attempted order, unnavailable - unagi')
        if item == 'nori':
            if getPhoneAvail(457, 255) == 1:
                Stock.nori += 10
                lib_mouseControl.clickAt(493,278)
            else:
                debugLog('Attempted order, unnavailable - nori')
        if item == 'roe':
            if getPhoneAvail(539, 255) == 1:
                Stock.roe += 10
                lib_mouseControl.clickAt(577, 278)
            else:
                debugLog('Attempted order, unnavailable - roe')
        if item == 'salmon':
            if getPhoneAvail(457, 310) == 1:
                Stock.salmon += 5
                lib_mouseControl.clickAt(493,330)
            else:
                debugLog('Attempted order, unnavailable - salmon')
    elif item == 'rice':
        if getPhoneAvail(510, 252) == 1:
            lib_mouseControl.clickAt(544, 292)
            Stock.rice += 10
            time.sleep(delay)
            lib_mouseControl.clickAt(540, 294)
        else:
            debugLog('Attempted order, unnavailable - rice')
    debugLog('Stock:[Shrimp:{},Rice:{},Nori:{},Roe:{},Salmon:{},Unagi:{}]'.format(Stock.shrimp, Stock.rice, Stock.nori, Stock.roe, Stock.salmon, Stock.unagi))
    time.sleep(delay)
    lib_mouseControl.clickAt(486,294)

    
#Determines what is needed in the stock
def checkStock():
    debugLog("Checking Stock")
    if Stock.shrimp < 2:
        orderItem('shrimp')
    if Stock.unagi < 2:
        orderItem('unagi')
    if Stock.nori < 4:
        orderItem('nori')
    if Stock.roe < 4:
        orderItem('roe')
    if Stock.salmon < 2:
        orderItem('salmon')
    if Stock.rice < 5:
        orderItem('rice')
        

##Runs through and clears all plates across the table
def clearPlates():
    debugLog("Clearing Plates")
    lib_mouseControl.clickAt(78, 210)
    time.sleep(.05)
    lib_mouseControl.clickAt(174, 210)
    time.sleep(.05)
    lib_mouseControl.clickAt(272, 210)
    time.sleep(.05)
    lib_mouseControl.clickAt(373, 210)
    time.sleep(.05)
    lib_mouseControl.clickAt(486, 210)
    time.sleep(.05)
    lib_mouseControl.clickAt(576, 210)
    time.sleep(.05)

#Adds the specific amount of each material to the mat, removing it from stock
def selectItem(item, numberOf):
    a = 0
    debugLog("Using {} of {}".format(numberOf, item))
    while a < numberOf:
        a += 1
        if item == 'unagi':
            lib_mouseControl.clickAt(Cord.f_unagi[0], Cord.f_unagi[1])
            Stock.unagi -= 1
        if item == 'salmon':
            lib_mouseControl.clickAt(Cord.f_salmon[0], Cord.f_salmon[1])
            Stock.salmon -= 1
        if item == 'shrimp':
            lib_mouseControl.clickAt(Cord.f_shrimp[0], Cord.f_shrimp[1])
            Stock.shrimp -= 1
        if item == 'rice':
            lib_mouseControl.clickAt(Cord.f_rice[0], Cord.f_rice[1])
            Stock.rice -= 1
        if item == 'nori':
            lib_mouseControl.clickAt(Cord.f_nori[0], Cord.f_nori[1])
            Stock.nori -= 1
        if item == 'roe':
            lib_mouseControl.clickAt(Cord.f_roe[0], Cord.f_roe[1])
            Stock.roe -= 1
        time.sleep(.1)

#Holds recipies for sushi, and prepares them when needed
def makeSushi(item):
    #What is currently being produced
    debugLog("Making " + item)
    while getMatClear() == 0:
        debugLog('Waiting, mat busy')
        time.sleep(0.1)
    if item == 'onigiri':
        selectItem('rice', 2)
        selectItem('nori', 1)
    elif item == 'caliroll':
        selectItem('rice', 1)
        selectItem('nori', 1)
        selectItem('roe', 1)
    elif item == 'maki':
        selectItem('rice', 1)
        selectItem('nori', 1)
        selectItem('roe', 2)
    elif item == 'salmonroll':
        selectItem('rice', 1)
        selectItem('nori', 1)
        selectItem('salmon', 2)
    elif item == 'shrimpsushi':
        selectItem('rice', 1)
        selectItem('nori', 1)
        selectItem('shrimp', 2)
    #Rolls the mat, to finish the sushi
    lib_mouseControl.clickAt(206, 375)
    #Stops to let the game catch up ad have everything move off the mat
    time.sleep(0.2)
        
#Clears all beginning menus
def startGame():
    #Home Menu
    debugLog("Menu 1")
    lib_mouseControl.clickAt(313, 207)
    time.sleep(.1)

    #Iphone Menu
    debugLog("Menu 2")
    lib_mouseControl.clickAt(317, 373)
    time.sleep(.1)

    #Skip Menu
    debugLog("Menu 3")
    lib_mouseControl.clickAt(587, 458)
    time.sleep(.1)

    #Goal Menu
    debugLog("Menu 4")
    lib_mouseControl.clickAt(317, 373)
    time.sleep(.1)

#What still needs to be produced
needed = {
        'onigiri':0,
        'caliroll':0,
        'maki':0,
        'salmonroll':0,
        'shrimpsushi':0
    }

#When called, issues the order of making everything, clearing the 'needed' array
def prepareFood():
    checkStock()
    while needed['onigiri'] > 0:
        needed['onigiri'] -= 1
        checkStock()
        makeSushi('onigiri')
    while needed['caliroll'] > 0:
        needed['caliroll'] -= 1
        checkStock()
        makeSushi('caliroll')
    while needed['maki'] > 0:
        needed['maki'] -= 1
        checkStock()
        makeSushi('maki')
    while needed['salmonroll'] > 0:
        needed['salmonroll'] -= 1
        checkStock()
        makeSushi('salmonroll')
    while needed['shrimpsushi'] > 0:
        needed['shrimpsushi'] -= 1
        checkStock()
        makeSushi('shrimpsushi')

#Which customer has been helped, prevents doubling orders
#0 is waiting 1 is served
served = [0, 0, 0, 0, 0, 0]

#Checks all customer bubbles to see if anyone needs an order taken
def checkBubbles():
    #Where the computer is
    currentSeat = 0
    while currentSeat < 6:
        #Checks stock, always making sure to keep full
        checkStock()
        #Gets the current value of the bubble, and checks for matches
        s1 = getSeat(currentSeat)
        if s1 != Blank[currentSeat] & served[currentSeat] == 0:
            if sushiTypes.has_key(s1):
                served[currentSeat] = 1
                needed[sushiTypes[s1]] += 1
                debugLog('Table {} needs %s'.format(currentSeat) % sushiTypes[s1])
            else:
                debugLog('Sushi id %s not found!' % s1)
        else:
            served[currentSeat] = 0
        currentSeat += 1
    #Mass debug information
    debugLog('Served:[{},{},{},{},{},{}]'.format(served[0],served[1],served[2],served[3],served[4],served[5]))
    debugLog('Stock:[Shrimp:{},Rice:{},Nori:{},Roe:{},Salmon:{},Unagi:{}]'.format(Stock.shrimp, Stock.rice, Stock.nori, Stock.roe, Stock.salmon, Stock.unagi))
    debugLog('Needed:[Oni:{},Cali:{},Maki:{},Samo:{},Shri{}]'.format(needed['onigiri'],needed['caliroll'],needed['maki'],needed['salmonroll'],needed['shrimpsushi']))


def begin():
    startGame()
    i = 0
    while i < 17:
        debugLog('$=== Run# : %s || Level# : 1 ===$' % i)
        i += 1
        checkStock()
        checkBubbles()
        prepareFood()
        clearPlates()
        time.sleep(5)
        debugLog('$===============================$')
    time.sleep(5)
    clearPlates()
    time.sleep(10)
    #Congratulations Menu
    debugLog('Menu 5')
    lib_mouseControl.clickAt(317, 373)
    time.sleep(.1)
    #Goal 2 Menu
    debugLog('Menu 6')
    lib_mouseControl.clickAt(317, 373)
    time.sleep(.1)
    i = 0
    while i < 17:
        debugLog('$=== Run# : %s || Level# : 2 ===$' % i)
        i += 1
        checkStock()
        checkBubbles()
        prepareFood()
        clearPlates()
        time.sleep(5)
        debugLog('$===============================$')
    debugLogFile.close()
    debugPostFile.close()

def main():
    begin()

if __name__ == '__main__':
    main()