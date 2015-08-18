import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tk_mb

default_width, default_height = 800, 400

class Main_window(tk.Tk):
	def __init__(self, plugin_base):
		tk.Tk.__init__(self)
		self.title('DaVis')
		self.minsize(400, 200)
		self.geometry('{0}x{1}+30+30'.format(default_width, default_height))
		self.columnconfigure(0, weight=0)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)
		
		self.data = {}
		
		self.data_frame = Data_frame(self, plugin_base)
		self.visualization_frame = Visualization_frame(self, plugin_base)
		self.operations_frame = Operations_frame(self, plugin_base)
		ttk.Sizegrip(self).grid(column=3, row=0, sticky='E S')
		
	# Convenience methods
	def get_data(self):
		return self.data
	def get_canvas(self):
		return self.visualization_frame.canvas
	def redraw(self):
		self.visualization_frame.redraw()
	def show_warning(self, message, title=None):
		tk_mb.showwarning(title=title, message=message)

class Data_frame(ttk.Frame):
	def __init__(self, parent, plugin_base):
		ttk.Frame.__init__(self, parent, padding=10)
		self.grid(column=0, row=0, sticky='W N E S')
		self.columnconfigure(0, weight=1)
		
		self.plugin_base = plugin_base
		self.action_count = 0
	
	def add_action(self, name, event_id, event_appendix):
		callback = lambda: self.plugin_base._notify_all( (event_id, event_appendix) )
		action = ttk.Button(self, text=name, command=callback)
		action.grid(column=0, row=self.action_count, sticky='W N E S')
		self.action_count += 1

class Visualization_frame(ttk.Frame):
	def __init__(self, parent, plugin_base):
		ttk.Frame.__init__(self, parent)
		self.grid(column=1, row=0, sticky='W N E S')
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		
		self.plugin_base = plugin_base
		
		h_scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
		v_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
		self.canvas = tk.Canvas(self, scrollregion=(-1000, -1000, 1000, 1000), xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set, background='white')
		self.canvas.grid(column=0, row=0, sticky='W N E S')
		h_scrollbar['command'] = self.canvas.xview
		v_scrollbar['command'] = self.canvas.yview
		h_scrollbar.grid(column=0, row=1, sticky='E W')
		v_scrollbar.grid(column=1, row=0, sticky='N S')
		
		scale_frame = ttk.Frame(self, borderwidth=5)
		scale_frame.grid(column=0, row=2, sticky='N E W S')
		scale_frame.columnconfigure(2, weight=1)
		self.scale_variable = tk.DoubleVar()
		scale_literal = ttk.Label(scale_frame, text='Scale:')
		scale_literal.grid(column=0, row=0)
		scale_label = ttk.Label(scale_frame, textvariable=self.scale_variable, width=4)
		scale_label.grid(column=1, row=0, padx=5, pady=5, sticky='W')
		callback = lambda new_scale: self.redraw()
		scale_bar = ttk.Scale(scale_frame, orient=tk.HORIZONTAL, from_=0.01, to=10.0, variable=self.scale_variable, command=callback)
		scale_bar.grid(column=2, row=0, padx=5, pady=5, stick='E W')
		self.scale_variable.set(1.0)
	
	def rescale(self):
		self.plugin_base._notify_all( ('rescale_pre', None) )
		scale = self.scale_variable.get()
		for identifier in self.canvas.find_all():
			self.canvas.scale(identifier, 0, 0, scale, scale)
		self.plugin_base._notify_all( ('rescale_post', None) )
	
	def redraw(self):
		self.canvas.delete(tk.ALL)
		self.plugin_base._notify_all( ('redraw', None) )
		
		#~ Rescale
		self.rescale()
		
		#~ Center everything in visible area
		try:
			canvas_dims = (self.canvas.winfo_width(), self.canvas.winfo_height())
			new_scrollregion = list(self.canvas.bbox('all')) # bbox can be None, causing a TypeError from list()
			if new_scrollregion[2] - new_scrollregion[0] < canvas_dims[0]:
				diff = canvas_dims[0] - (new_scrollregion[2] - new_scrollregion[0])
				new_scrollregion[2] += diff // 2
				new_scrollregion[0] -= diff // 2
			if new_scrollregion[3] - new_scrollregion[1] < canvas_dims[1]:
				diff = canvas_dims[1] - (new_scrollregion[3] - new_scrollregion[1])
				new_scrollregion[3] += diff // 2
				new_scrollregion[1] -= diff // 2
			self.canvas.configure(scrollregion = new_scrollregion)
		except TypeError:
			pass

class Operations_frame(ttk.Frame):
	def __init__(self, parent, plugin_base):
		ttk.Frame.__init__(self, parent, padding=10)
		self.grid(column=2, row=0, sticky='W N E S')
		self.columnconfigure(0, weight=1)
		
		self.plugin_base = plugin_base
		self.action_count = 0
	
	def add_action(self, name, event_id, event_appendix):
		callback = lambda: self.plugin_base._notify_all( (event_id, event_appendix) )
		action = ttk.Button(self, text=name, command=callback)
		action.grid(column=0, row=self.action_count, sticky='W N E S')
		self.action_count += 1









