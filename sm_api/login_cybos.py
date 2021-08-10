import win32com.client
from pywinauto import application
import os
import time
import configparser

config = configparser.ConfigParser()
config.read('../config.ini', encoding='UTF8')
LOGIN = config['LOGIN']
ID = LOGIN.get("ID")
PW = LOGIN.get("PW")
CERT = LOGIN.get("CERT")


class LoginCybos:
    def __init__(self):
        self.g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')

    def kill_client(self):
        print("########## 기존 CYBOS 프로세스 강제 종료")
        os.system('taskkill /IM ncStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T')
        os.system('taskkill /IM DibServer* /F /T')
        os.system('wmic process where "name like \'%ncStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')

    def connect(self):
        if not self.connected():
            self.disconnect()
            self.kill_client()
            print("########## CYBOS 프로세스 자동 접속")
            app = application.Application()
            app.start(f'C:/Daishin/Starter\\ncStarter.exe /prj:cp /id:{ID} /pwd:{PW} /pwdcert:{CERT} /autostart')
        time.sleep(20)
        return True

    def connected(self):
        b_connected = self.g_objCpStatus.IsConnect
        if b_connected == 0:
            return False
        return True

    def disconnect(self):
        if self.connected():
            self.g_objCpStatus.PlusDisconnect()

    def waitForRequest(self):
        remainCount = self.g_objCpStatus.GetLimitRemainCount(1)
        if remainCount <= 0:
            time.sleep(self.g_objCpStatus.LimitRequestRemainTime / 1000)


if __name__ == '__main__':
    login_cybos = LoginCybos()
    login_cybos.connect()
