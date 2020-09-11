import tkinter as tk
import os, webbrowser, serial, datetime, time, threading, cv2, json, ipfshttpclient
import pyqrcode

from web3 import Web3
import numpy as np
from pyzbar.pyzbar import decode
from datetime import datetime
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

ganach_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganach_url))
web3.eth.defaultAccount = web3.eth.accounts[0]
address = web3.toChecksumAddress("0x781c8b73d2d0a978d9b1a0f5054aaf48f495f79b")
abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"_t","type":"uint256"}],"name":"addtime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"z","type":"string"}],"name":"checkname","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"comferm","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"z","type":"string"}],"name":"deluser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_x","type":"uint256"}],"name":"getphoto1","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getphoto2","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getphototime","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getworkt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"photoNumb","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"setname","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_fi","type":"string"},{"internalType":"string","name":"_time","type":"string"}],"name":"setphoto","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
contract = web3.eth.contract(address=address, abi=abi)
ser = serial.Serial('/dev/ttyACM0', 19200, timeout=5)


def enter():
    cn = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    f = True
    nstr = 0
    while f and cn < 100:
        sleep(0.1)
        cn += 1
        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            print(myData)
            if len(myData) > 3:
                f = False
                nstr = 1

            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 255), 2)

        cv2.imshow('Result', img)
        cv2.waitKey(1)
    cap.release()  #################
    cv2.destroyAllWindows()
    if nstr == 0:
        return '0'
    else:
        return myData


# def backend1():


def backend():
    while 1:
        cont = 0
        t1 = 0
        t2 = 0

        while 1:

            x = ser.readline().decode("UTF-8")
            if 'Motion1' in x:
                time.sleep(2)
                # print(x)
                cv2.namedWindow("preview")
                vc = cv2.VideoCapture(0)
                if vc.isOpened():  # try to get the first frame
                    rval, frame = vc.read()
                else:
                    rval = False

                    # while rval:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow("preview", gray)
                rval, frame = vc.read()
                cv2.imwrite('img1s.png', gray)
                key = cv2.waitKey(20)
                # if key == 27: # exit on ESC
                #  break
                time.sleep(3)
                vc.release()  #########
                cv2.destroyAllWindows()  ########

                client = ipfshttpclient.connect('/dns/ipfs.infura.io/tcp/5001/https')
                res = client.add('img1s.png')
                tx_hash = contract.functions.setphoto(res['Hash'], str(datetime.now())).transact()
                os.remove("img1s.png")
                # tx_hash = contract.functions.setphoto('QmdoNEKfPcCNct6gQFqQa9J4QTFaUsPcs3yLdsB4dqeJnd', str(datetime.now())).transact()
                print('ipfs')
                print(res['Hash'])
                tx_hash = contract.functions.addtime(2).transact()

                nz = enter()
                if len(nz) < 2:
                    flag = False
                else:
                    tx_hash = contract.functions.checkname(nz).transact()
                    print(contract.functions.comferm().call())
                    flag = contract.functions.comferm().call()
                if flag == True:

                    # print (ser.readline())
                    time.sleep(2)
                    ser.write(b"tt\n")
                    zz = ser.readline()

                elif flag == False:

                    # print (ser.readline())
                    time.sleep(2)
                    ser.write(b"ff\n")
                    zz = ser.readline()
            if 'lon' in x:
                cont += 1

                if cont % 2 == 1:
                    t1 = time.time()
                    print('t1={}'.format(t1))
                elif cont % 2 == 0 and t1 > 0:
                    t2 = time.time()
                    print('t2={}'.format(t2))
                    wtime = int(t2 - t1)  # will add to chian
                    tx_hash = contract.functions.addtime(int(wtime)).transact()
                    wt = wtime
                    print('time : {}'.format(wt))
                    t1 = 0
                    cont = 0
    ser.close()


def bb():
    ser.close()
    return os._exit(0)


