import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import plugin_base

#~ TODO padding
class Uniform_Window(tk.Toplevel):
	def __init__(self, parent):
		super().__init__(parent)
		
		self.title('Data from uniform distribution')
		self.resizable(tk.FALSE, tk.FALSE)
		self.protocol('WM_DELETE_WINDOW', self.cancel_action)
		
		config_frame = ttk.Frame(self, borderwidth=10)
		config_frame.grid(column=0, row=0, sticky='N E W S')
		
		ttk.Label(config_frame, text='Min. x1 value').grid(column=0, row=0, sticky='W', padx=5, pady=5)
		self.minX1var = tk.IntVar()
		self.minX1var.set(-100)
		ttk.Entry(config_frame, textvariable=self.minX1var, width=5).grid(column=1, row=0, sticky='E')
		
		ttk.Label(config_frame, text='Max. x1 value').grid(column=0, row=1, sticky='W', padx=5, pady=5)
		self.maxX1var = tk.IntVar()
		self.maxX1var.set(100)
		ttk.Entry(config_frame, textvariable=self.maxX1var, width=5).grid(column=1, row=1, sticky='E')
		
		ttk.Label(config_frame, text='Min. x2 value').grid(column=0, row=2, sticky='W', padx=5, pady=5)
		self.minX2var = tk.IntVar()
		self.minX2var.set(-30)
		ttk.Entry(config_frame, textvariable=self.minX2var, width=5).grid(column=1, row=2, sticky='E')
		
		ttk.Label(config_frame, text='Max. x2 value').grid(column=0, row=3, sticky='W', padx=5, pady=5)
		self.maxX2var = tk.IntVar()
		self.maxX2var.set(30)
		ttk.Entry(config_frame, textvariable=self.maxX2var, width=5).grid(column=1, row=3, sticky='E')
		
		ttk.Label(config_frame, text='Number of points').grid(column=0, row=4, sticky='W', padx=5, pady=5)
		self.point_countvar = tk.IntVar()
		self.point_countvar.set(100)
		self.a = ttk.Entry(config_frame, textvariable=self.point_countvar, width=5)
		self.a.grid(column=1, row=4, sticky='W')
		
		confirmation_frame = ttk.Frame(self)
		confirmation_frame.grid(column=0, row=1, sticky='N E W S')
		ttk.Button(confirmation_frame, text='Cancel', command=self.cancel_action).grid(column=0, row=0, sticky='W', padx=5, pady=5)
		ttk.Button(confirmation_frame, text='Ok', command=self.ok_action).grid(column=1, row=0, sticky='E', padx=5, pady=5)
		
	def ok_action(self):
		self.accept = True
		self.destroy()
	
	def cancel_action(self):
		self.accept = False
		self.destroy()
	
	def get_values(self):
		self.wait_window()
		if self.accept:
			return self.minX1var.get(), self.maxX1var.get(), self.minX2var.get(), self.maxX2var.get(), self.point_countvar.get()
		else:
			raise Exception('cancel')

class Point_Cloud(plugin_base.Plugin_Base):
	def __init__(self):
		super().__init__()
		
		self.program.data_frame.add_action('New uniform', 'pq_new_uniform', None)
		self.program.data_frame.add_action('Clear', 'pq_clear', None)
		self.register_event_handler('pq_new_uniform', self.new_uniform)
		self.register_event_handler('pq_clear', self.clear)
		self.register_event_handler('redraw', self.draw)
	
	def new_uniform(self, event):
		query_window = Uniform_Window(self.program)
		
		try:
			minX1, maxX1, minX2, maxX2, point_count = query_window.get_values()
		except:
			return
		
		pointsX1 = np.random.uniform(minX1, maxX1, (point_count, 1))
		pointsX2 = np.random.uniform(minX2, maxX2, (point_count, 1))
		points = np.column_stack([pointsX1, pointsX2])
		try:
			self.program.get_data()['points'].append( (points, 'black') )
		except KeyError:
			self.program.get_data()['points'] = [ (points, 'black') ]
		
		self.program.redraw()
	
	def clear(self, event):
		self.program.get_data()['points'] = []
		self.program.redraw()
	
	def draw(self, event):
		canvas = self.program.get_canvas()
		for point_set, color in self.program.get_data()['points']:
			for point in point_set:
				canvas.create_oval(point[0], point[1], point[0], point[1], fill=color, outline=color)






