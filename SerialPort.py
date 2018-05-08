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
import threading
import queue
import time
import os


########################### serial port operation ################################# 
class SerialPortProc(threading.Thread):
	def __init__(self, data_queue):
		threading.Thread.__init__(self, daemon = True)
		self.dat_queue = data_queue
		#open serial port
		self.hcom = serial.Serial('COM2', 9600, timeout = 0.5, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE) 

	def run(self):
		while 1:
			com_read = self.hcom.readall()
			if len(com_read):
				res = self.serial_data_extract(com_read)
				
				if res != None:
					self.dat_queue.put(res)
			
	def serial_data_extract(self, serial_data):
		#pack_head = serial_data[0:6].decode()
		
		cbop_data = {}
		
		dat_index = 6;
		if serial_data[0:6] == b'sensor':
			cbop_data['left_n_730'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]
			dat_index += 2;
			cbop_data['left_f_730'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]
			dat_index += 2;
			cbop_data['left_n_850'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]
			dat_index += 2;
			cbop_data['left_f_850'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]
			dat_index += 2;
			cbop_data['right_n_730'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]
			dat_index += 2;
			cbop_data['right_f_730'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]
			dat_index += 2;
			cbop_data['right_n_850'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]
			dat_index += 2;
			cbop_data['right_f_850'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]
			dat_index += 2;
			cbop_data['left_cbop'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]
			dat_index += 2;
			cbop_data['right_cbop'] = struct.unpack('<H', bytes(serial_data[dat_index:dat_index + 2]))[0]

			return cbop_data
		else:
			return None