def gui():
    def p_btn2():
        n = entery1.get()
        tx_hash = contract.functions.getphoto1(int(n)).transact()
        urlh = contract.functions.getphoto2().call()
        y = 'https://ipfs.infura.io/ipfs/'
        z = y + urlh
        timex = contract.functions.getphototime().call()
        timestr = "Log Date-Time: {}".format(timex)
        webbrowser.open_new_tab(z)
        sdate.config(text=timestr)
        sdate.grid(row=4, column=3)

    def photo():
        tx = contract.functions.photoNumb().call()
        lblphoto.config(text=tx)
        lblphoto.grid(row=3, column=2)
        return tx

    def p_btn1():
        n = int(contract.functions.getworkt().call())
        t = int(n)

        day = t // 86400
        hour = (t - (day * 86400)) // 3600
        minit = (t - ((day * 86400) + (hour * 3600))) // 60
        seconds = t - ((day * 86400) + (hour * 3600) + (minit * 60))
        print(day, 'days', hour, ' hours', minit, 'minutes', seconds, ' seconds')
        lpow = n * 0.072 * 3
        cal =(lpow*74.88)/129.9
        st = "power used with 3 lamp :{:.2f} Watt consumption: {:.2f} Watt".format(lpow,cal)
        #sdate.config(text=st)
        sdate.config(text="Report Upon")
        sdate.grid(row=8, column=1)
        lbl10.config(text="Demo Lamp")
        lbl10.grid(row=8, column=2)

        lbl11.config(text="Regular Case ")
        lbl11.grid(row=9, column=1)
        lbl13.config(text="{:.2f} w".format(lpow))
        lbl13.grid(row=9, column=2)

        lbl12.config(text="With BLockchain ")
        lbl12.grid(row=10, column=1)

        lbl14.config(text="{:.2f} w".format(cal))
        lbl14.grid(row=10, column=2)

    def p_btn():
        n = entery.get()
        #if len(n) >2:
        qr = pyqrcode.create(n)
        tx_hash = contract.functions.setname(n).transact()
        qr.png('testqr.png', scale=8)
        email = enterye.get()

        email_user = "ur email@gmail.com"
        email_password = "ur password"
        email_send = str(email)

        subject = 'ur QRcode'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = 'Hi there, sending this email from home access system!'
        msg.attach(MIMEText(body, 'plain'))

        filename = 'testqr.png'
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text)
        server.quit()
        os.remove("testqr.png")

    def p_del():
        n = entery.get()
        tx_hash = contract.functions.deluser(n).transact()

    root = tk.Tk()
    root.geometry("730x340")
    lbl = tk.Label()
    lblphoto = tk.Label()
    lbl0 = tk.Label()
    lbl0.config(text='Access Control ')
    lbl0.grid(row=0, column=1)
    lbl1 = tk.Label()
    lbl1.config(text=' Using Blockchain')
    lbl1.grid(row=0, column=2)
    lbl2 = tk.Label()
    lbl2.config(text='Enter Name')
    lbl2.grid(row=1, column=0)
    entery = tk.Entry(width=15)
    entery.grid(row=1, column=1)
    enterye = tk.Entry(width=20)
    lbl3 = tk.Label()
    lbl3.config(text='Enter Email')
    lbl3.grid(row=1, column=2)
    enterye.grid(row=1, column=3)
    btn1 = tk.Button(text="Grant User", command=p_btn)
    btn1.grid(row=2, column=1)
    btn2 = tk.Button(text="Revoke User", command=p_del)
    btn2.grid(row=2, column=2)


    spow = tk.Label()

    btn4 = tk.Button(text="Number of Photos", command=photo)
    btn4.grid(row=3, column=0)
    lbl4 = tk.Label()
    lbl4.config(text='You have ')
    lbl4.grid(row=3, column=1)
    lbl5 = tk.Label()
    lbl5.config(text='Photos')
    lbl5.grid(row=3, column=3)
    lbl6 = tk.Label()
    lbl6.config(text='Enter Photo Number')
    lbl6.grid(row=4, column=0)
    entery1 = tk.Entry(width=5)
    entery1.grid(row=4, column=1)
    btn4 = tk.Button(text="Search", command=p_btn2)
    btn4.grid(row=4, column=2)
    sdate = tk.Label()

    lbl8 = tk.Label()
    lbl8.config(text='Energy Conservation ')
    lbl8.grid(row=7, column=1)
    lbl9 = tk.Label()
    lbl9.config(text=' Using Blockchain')
    lbl9.grid(row=7, column=2)

    btn3 = tk.Button(text="show power", command=p_btn1)
    btn3.grid(row=8, column=0)
    lbl10 = tk.Label()

    lbl11 = tk.Label()
    lbl12 = tk.Label()
    lbl13 = tk.Label()
    lbl14 = tk.Label()

    btn = tk.Button(text="Exit", command=bb)
    btn.grid(row=10, column=3)
    # backend()
    print(1)

    lbl71 = tk.Label()
    lbl71.config(text='==========')
    lbl71.grid(row=5, column=0)
    lbl72 = tk.Label()
    lbl72.config(text='=============')
    lbl72.grid(row=5, column=1)
    lbl73 = tk.Label()
    lbl73.config(text='===========')
    lbl73.grid(row=5, column=2)
    lbl74 = tk.Label()
    lbl74.config(text='=========================')
    lbl74.grid(row=5, column=3)
    lbl711 = tk.Label()
    lbl711.config(text='==========')
    lbl711.grid(row=6, column=0)
    lbl721 = tk.Label()
    lbl721.config(text='=============')
    lbl721.grid(row=6, column=1)
    lbl731 = tk.Label()
    lbl731.config(text='===========')
    lbl731.grid(row=6, column=2)
    lbl741 = tk.Label()
    lbl741.config(text='=========================')
    lbl741.grid(row=6, column=3)

    root.mainloop()


x = threading.Thread(target=backend).start()
gui()



