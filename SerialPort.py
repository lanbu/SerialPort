#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' serial port using example'''

__author__ = 'Lanbu'

import serial
from serial import *
import datetime
import struct
from tkinter import *
from tkinter import ttk


########################### serial port operation ################################# 
hcom = serial.Serial('COM22', 9600, timeout = 0.5, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE) 

def serial_data_extract(serial_data):
	pack_head = serial_data[0:6].decode()
	
	cbop_data = {}
	
	dat_index = 6;
	if pack_head == 'sensor':
		cbop_data['left_n_led1'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		dat_index += 2;
		cbop_data['left_f_led1'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		dat_index += 2;
		cbop_data['left_n_led2'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		dat_index += 2;
		cbop_data['left_f_led2'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		dat_index += 2;
		cbop_data['right_n_led1'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		dat_index += 2;
		cbop_data['right_f_led1'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		dat_index += 2;
		cbop_data['right_n_led2'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		dat_index += 2;
		cbop_data['right_f_led2'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		dat_index += 2;
		cbop_data['left_cbop'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		dat_index += 2;
		cbop_data['right_cbop'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))
		
		print(cbop_data)

while 1:
	com_read = hcom.readall()
	if len(com_read):
		serial_data_extract(com_read)
		


