# CAMERA
import picamera
# TEMPERATURE AND HUMIDITY SENDER
import Adafruit_DHT
# LED
import RPi.GPIO as GPIO
# TIME
import time
import datetime
# PARAMETERS
import sys
# FTP
import ftplib
# FILE
import os
# api cherrypy
import cherrypy
import random
import string
import json

#LED SETUP
pin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)

#CAMERA
camera = picamera.PiCamera()

currenttemp = 0
targettemp = 0
lasttemp = 0
lasttime = time.time()
active = False

def getCurrentTemp():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
        if humidity is not None and temperature is not None:
            return str(int(temperature))

def setCurrentTemp():
    global currenttemp
    global temptime
    global lasttemp
    # // for simulation //
    lasttemp = currenttemp
    currenttemp = lasttemp + 1
    return
    # // for simulation //
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
        if humidity is not None and temperature is not None:
            currenttemp = int(temperature)
            lasttime = time.time()
            break

def getWhenDone():
    global active
    if active:
        global currenttemp
        global targettemp
        global lasttime
        global lasttemp
        setCurrentTemp()
        takePicture()
        if(currenttemp == targettemp):
            ledOff()
            active = False
            return '{"whendone":"now"}'
        currenttime = time.time()
        last = lasttemp
        tempdif = currenttemp-lasttemp
        timedif = currenttime-lasttime
        k = tempdif / timedif
        if k == 0 or k < 0:
            return '{"heat":"increase"}'
        donetime = (targettemp - currenttemp)/k + currenttime
        lasttemp = currenttemp
        lasttime = currenttime
        return '{"targettemp":"'+str(targettemp)+'","curremtemp":"'+str(currenttemp)+'","currenttime":"'+datetime.datetime.fromtimestamp(int(currenttime)).strftime('%Y-%m-%d %H:%M:%S')+'","whendone":"'+datetime.datetime.fromtimestamp(int(donetime)).strftime('%Y-%m-%d %H:%M:%S')+'","lasttemp":"'+str(last)+'","tempdif":"'+str(tempdif)+'","timedif":"'+str(timedif)+'","k":"'+str(k)+'"}'

def takePicture():
    global camera
    camera.capture('/home/pi/saunavahti/images/img.jpg')
    return "Picture taken"

def startSaunavahti():
    global active
    global lasttemp
    global lasttime
    global currenttemp
    if active is False:
        active = True
        ledOn()
        currenttemp = int(getCurrentTemp())
        lasttemp = currenttemp
        return '{"result":"saunavahti started, target temperature is '+str(targettemp)+'"}'
    else:
        return '{"result":"sauna is already active"}'

def ledOn():
    GPIO.output(pin,GPIO.HIGH)

def ledOff():
    GPIO.output(pin,GPIO.LOW)
    
@cherrypy.expose
class saunavahti(object):

    def GET(self):
        return '<html><body>'+getCurrentTemp()+'<br><img src="images/img.jpg"></body></html>'
    
    @cherrypy.tools.accept(media='application/json')
    def POST(self):
        global targettemp
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)
        if 'whendone' in body:
                return getWhenDone()
        if 'start' and 'target' in body:
            targettemp = int(body['target'])
            return startSaunavahti()
        if 'settarget' in body:
            if(len(body['settarget'])<3):
                targettemp = int(body['settarget'])
                return '{"result":"target temperature is now '+str(targettemp)+'"}'
        if 'led' in body:
            if(body['led']=='on'):
                ledOn()
                return '{"result":"led is on"}'
            if(body['led']=='off'):
                ledOff()
                return '{"result":"led is off"}'
        if 'picture' in body:
            if(body['picture']=='take'):
                return '{"result":"'+takePicture()+'"}'
        return "mee pois"
    


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        },
        '/images': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(current_dir, 'images')}
    }
    cherrypy.config.update( {'server.socket_host': '0.0.0.0'} )
    cherrypy.quickstart(saunavahti(), '/', conf)