#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
from sqlite3.dbapi2 import connect
from threading import Thread
import sys, os, traceback
import asyncio
import websockets
import json
from log import logger
from OPTControllerPython.pyOPTcontroller import OPTController
from pyImageSourceCam import ImageSourceCam
import cv2, numpy as np
import base64


class PyServerAPI(object):
    def __init__(self, loop):
        self.users = set()
        self.opt = OPTController()
        self.cam = ImageSourceCam()
        self.loop = loop
        self.lastImage = None
        self.channelStates = [True, True, True, True]
        self.appRoot = None
        self.firstLoad = True

    async def register(self,websocket):
        self.users.add(websocket)
        logger.debug('new user connected: {}'.format(websocket))

    async def unregister(self,websocket):
        self.users.remove(websocket)
        logger.debug('user disconnected: {}'.format(websocket))

    async def handler(self,websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        async for message in websocket:
            try:
                # print(message)
                logger.debug(message)
                msg = json.loads(message)
                cmd = msg["cmd"]
                data = msg["data"]
                if cmd == 'pong':
                    print('client pong: {}'.format(data))
                elif cmd == 'init_server':
                    self.init_server(data)
                    await self.sendMsg(websocket,'reply_init_ok')
                elif cmd == 'grab':
                    t = Thread(target=self.grab, args=[websocket,])
                    t.start()
                elif cmd == 'snap':
                    t = Thread(target=self.snap, args=[websocket,])
                    t.start()
                elif cmd == 'grabStop':
                    self.stop_grab()
                elif cmd == 'connectController':
                    await self.connect_controller(websocket, data)
                elif cmd == 'change_intensity':
                    await self.change_intensity(websocket, data['channelIndex'], data['intensity'])
                elif cmd == 'enable_channel':
                    await self.enable_channel(websocket, data['channelIndex'])
                elif cmd == 'saveSetting':
                    await self.saveSetting(data)
                elif cmd == 'saveImage':
                    await self.saveImage(data)
                elif cmd == 'close':
                    self.close()
                    await self.sendMsg(websocket,'reply_closed_all')
            except Exception as e:
                try:
                    err_msg = traceback.format_exc()
                    logger.debug(err_msg)
                    await self.sendMsg(websocket,'reply_server_error',{'error':err_msg})
                except:
                    logger.debug('error during excetipn handling')
                    logger.debug(e)

    async def sendMsg(self, websocket, cmd, data=None):
        msg = {'cmd': cmd, 'data': data}
        filter_cmd = ['update_cur_status', 'pong']
        if cmd not in filter_cmd:
            pass
            # logger.debug('server sent msg: {}'.format(msg))
        try:
            await websocket.send(json.dumps(msg))
        except Exception as e:
            err_msg = traceback.format_exc()
            logger.debug(err_msg)

    def init_server(self, appRoot):
        self.appRoot = appRoot
        self.channelStates = [True, True, True, True]
        self.firstLoad = True

    def encode_image(self, image):
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, imgencode = cv2.imencode('.jpg', image, encode_param)
        encoded_string = base64.b64encode(imgencode).decode()
        return encoded_string

    def snap(self, websocket):
        try:
            self.stop = False
            self.cam.open()
            self.cam.config()
            self.cam.start()
            image = self.cam.snap()
            self.lastImage = image.copy()
            encoded_string = self.encode_image(image)
            future = asyncio.run_coroutine_threadsafe(self.sendMsg(websocket,'reply_image',{'image':encoded_string}), self.loop)
            future.result()
            self.cam.close()
        except:
            err_msg = traceback.format_exc()
            future = asyncio.run_coroutine_threadsafe(self.sendMsg(websocket,'reply_get_image_error',{'error':err_msg}), self.loop)
            future.result()
        finally:
            self.stop = True

    def grab(self, websocket):
        try:
            self.stop = False
            self.cam.open()
            self.cam.config()
            self.cam.start()
            image = None
            while not self.stop:
                image = self.cam.snap()
                self.lastImage = image.copy()
                encoded_string = self.encode_image(image)
                future = asyncio.run_coroutine_threadsafe(self.sendMsg(websocket,'reply_image',{'image':encoded_string}), self.loop)
                future.result()
                asyncio.sleep(0.05)
            self.cam.close()
        except:
            err_msg = traceback.format_exc()
            asyncio.run_coroutine_threadsafe(self.sendMsg(websocket,'reply_get_image_error',{'error':err_msg}), self.loop)
        finally:
            self.stop = True

    def stop_grab(self):
        self.stop = True
    
    async def connect_controller(self, websocket, ip):
        try:
            errorCode, errorMsg = self.opt.close()
        except:
            pass
        errorCode, errorMsg = self.opt.open(ip)
        connected = False
        if errorCode == 0:
            connected = True        
        await self.sendMsg(websocket,'reply_connect_controller', connected)
        if connected:
            if self.firstLoad:
                await self.loadSetting(websocket)
            await self.read_all_intensity(websocket)
            await self.read_all_ch_state(websocket)
    
    async def read_all_intensity(self, websocket):
        intensityArr = []
        for i in range(4):
            intensity = self.opt.readIntensity(i+1)
            intensityArr.append(intensity)
        await self.sendMsg(websocket,'reply_read_all_intensity', intensityArr)

    async def read_all_ch_state(self, websocket):
        await self.sendMsg(websocket,'reply_read_all_ch_state', self.channelStates)

    async def change_intensity(self, websocket, channelIndex, intensity):
        errorCode, errorMsg = self.opt.setIntensity(channelIndex,intensity)
        await self.read_all_intensity(websocket)

    async def enable_channel(self, websocket, channelIndex):
        targetState = not self.channelStates[channelIndex-1]
        if targetState == True:
            errorCode, errorMsg = self.opt.turnOnChannel(channelIndex)
            self.channelStates[channelIndex-1] = targetState
        else:
            errorCode, errorMsg = self.opt.turnOffChannel(channelIndex)
            self.channelStates[channelIndex-1] = targetState
        await self.read_all_ch_state(websocket)

    async def loadSetting(self,websocket):
        path = os.path.join(self.appRoot, 'config.json')
        with open(path, 'r', encoding='utf-8') as outfile:
            data = json.load(outfile)
        intensityArr = data['intensityArr']
        await self.sendMsg(websocket,'reply_loadSetting', intensityArr)

    async def saveSetting(self, appRoot):
        path = os.path.join(appRoot, 'config.json')
        intensityArr = []
        for i in range(4):
            intensity = self.opt.readIntensity(i+1)
            intensityArr.append(intensity)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'intensityArr': intensityArr}, f, ensure_ascii=False, indent=4)

    async def saveImage(self, appRoot):
        path = os.path.join(appRoot, 'image.png')
        cv2.imwrite(path, self.lastImage)

    def close(self):
        try:
            self.stop_grab = True
            self.cam.close()
        except:
            pass
        try:
            self.opt.close()
        except:
            pass

def main():
    loop = asyncio.get_event_loop()
    sokObj = PyServerAPI(loop)
    port=8023
    addr = 'tcp://127.0.0.1:{}'.format(port)
    print('start running on {}'.format(addr))

    start_server = websockets.serve(sokObj.handler, "127.0.0.1", port, ping_interval=30)
    loop.run_until_complete(start_server)
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()