############################# serial port gui ################################################
class SerialPortGUI(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title('CBOP Dispaly')
		win_width = 1000
		win_height = 610
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		
		self.canvas_height = 250
		self.canvas_width = 800
		self.dot_len = 4
		self.dot_height = 4
		self.max_data_len = self.canvas_width // self.dot_len
		
		#file for storing cbop data
		current_dir = os.getcwd()
		current_dir += '\\data\\'
		file_name = time.strftime('%Y%m%d %H%M%S', time.localtime())
		file_name += '.txt'
		self.f_data = open(current_dir + file_name, 'w')
		
		#data buffer for canvas
		self.left_data_buf = []
		self.right_data_buf = []
		
		#queue for serial data from serial port threading
		self.data_queue = queue.Queue()
		
		gui_frame = ttk.Frame(self)
		
		#left 730nm
		self.left_near_730_var = StringVar()
		left_near_730_lb = ttk.Label(gui_frame, text = '左-近-730nm: ')
		left_near_730 = ttk.Entry(gui_frame, textvariable = self.left_near_730_var)
		self.left_far_730_var = StringVar()
		left_far_730_lb = ttk.Label(gui_frame, text = '左-远-730nm: ')
		left_far_730 = ttk.Entry(gui_frame, textvariable = self.left_far_730_var)
		#left 850nm
		self.left_near_850_var = StringVar()
		left_near_850_lb = ttk.Label(gui_frame, text = '左-近-850nm: ')
		left_near_850 = ttk.Entry(gui_frame, textvariable = self.left_near_850_var)
		self.left_far_850_var = StringVar()
		left_far_850_lb = ttk.Label(gui_frame, text = '左-远-850nm: ')
		left_far_850 = ttk.Entry(gui_frame, textvariable = self.left_far_850_var)
		#right 730nm
		self.right_near_730_var = StringVar()
		right_near_730_lb = ttk.Label(gui_frame, text = '右-近-730nm: ')
		right_near_730 = ttk.Entry(gui_frame, textvariable = self.right_near_730_var)
		self.right_far_730_var = StringVar()
		right_far_730_lb = ttk.Label(gui_frame, text = '右-远-730nm: ')
		right_far_730 = ttk.Entry(gui_frame, textvariable = self.right_far_730_var)
		#right 850nm
		self.right_near_850_var = StringVar()
		right_near_850_lb = ttk.Label(gui_frame, text = '右-近-850nm: ')
		right_near_850 = ttk.Entry(gui_frame, textvariable = self.right_near_850_var)
		self.right_far_850_var = StringVar()
		right_far_850_lb = ttk.Label(gui_frame, text = '右-远-850nm: ')
		right_far_850 = ttk.Entry(gui_frame, textvariable = self.right_far_850_var)
		
		#left
		self.left_cbop_var = StringVar()
		left_cbop_lb = ttk.Label(gui_frame, font = (None, 40), textvariable = self.left_cbop_var)
		self.data_canvas_left = Canvas(gui_frame, height = self.canvas_height)
		#right
		self.right_cbop_var = StringVar()
		right_cbop_lb = ttk.Label(gui_frame, font = (None, 40), textvariable = self.right_cbop_var)	
		self.data_canvas_right = Canvas(gui_frame, height = self.canvas_height)
	
	
		gui_frame.grid(column = 0, row = 0, padx = 10)
		#left 730
		left_near_730_lb.grid(column = 0, row = 0, padx = 5, pady = 10)
		left_near_730.grid(column = 1, row = 0)
		left_far_730_lb.grid(column = 2, row = 0, padx = 5)
		left_far_730.grid(column = 3, row = 0, padx = 5)
		#left 850
		left_near_850_lb.grid(column = 4, row = 0, padx = 5, pady = 10)
		left_near_850.grid(column = 5, row = 0)
		left_far_850_lb.grid(column = 6, row = 0, padx = 5)
		left_far_850.grid(column = 7, row = 0, padx = 5)
		#right 730
		right_near_730_lb.grid(column = 0, row = 1, padx = 5, pady = 10)
		right_near_730.grid(column = 1, row = 1)
		right_far_730_lb.grid(column = 2, row = 1, padx = 5)
		right_far_730.grid(column = 3, row = 1, padx = 5)
		#right 850
		right_near_850_lb.grid(column = 4, row = 1, padx = 5, pady = 10)
		right_near_850.grid(column = 5, row = 1)
		right_far_850_lb.grid(column = 6, row = 1, padx = 5)
		right_far_850.grid(column = 7, row = 1, padx = 5)
		#plot left
		self.left_cbop_var.set('%s' % (0.0))
		left_cbop_lb.grid(column = 7, row = 2, sticky = E)
		self.data_canvas_left.grid(column = 0, row = 2, columnspan = 7, sticky = (E, W), pady = 5)
		#plot right
		self.right_cbop_var.set('%s' % (0.0))
		right_cbop_lb.grid(column = 7, row = 3, sticky = E)
		self.data_canvas_right.grid(column = 0, row = 3, columnspan = 7, sticky = (E, W), pady = 5)

		#serial threading
		self.serial_thread = SerialPortProc(self.data_queue)
		self.serial_thread.start()
		
		self.draw_canvas()
		#message process loop
		self.loop_plot()
		
	def destroy(self):
		self.f_data.close()
		self.quit()
		
	#init canvas
	def draw_canvas(self):
		#at first delete all in canvas
		self.data_canvas_left.delete('all')
		self.data_canvas_right.delete('all')
		
		index_x = 0;
		dot_position = {'x_1':0, 'y_1':0, 'x_2':0, 'y_2':0}
		for dat in self.left_data_buf:
			if index_x == 0:
				dot_position['x_2'] = self.canvas_width - index_x 			
				dot_position['y_2'] = self.canvas_height - dat * self.canvas_height // 1000
				if dot_position['y_2'] == 0:
					dot_position['y_2'] = 1
					
				index_x += self.dot_len	
				dot_position['x_1'] = self.canvas_width - index_x			
				dot_position['y_1'] = dot_position['y_2']
							
			else:
				index_x += self.dot_len
				dot_position['x_1'] = self.canvas_width - index_x
				dot_position['y_1'] = self.canvas_height - dat * self.canvas_height // 1000
				if dot_position['y_1'] == 0:
					dot_position['y_1'] = 1
				
			self.data_canvas_left.create_line(dot_position['x_1'], dot_position['y_1'], dot_position['x_2'], dot_position['y_2'], width = self.dot_height, fill = 'red')
			dot_position['x_2'] = dot_position['x_1']
			dot_position['y_2'] = dot_position['y_1']
			
		index_x = 0;
		for dat in self.right_data_buf:
			if index_x == 0:
				dot_position['x_2'] = self.canvas_width - index_x 
				dot_position['y_2'] = self.canvas_height - dat * self.canvas_height // 1000
				if dot_position['y_2'] == 0:
					dot_position['y_2'] = 1
					
				index_x += self.dot_len
				dot_position['x_1'] = self.canvas_width - index_x			
				dot_position['y_1'] = dot_position['y_2']
			else:
				index_x += self.dot_len
				dot_position['x_1'] = self.canvas_width - index_x
				dot_position['y_1'] = self.canvas_height - dat * self.canvas_height // 1000
				if dot_position['y_1'] == 0:
					dot_position['y_1'] = 1
				
			self.data_canvas_right.create_line(dot_position['x_1'], dot_position['y_1'], dot_position['x_2'], dot_position['y_2'], width = self.dot_height, fill = 'red')
			dot_position['x_2'] = dot_position['x_1']
			dot_position['y_2'] = dot_position['y_1']
			
		#y axis
		self.data_canvas_left.create_line(0, 0, 0, self.canvas_height, width = 8, fill = 'blue')
		self.data_canvas_right.create_line(0, 0, 0, self.canvas_height, width = 8, fill = 'blue')
		#y axis
		self.data_canvas_left.create_line(0, self.canvas_height, self.canvas_width, self.canvas_height, width = 2, fill = 'blue')
		self.data_canvas_right.create_line(0, self.canvas_height, self.canvas_width, self.canvas_height, width = 2, fill = 'blue')

				
	#message loop for plotting serial data_canvas_left
	def loop_plot(self):
				
		while not self.data_queue.empty():
			value = self.data_queue.get()
			
			if len(self.left_data_buf) == self.max_data_len:
				self.left_data_buf.pop(-1)
				self.right_data_buf.pop(-1)
							
			self.left_data_buf.insert(0, value['left_cbop'])
			self.right_data_buf.insert(0, value['right_cbop'])
			
			#update the cbop data
			self.left_cbop_var.set('%s' % (value['left_cbop'] / 10))
			self.right_cbop_var.set('%s' % (value['right_cbop'] / 10))
			
			#left
			self.left_near_730_var.set('%s' % (value['left_n_730']))
			self.left_far_730_var.set('%s' % (value['left_f_730']))
			self.left_near_850_var.set('%s' % (value['left_n_850']))
			self.left_far_850_var.set('%s' % (value['left_f_850']))
			
			#right
			self.right_near_730_var.set('%s' % (value['right_n_730']))
			self.right_far_730_var.set('%s' % (value['right_f_730']))
			self.right_near_850_var.set('%s' % (value['right_n_850']))
			self.right_far_850_var.set('%s' % (value['right_f_850']))
			
			#store data into file
			self.f_data.write(str(value))
			self.f_data.write('\n')
			
			#update drawing the canvas
			self.draw_canvas()
			
		self.after(100, self.loop_plot)
# main		
if __name__ == '__main__':
	serial_gui = SerialPortGUI()		
	serial_gui.mainloop()