# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 14:38:33 2023
@author: USER
"""

# python C:\Users\USER\Desktop\STM32\upload_bin_func.py
# python C:\Users\USER\Documents\STM32\upload_bin_func.py

import sys
import time
import os

import numpy as np
import serial
import PyQt5
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtTest import *
# bin_file = "C:/Users/USER/Desktop/STM32/BIN.bin"
# bin_file = "C:/Users/USER/Desktop/STM32/BIN2_F413ZH.bin"

form_window = uic.loadUiType("UI_V2.ui")[0]

def progressbar_update(count):
    print("progressbar updating")
    try:
        for _ in range(50):
            QApplication.processEvents()

        print("뒤야")
        main_window.progressBar.setValue(count)

        print("앞이야")
        for _ in range(50):
            QApplication.processEvents()
    except:
        print("except")
        progressbar_update(count)

    print("progressbar updating end")

class main_threading(QThread):

    def run(self):
        while True:

            try:
                if main_func(main_window.bin_file, main_window.port, main_window.skip_checksum):
                    main_window.btn_done.setEnabled(True)
                    print("?")

                    break
                else:
                    print("?????")
                    main_window.text_label.setText("restart in 3 seconds")
                    print(main_window.port)
                    try:
                        serial.Serial(main_window.port).close()
                    except:
                        print("Serial not opened")
                    main_window.thread_stop()

                    # time.sleep(3)

            except Exception as E:
                print(E)

        # check_main_func = main_window.main_func(bin_file, port, skip_checksum)


global count
count = 0


class UiMainWindow(QtWidgets.QMainWindow, form_window):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Firmware Update")
        self.setupUi(self)
        self.bin_file = "BIN2_F413ZH.bin"
        self.port = "11"
        self.skip_checksum = False
        self.lineEdit.setText(self.bin_file)
        self.lineEdit_2.setText(self.port)

        self.progressBar.setMaximum(100)
        self.progressBar.setValue(count)

        self.btn_done.setEnabled(False)
        self.btn_done.clicked.connect(self.done_clicked)
        # self.btn_done.setDisabled(True)

        ###초기화 잘해주기

        self.setWindowFlags(self.windowFlags() | PyQt5.QtCore.Qt.WindowStaysOnTopHint)

    def File_Dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                  options=options)
        if fileName:
            print(fileName)
            self.lineEdit.setText(fileName)

    def closeEvent(self, event):
        try:
            if self.threading.isRunning():
                close = self.alert()
                if close == QMessageBox.Yes:
                    event.accept()
                else:
                    event.ignore()
        except:
            pass

    def alert(self):
        return QMessageBox.question(self, "Warning", "Are you sure want to quit?? \nYou might have a severe damage",
                                    QMessageBox.Yes, QMessageBox.No)

    def Ok_Clicked(self):
        self.threading = None
        try:
            print(self.threading)
            print(".threading 초기화")
        except:
            print(".threading None 초기화 안됨")

        self.bin_file = self.lineEdit.text()
        self.port = "COM" + self.lineEdit_2.text()
        if self.checkBox.checkState():
            self.skip_checksum = True

        QApplication.processEvents()
        main_window.buttonBox.setEnabled(False)
        QApplication.processEvents()
        print("threading 생성 확인")
        self.threading = main_threading(self)
        self.threading.start()
        print("threading 돌아가는중")

    def done_clicked(self):
        main_window.threading.quit()
        QApplication.processEvents()
        main_window.lineEdit.setText(main_window.bin_file)
        QApplication.processEvents()
        self.btn_done.setEnabled(False)
        QApplication.processEvents()
        main_window.buttonBox.setEnabled(True)
        QApplication.processEvents()

    def thread_stop(self):
        for _ in range(30):
            QApplication.processEvents()

        print("thread stop")
        QTest.qWait(3000)
        print("sleep end")

        for _ in range(30):
            QApplication.processEvents()

app = QtWidgets.QApplication(sys.argv)
main_window = UiMainWindow()

main_window.show()


def read_bin(bin_file):
    try:
        print("HHH")
        with open(bin_file, "rb") as f:
            contents = f.read()

        main_window.text_label.setText("Found")
        main_window.text_label.setText("Found .bin file (%s)" % bin_file)
        # main_window.thread_stop()
        print("어디까지?")
        # for i in range(len(contents) // 16):
        #    print("0x%08x: 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x" % (16*i, contents[16*i + 3], contents[16*i + 2], contents[16*i + 1], contents[16*i + 0], contents[16*i + 7], contents[16*i + 6], contents[16*i + 5], contents[16*i + 4], contents[16*i + 11], contents[16*i + 10], contents[16*i + 9], contents[16*i + 8], contents[16*i + 15], contents[16*i + 14], contents[16*i + 13], contents[16*i + 12]))
        # if len(contents) % 16 != 0:
        #    temp = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
        #    for i in range(16):
        #        if (len(contents) // 16) * 16 + i < len(contents):
        #            temp[i] = "%02x" % contents[(len(contents) // 16) * 16 + i]
        #    print("0x%08x: 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s" % ((len(contents) // 16) * 16, temp[3], temp[2], temp[1], temp[0], temp[7], temp[6], temp[5], temp[4], temp[11], temp[10], temp[9], temp[8], temp[15], temp[14], temp[13], temp[12]))

        # for i in range(len(contents) // 16):
        #     print("0x%08x: 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x" % (16*i, contents[16*i + 0], contents[16*i + 1], contents[16*i + 2], contents[16*i + 3], contents[16*i + 4], contents[16*i + 5], contents[16*i + 6], contents[16*i + 7], contents[16*i + 8], contents[16*i + 9], contents[16*i + 10], contents[16*i + 11], contents[16*i + 12], contents[16*i + 13], contents[16*i + 14], contents[16*i + 15]))
        if len(contents) % 16 != 0:
            temp = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
            for i in range(16):
                if (len(contents) // 16) * 16 + i < len(contents):
                    temp[i] = "%02x" % contents[(len(contents) // 16) * 16 + i]
            # print("0x%08x: 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s" % ((len(contents) // 16) * 16, temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15]))

        # crc = 0x00000000
        # for i in range(len(contents)):
        #    crc = crc + int(("0x%02x" % contents[i]), 16)
        #    crc = crc & 0xffffffff
        # print("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, len(contents) - 1, crc, len(contents)))


        crc = np.uint32(0x00000000)
        for i in range(len(contents)):
            crc = crc + np.uint32(int(("0x%02x" % contents[i]), 16))

        print("Not pass")
        QApplication.processEvents()
        main_window.text_label.setText(
            "Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, len(contents) - 1, crc, len(contents)))
        QApplication.processEvents()
        print("pass")
        if len(contents) % 128 == 0:
            num_128 = len(contents) // 128
        else:
            num_128 = (len(contents) // 128) + 1

        # crc_128 = 0x00000000
        # for i in range(num_128 * 128):
        #    if i < len(contents):
        #        crc_128 = crc_128 + int(("0x%02x" % contents[i]), 16)
        #    else:
        #        crc_128 = crc_128 + int(("0x%02x" % 0xff), 16)
        #    crc_128 = crc_128 & 0xffffffff
        # print("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, (num_128 * 128) - 1, crc_128, (num_128 * 128)))

        print("어디가 문제니0")
        crc_128 = np.uint32(0x00000000)
        for i in range(num_128 * 128):
            if i < len(contents):
                crc_128 = crc_128 + np.uint32(int(("0x%02x" % contents[i]), 16))
            else:
                crc_128 = crc_128 + np.uint32(int(("0x%02x" % 0xff), 16))

        print("어디가 문제니1")
        QApplication.processEvents()
        main_window.text_label.setText("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (
            0x00000000, (num_128 * 128) - 1, crc_128, (num_128 * 128)))
        QApplication.processEvents()
        print("어디가 문제니2")
        # main_window.thread_stop()

        print("pass out")
        return True, contents, crc, num_128, crc_128, print("Hihi")

    except:
        QApplication.processEvents()
        main_window.text_label.setText("Can not find .bin file (%s)" % bin_file)
        QApplication.processEvents()
        main_window.thread_stop()

        return False, b'', np.uint32(0x00000000), 0, np.uint32(0x00000000)


def open_serial(port):
    print(port) #여기부터 실행해서 확인해보기
    ser = None
    check_ser = None
    try:
        print("In")
        try:
            ser = serial.Serial(port)
        except:
            print("Serial 문제")
        print(ser)
        ser.baudrate = 115200
        print("Node1")
        QApplication.processEvents()
        main_window.text_label.setText("Opened %s" % port)
        QApplication.processEvents()
        print("Node 2")

        # main_window.thread_stop()
        print("Hi")
        check_ser = True
        # ser = ser
    except:
        print("Nope0")
        QApplication.processEvents()
        main_window.text_label.setText("Can not open %s" % port)
        QApplication.processEvents()
        print("Nope1")
        main_window.thread_stop()
        print("Nope2")
        check_ser = False
        ser = False
    print("bye")
    return check_ser, ser


def check_serial(check_ser, ser):
    data_dummy = None
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
            QApplication.processEvents()
            main_window.text_label.setText("%s is alive" % main_window.port)
            QApplication.processEvents()
            print("main_window.thread_stop()문제")
            # main_window.thread_stop()
            print("main_window.thread_stop()문제 맞는듯")

            check_ser = True
            print("pass here?")
        except:
            QApplication.processEvents()
            main_window.text_label.setText("%s is dead" % main_window.port)
            QApplication.processEvents()
            main_window.thread_stop()

            check_ser = False
    else:

        main_window.text_label.setText("Can not found serial port")

        main_window.thread_stop()

        # check_ser = False
    print("뭐지 도대체?")
    return check_ser


def close_serial(check_ser, ser):
    if check_ser == True:
        try:
            ser.close()

            main_window.text_label.setText("Closed %s" % ser.port)

            main_window.thread_stop()

            check_ser = False
        except:

            main_window.text_label.setText("Can not close serial port")

            main_window.thread_stop()

            check_ser = False
    else:

        main_window.text_label.setText("Can not found serial port")

        main_window.thread_stop()

        # check_ser = False

    return check_ser


def check_hse_frequency(check_ser, ser):
    print("check in")
    if check_ser == True:


        print("Truee")
        try:
            check_check_hse_frequency, check_check_hse_frequency_opt, data_dummy, request, response, prev_time, data_rx, data = [None for _ in range(8)]
            print(check_check_hse_frequency, check_check_hse_frequency_opt, data_dummy, request, response, prev_time, data_rx, data)
            print("In the try")
            data_dummy = b't0048ffffffffffffffff\r'
            print("In the try2")
            for i in range(16):
                print(i)
                ser.write(data_dummy)
                time.sleep(0.1)

            QApplication.processEvents()
            print("before ser while")
            while ser.in_waiting > 0:
                data_dummy = ser.read()
            print("ser while end")

            request = b't079100\r'
            print("befere for")
            QApplication.processEvents()
            for i in range(20):
                ser.write(request)

                time.sleep(0.05)
            print("after for")
            # main_window.text_label.setText("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)

            response = b''
            prev_time = time.time()
            QApplication.processEvents()
            while True:
                print("In the While")
                if ser.in_waiting > 0:
                    print("ser +")
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("datarx == b'r'")
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't079179\r':
                            print('if1')
                            main_window.text_label.setText("Check HSE frequency Response Done (ACK)")

                            check_check_hse_frequency = True
                            check_check_hse_frequency_opt = True

                            break
                        elif response == b't07911f\r':
                            print("elif 1")
                            main_window.text_label.setText("Check HSE frequency Response Failed (NACK)")

                            check_check_hse_frequency = True
                            check_check_hse_frequency_opt = False

                            break
                        else:
                            print("else")
                            main_window.text_label.setText("Check HSE frequency Response Failed (Missing data)")

                            check_check_hse_frequency = False
                            check_check_hse_frequency_opt = True

                            break
                if time.time() >= prev_time + 1.0:
                    print("time end")
                    # main_window.text_label.setText("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.text_label.setText("Check HSE frequency Response Failed (Timeout)")

                    check_check_hse_frequency = False
                    check_check_hse_frequency_opt = False

                    break

            time.sleep(1.0)
            QApplication.processEvents()
            while ser.in_waiting > 0:
                data_dummy = ser.read()
            print("out of while")
            if check_check_hse_frequency == True:
                if check_check_hse_frequency_opt == True:
                    print("a")
                    main_window.text_label.setText("Checked HSE frequency")
                else:
                    print("b")
                    main_window.text_label.setText("Already checked HSE frequency")
            else:
                print("c")
                main_window.text_label.setText("Can not check HSE frequency")

            print("thread 짧아서?")
            main_window.thread_stop()
        except:
            print("Exception")
            main_window.text_label.setText("Can not check HSE frequency")
            main_window.text_label.setText("Can not use %s" % ser.port)

            main_window.thread_stop()

            check_check_hse_frequency = False
            check_check_hse_frequency_opt = False
    else:
        print("else")
        main_window.text_label.setText("Can not check HSE frequency")
        main_window.text_label.setText("Can not find serial port")

        main_window.thread_stop()

        check_check_hse_frequency = False
        check_check_hse_frequency_opt = False

    print("before return")
    return check_check_hse_frequency, check_check_hse_frequency_opt


def get_ID(check_ser, ser):
    if check_ser == True:
        try:
            QApplication.processEvents()
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            request = b't002100\r'
            ser.write(request)
            # print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)

            response = b''
            prev_time = time.time()
            QApplication.processEvents()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't002179\r':
                            main_window.text_label.setText("Get ID Request Done (ACK)")

                            check_id = True

                            break
                        elif response == b't00211f\r':
                            main_window.text_label.setText("Get ID Request Failed (NACK)")

                            check_id = False

                            break
                        else:
                            main_window.text_label.setText("Get ID Request Failed (Unknown)")

                            check_id = False

                            break
                if time.time() >= prev_time + 1.0:
                    # print("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.text_label.setText("Get ID Request Failed (Timeout)")

                    check_id = False

                    break

            response = b''
            prev_time = time.time()
            QApplication.processEvents()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response[0:5] == b't0022':
                            if response[5:10] == b'0421\r':
                                main_window.text_label.setText(
                                    "Get ID Done (ID: 0x%03s (STM32F446xx))" % response[6:9].decode("utf-8"))

                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)

                                break
                            elif response[5:10] == b'0463\r':
                                main_window.text_label.setText(
                                    "Get ID Done (ID: 0x%03s (STM32F413xx))" % response[6:9].decode("utf-8"))

                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)

                                break
                            else:
                                main_window.text_label.setText(
                                    "Get ID Done (ID: 0x%03s)" % response[6:9].decode("utf-8"))

                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)

                                break
                        else:
                            main_window.text_label.setText("Get ID Failed (Unknown)")

                            chip_id = 0x000

                            break
                if time.time() >= prev_time + 1.0:
                    # print("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.text_label.setText("Get ID Failed (Timeout)")

                    chip_id = 0x000

                    break

            response = b''
            prev_time = time.time()
            QApplication.processEvents()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't002179\r':
                            main_window.text_label.setText("Get ID Response Done (ACK)")

                            check_id = True

                            break
                        elif response == b't00211f\r':
                            main_window.text_label.setText("Get ID Response Failed (NACK)")

                            check_id = False

                            break
                        else:
                            main_window.text_label.setText("Get ID Response Failed (Unknown)")

                            check_id = False

                            break
                if time.time() >= prev_time + 1.0:
                    # print("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.text_label.setText("Get ID Response Failed (Timeout)")

                    check_id = False

                    break

            if check_id == True:
                if chip_id == 0x421:
                    main_window.text_label.setText("Got ID: 0x%03x (STM32F446xx)" % chip_id)
                elif chip_id == 0x463:
                    main_window.text_label.setText("Got ID: 0x%03x (STM32F413xx)" % chip_id)
                else:
                    main_window.text_label.setText("Got ID: 0x%03x" % chip_id)
            else:
                main_window.text_label.setText("Can not get Chip ID")

            main_window.thread_stop()
        except:
            main_window.text_label.setText("Can not get Chip ID")
            main_window.text_label.setText("Can not use %s" % ser.port)

            main_window.thread_stop()

            check_id = False
            chip_id = 0x000
    else:
        main_window.text_label.setText("Can not get Chip ID")
        main_window.text_label.setText("Can not find serial port")

        main_window.thread_stop()

        check_id = False
        chip_id = 0x000

    return check_id, chip_id


def erase_memory(check_ser, ser):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            request = b't0431ff\r'
            ser.write(request)
            # print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)

            response = b''
            prev_time = time.time()
            QApplication.processEvents()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't043179\r':
                            main_window.text_label.setText("Erase Memory Request Done (ACK)")

                            check_erase = True

                            break
                        elif response == b't04311f\r':
                            main_window.text_label.setText("Erase Memory Request Failed (NACK)")

                            check_erase = False

                            break
                        else:
                            main_window.text_label.setText("Erase Memory Request Failed (Unknown)")

                            check_erase = False

                            break
                if time.time() >= prev_time + 1.0:
                    # main_window.text_label.setText("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.text_label.setText("Erase Memory Request Failed (Timeout)")

                    check_erase = False

                    break

            response = b''
            prev_time = time.time()
            QApplication.processEvents()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't043179\r':
                            main_window.text_label.setText("Erase Memory Response Done (ACK)")

                            check_erase = True

                            break
                        elif response == b't04311f\r':
                            main_window.text_label.setText("Erase Memory Response Failed (NACK)")

                            check_erase = False

                            break
                        else:
                            main_window.text_label.setText("Erase Memory Response Failed (Unknown)")

                            check_erase = False

                            break
                if time.time() >= prev_time + 30.0:
                    # print("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.text_label.setText("Erase Memory Response Failed (Timeout)")

                    check_erase = False

                    break

            if check_erase == True:
                main_window.text_label.setText("Erased memory")
            else:
                main_window.text_label.setText("Can not erase memory")

            main_window.thread_stop()
        except:
            main_window.text_label.setText("Can not erase memory")
            main_window.text_label.setText("Can not use %s" % ser.port)

            main_window.thread_stop()

            check_erase = False
    else:
        main_window.text_label.setText("Can not erase memory")
        main_window.text_label.setText("Can not find serial port")

        main_window.thread_stop()

        check_erase = False

    return check_erase


def upload_bin(check_ser, ser, check_bin, contents, num_128):
    if check_ser == True and check_bin == True:
        try:
            QApplication.processEvents()
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            for_break = False
            check_upload_bin = False
            QApplication.processEvents()
            for num in range(num_128):
                while ser.in_waiting > 0:
                    data_dummy = ser.read()

                addr = 0x08000000 + (128 * num)
                request = b't0315%08x7f\r' % addr
                ser.write(request)
                # print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                time.sleep(0.01)

                response = b''
                prev_time = time.time()
                QApplication.processEvents()
                while True:
                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # print(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't031179\r':
                                # main_window.text_label.setText("Write Memory 0x%08x - 0x%08x Request Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                check_upload_bin = True

                                break
                            elif response == b't03111f\r':
                                # main_window.text_label.setText("Write Memory 0x%08x - 0x%08x Request Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_upload_bin = False

                                break
                            else:
                                # main_window.text_label.setText("Write Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_upload_bin = False

                                break
                    if time.time() >= prev_time + 1.0:
                        # main_window.text_label.setText("Recv: %s" % response[0:].decode("utf-8"))
                        main_window.text_label.setText(
                            "Write Memory 0x%08x - 0x%08x Request Failed (Timeout), %04d / %04d" % (
                                addr, addr + 128 - 1, num + 1, num_128))

                        for_break = True
                        check_upload_bin = False

                        break

                if for_break == True:
                    break

                for i in range(16):
                    temp = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
                    for j in range(8):
                        if ((128 * num) + (8 * i) + j) < len(contents):
                            temp[j] = contents[(128 * num) + (8 * i) + j]

                    request = b't0048%02x%02x%02x%02x%02x%02x%02x%02x\r' % (
                        temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7])
                    ser.write(request)
                    # main_window.text_label.setText("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                    time.sleep(0.001)

                    response = b''
                    prev_time = time.time()
                    QApplication.processEvents()
                    while True:
                        if ser.in_waiting > 0:
                            data_rx = ser.read()
                            # print(data_rx)
                            response = response + data_rx
                            if data_rx == b'\r':
                                # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                                if response == b't031179\r':
                                    # main_window.text_label.setText("Write Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done (ACK), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, request[5:7].decode("utf-8"), request[7:9].decode("utf-8"), request[9:11].decode("utf-8"), request[11:13].decode("utf-8"), request[13:15].decode("utf-8"), request[15:17].decode("utf-8"), request[17:19].decode("utf-8"), request[19:21].decode("utf-8"), num + 1, num_128))

                                    check_upload_bin = True

                                    break
                                elif response == b't03111f\r':
                                    # main_window.text_label.setText("Write Memory 0x%08x - 0x%08x Failed (NACK), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))

                                    for_break = True
                                    check_upload_bin = False

                                    break
                                else:
                                    # main_window.text_label.setText("Write Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))

                                    for_break = True
                                    check_upload_bin = False

                                    break
                        if time.time() >= prev_time + 1.0:
                            # main_window.text_label.setText("Recv: %s" % response[0:].decode("utf-8"))

                            for_break = True
                            check_upload_bin = False

                            # main_window.text_label.setText("Write Memory 0x%08x - 0x%08x Failed (Timeout), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                            break

                    if for_break == True:
                        break

                if for_break == True:
                    break

                response = b''
                prev_time = time.time()
                QApplication.processEvents()
                while True:
                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # print(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't031179\r':
                                # print("Write Memory 0x%08x - 0x%08x Response Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                check_upload_bin = True

                                break
                            elif response == b't03111f\r':
                                # print("Write Memory 0x%08x - 0x%08x Response Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_upload_bin = False

                                break
                            else:
                                # print("Write Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_upload_bin = False

                                break
                    if time.time() >= prev_time + 1.0:
                        # print("Recv: %s" % response[0:].decode("utf-8"))
                        # print("Write Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                        for_break = True
                        check_upload_bin = False

                        break

                if for_break == True:
                    break

                time.sleep(0.01)

            if check_upload_bin == True:
                main_window.text_label.setText("Uploaded .bin file")
            else:
                main_window.text_label.setText("Can not upload .bin file")

            main_window.thread_stop()
        except:
            main_window.text_label.setText("Can not upload .bin file")
            main_window.text_label.setText("Can not use %s" % ser.port)

            main_window.thread_stop()

            check_upload_bin = False
    elif check_ser == True and check_bin == False:
        main_window.text_label.setText("Can not upload .bin file")
        main_window.text_label.setText("Can not find .bin file")

        main_window.thread_stop()

        check_upload_bin = False
    elif check_ser == False and check_bin == True:
        main_window.text_label.setText("Can not upload .bin file")
        main_window.text_label.setText("Can not find serial port")

        main_window.thread_stop()

        check_upload_bin = False
    else:
        main_window.text_label.setText("Can not upload .bin file")
        main_window.text_label.setText("Can not find both .bin file and serial port")

        main_window.thread_stop()

        check_upload_bin = False

    return check_upload_bin


def get_checksum(check_ser, ser, num_128):
    main_window.text_label.setText("Checking Checksum...")
    if check_ser == True:
        try:
            QApplication.processEvents()
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            for_break = False
            check_get_checksum = False
            crc_128_ack = np.uint32(0x00000000)
            QApplication.processEvents()
            for num in range(num_128):
                QApplication.processEvents()

                while ser.in_waiting > 0:
                    data_dummy = ser.read()

                addr = 0x08000000 + (128 * num)
                request = b't0115%08x7f\r' % addr
                ser.write(request)
                # print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                time.sleep(0.01)

                response = b''
                prev_time = time.time()
                QApplication.processEvents()
                while True:
                    QApplication.processEvents()

                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # main_window.text_label.setText(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # main_window.text_label.setText("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't011179\r':
                                # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Request Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                check_get_checksum = True

                                break
                            elif response == b't01111f\r':
                                # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Request Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_get_checksum = False

                                break
                            else:
                                # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_get_checksum = False

                                break
                    if time.time() >= prev_time + 1.0:
                        # main_window.text_label.setText("Recv: %s" % response[0:].decode("utf-8"))

                        for_break = True
                        check_get_checksum = False

                        # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Request Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        break

                if for_break == True:
                    break

                i = 0
                response = b''
                prev_time = time.time()
                QApplication.processEvents()
                while True:
                    QApplication.processEvents()

                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # main_window.text_label.setText(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # main_window.text_label.setText("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response[0:5] == b't0118':
                                if len(response) == 22:
                                    for j in range(8):
                                        crc_128_ack = crc_128_ack + np.uint32(
                                            int(("0x%02s" % response[5 + 2 * j:5 + 2 * j + 2].decode("utf-8")), 16))

                                    check_get_checksum = True

                                    # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done, %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, response[5:7].decode("utf-8"), response[7:9].decode("utf-8"), response[9:11].decode("utf-8"), response[11:13].decode("utf-8"), response[13:15].decode("utf-8"), response[15:17].decode("utf-8"), response[17:19].decode("utf-8"), response[19:21].decode("utf-8"), num + 1, num_128))
                                else:
                                    for_break = True
                                    check_get_checksum = False

                                    # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Failed (Missing data), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                            else:
                                for_break = True
                                check_get_checksum = False

                                # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))

                            response = b''
                            prev_time = time.time()

                            i = i + 1
                            if i == 16:
                                break
                    if time.time() >= prev_time + 1.0:
                        # main_window.text_label.setText("Recv: %s" % response[0:].decode("utf-8"))

                        for_break = True
                        check_get_checksum = False

                        # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        break

                if for_break == True:
                    break

                response = b''
                prev_time = time.time()
                QApplication.processEvents()
                while True:
                    QApplication.processEvents()

                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # main_window.text_label.setText(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # main_window.text_label.setText("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't011179\r':
                                # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Response Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                check_get_checksum = True

                                break
                            elif response == b't01111f\r':
                                # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Response Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_get_checksum = False

                                break
                            else:
                                # main_window.text_label.setText("Read Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_get_checksum = False

                                break
                    if time.time() >= prev_time + 1.0:
                        # main_window.text_label.setText("Recv: %s" % response[0:].decode("utf-8"))

                        for_break = True
                        check_get_checksum = False

                        main_window.text_label.setText(
                            "Read Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (
                                addr, addr + 128 - 1, num + 1, num_128))
                        break

                if for_break == True:
                    break

                time.sleep(0.01)

            if check_get_checksum == True:
                pass
                # main_window.text_label.setText("Got checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x08000000, 0x08000000 + (num_128 * 128) - 1, crc_128_ack, (num_128 * 128)))
            else:
                main_window.text_label.setText("Can not get checksum")

            main_window.thread_stop()
        except:
            main_window.text_label.setText("Can not get checksum")
            main_window.text_label.setText("Can not use %s" % ser.port)

            main_window.thread_stop()

            check_get_checksum = False
            crc_128_ack = np.uint32(0x00000000)
    else:
        main_window.text_label.setText("Can not get checksum")
        main_window.text_label.setText("Can not find serial port")

        main_window.thread_stop()

        check_get_checksum = False
        crc_128_ack = np.uint32(0x00000000)

    return check_get_checksum, crc_128_ack


def verify_checksum(crc_128, crc_128_ack):
    if crc_128 == crc_128_ack:
        main_window.text_label.setText(
            "Checksum matched (.bin file: 0x%08x, Memory: 0x%08x)" % (crc_128, crc_128_ack))

        main_window.thread_stop()

        check_verify_checksum = True
    else:
        main_window.text_label.setText(
            "Checksum not matched (.bin file: 0x%08x, Memory: 0x%08x)" % (crc_128, crc_128_ack))

        main_window.thread_stop()

        check_verify_checksum = False

    return check_verify_checksum


def main_func(bin_file, port, skip_checksum):
    count = 0
    progressbar_update(count)

    check_bin, contents, crc, num_128, crc_128, a = read_bin(bin_file)
    print("Why?")
    if check_bin == False:
        print('hihi')
        main_window.text_label.setText("Failed to upload .bin file (read_bin)")

        main_window.thread_stop()

        return False

    print("HiHiHi")

    check_ser, ser = open_serial(port)
    print("open_serial port 문제인가?")

    progressbar_update(10)

    print("open serial port 문제 아니네")

    if check_ser == False:
        main_window.text_label.setText("Failed to upload .bin file (open_serial)")
        print("main_window.thread_stop()이 문제인가?")
        main_window.thread_stop()
        print("main pass")
        return False

    print("여기 지나가면 안됨")
    check_ser = check_serial(check_ser, ser)
    count = 15
    progressbar_update(count)

    print("progressBar 뒤에 processEvent")
    if check_ser == False:
        check_ser = close_serial(check_ser, ser)

        main_window.text_label.setText("Failed to upload .bin file (check_serial)")

        main_window.thread_stop()

        return False

    print("Noppppp")
    check_check_hse_frequency, check_check_hse_frequency_opt = check_hse_frequency(check_ser, ser)
    print("progress 더 해줘야되나?")
    count = 20
    progressbar_update(count)

    print("whywhy")
    if check_check_hse_frequency == False:
        check_ser = close_serial(check_ser, ser)

        main_window.text_label.setText("Failed to upload .bin file (check_hse_frequency)")

        main_window.thread_stop()

        return False

    check_get_id, chip_id = get_ID(check_ser, ser)

    print("또 여기?")
    count = 25
    progressbar_update(count)
    print("hse progressbar passed")
    if check_get_id == False:
        check_ser = close_serial(check_ser, ser)

        main_window.text_label.setText("Failed to upload .bin file (check_get_id)")

        main_window.thread_stop()

        return False

    check_erase_memory = erase_memory(check_ser, ser)

    count = 30
    progressbar_update(count)

    if check_erase_memory == False:
        check_ser = close_serial(check_ser, ser)

        main_window.text_label.setText("Failed to upload .bin file (erase_memory)")

        main_window.thread_stop()

        return False

    check_upload_bin = upload_bin(check_ser, ser, check_bin, contents, num_128)

    count = 35
    progressbar_update(count)

    if check_upload_bin == False:
        check_ser = close_serial(check_ser, ser)

        main_window.text_label.setText("Failed to upload .bin file (upload_bin)")

        main_window.thread_stop()

        return False

    if skip_checksum == False:
        check_get_checksum, crc_128_ack = get_checksum(check_ser, ser, num_128)
        if check_get_checksum == False:
            check_ser = close_serial(check_ser, ser)

            main_window.text_label.setText("Failed to verify checksum (get_checksum)")

            main_window.thread_stop()

            return False

        check_verify_checksum = verify_checksum(crc_128, crc_128_ack)
    else:
        main_window.text_label.setText("Skipped checksum verification")

        main_window.thread_stop()

    check_ser = close_serial(check_ser, ser)

    count = 40
    progressbar_update(count)

    if skip_checksum == False:
        if check_verify_checksum == True:
            main_window.text_label.setText("Successfully uploaded .bin file (Checksum matched)")

            main_window.thread_stop()

            return True
        else:
            main_window.text_label.setText("Failed to upload .bin file (Checksum unmatched)")

            main_window.thread_stop()

            return False
    else:
        main_window.text_label.setText("Successfully uploaded .bin file (Checksum verification skipped)")

        main_window.thread_stop()

        return True


sys.exit(app.exec_())