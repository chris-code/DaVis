try:
	import numpy as np
except ImportError:
	raise Exception('This plugin requires the numpy library, which failed to import. \
	Install the python3 version of numpy.')
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.colorchooser as tkcc
import plugin

class Distribution_Query_Window(tk.Toplevel):
	def __init__(self, parent):
		super().__init__(parent)
			
		self.title('Data from distribution')
		self.resizable(tk.FALSE, tk.FALSE)
		self.protocol('WM_DELETE_WINDOW', self.cancel_action)
		self.grab_set() # Make window modal
		
		self.nb = ttk.Notebook(self)
		self.nb.grid(column=0, row=0, sticky='N E W S', padx=10, pady=10)
		self.nb.add(self.make_uniform_frame(self.nb), text='Uniform', sticky='EW')
		self.nb.add(self.make_normal_frame(self.nb), text='Normal', sticky='EW')
		
		general_options_frame = ttk.LabelFrame(self, padding=5, text='General options')
		general_options_frame.grid(column=0, row=1, sticky='N E W S', padx=5, pady=5)
		general_options_frame.columnconfigure(1, weight=1)
		ttk.Label(general_options_frame, text='Number of points').grid(column=0, row=0, sticky='N W S', padx=5, pady=5)
		self.number_of_points = tk.IntVar()
		self.number_of_points.set(100)
		point_count_spinbox = tk.Spinbox(general_options_frame, from_=1, to=1000000, increment=100, textvariable=self.number_of_points, width=7)
		point_count_spinbox.grid(column=1, row=0, sticky='N E S', padx=5, pady=5)
		ttk.Label(general_options_frame, text='Color').grid(column=0, row=1, sticky='N W S', padx=5, pady=5)
		ttk.Button(general_options_frame, text='choose', command=self.color_choose_action).grid(column=1, row=1, sticky='N E S', padx=5, pady=5)
		self.color = '#000000'
		
		confirmation_frame = ttk.Frame(self)
		confirmation_frame.grid(column=0, row=2, sticky='N E W S', padx=10, pady=10)
		confirmation_frame.columnconfigure(1, weight=1)
		ttk.Button(confirmation_frame, text='Cancel', command=self.cancel_action).grid(column=0, row=0, sticky='N W S')
		ttk.Button(confirmation_frame, text='Ok', command=self.ok_action).grid(column=1, row=0, sticky='N E S')
		
	def make_uniform_frame(self, notebook):
		frame = ttk.Frame(notebook, padding=10)
		self.uniform_parameters = {}
		frame.columnconfigure(0, weight=1)
		
		#~ x_1 dimension
		x1_frame = ttk.LabelFrame(frame, padding=5, text='X1 dimension')
		x1_frame.grid(column=0, row=0, sticky='N E W S', padx=5, pady=5)
		x1_frame.columnconfigure(1, weight=1)
		
		ttk.Label(x1_frame, text='Min').grid(column=0, row=0, padx=5, pady=5, sticky='W')
		self.uniform_parameters['x1_min'] = tk.DoubleVar()
		self.uniform_parameters['x1_min'].set(-100)
		x1_min_spinbox = tk.Spinbox(x1_frame, from_=-1000.0, to=1000.0, increment=10, textvariable=self.uniform_parameters['x1_min'], width=5)
		x1_min_spinbox.grid(column=1, row=0, sticky='E', padx=5, pady=5)
		
		ttk.Label(x1_frame, text='Max').grid(column=0, row=1, padx=5, pady=5, sticky='W')
		self.uniform_parameters['x1_max'] = tk.DoubleVar()
		self.uniform_parameters['x1_max'].set(100)
		x1_min_spinbox = tk.Spinbox(x1_frame, from_=-1000.0, to=1000.0, increment=10, textvariable=self.uniform_parameters['x1_max'], width=5)
		x1_min_spinbox.grid(column=1, row=1, sticky='E', padx=5, pady=5)
		
		#~ x_2 dimension
		x2_frame = ttk.LabelFrame(frame, padding=5, text='X2 dimension')
		x2_frame.grid(column=0, row=1, sticky='N E W S', padx=5, pady=5)
		x2_frame.columnconfigure(1, weight=1)
		
		ttk.Label(x2_frame, text='Min').grid(column=0, row=0, padx=5, pady=5, sticky='W')
		self.uniform_parameters['x2_min'] = tk.DoubleVar()
		self.uniform_parameters['x2_min'].set(-30)
		x2_min_spinbox = tk.Spinbox(x2_frame, from_=-1000.0, to=1000.0, increment=10, textvariable=self.uniform_parameters['x2_min'], width=5)
		x2_min_spinbox.grid(column=1, row=0, sticky='E', padx=5, pady=5)
		
		ttk.Label(x2_frame, text='Max').grid(column=0, row=1, padx=5, pady=5, sticky='W')
		self.uniform_parameters['x2_max'] = tk.DoubleVar()
		self.uniform_parameters['x2_max'].set(30)
		x2_min_spinbox = tk.Spinbox(x2_frame, from_=-1000.0, to=1000.0, increment=10, textvariable=self.uniform_parameters['x2_max'], width=5)
		x2_min_spinbox.grid(column=1, row=1, sticky='E', padx=5, pady=5)
		
		return frame
		
	def make_normal_frame(self, notebook):
		frame = ttk.Frame(notebook, padding=10)
		self.normal_parameters = {}
		
		#~ x_1 dimension
		x1_frame = ttk.LabelFrame(frame, padding=5, text='X1 dimension')
		x1_frame.grid(column=0, row=0, sticky='N E W S', padx=5, pady=5)
		
		ttk.Label(x1_frame, text='Mean').grid(column=0, row=0, padx=5, pady=5, sticky='W')
		self.normal_parameters['x1_mean'] = tk.DoubleVar()
		self.normal_parameters['x1_mean'].set(0)
		x1_mean_spinbox = tk.Spinbox(x1_frame, from_=-1000.0, to=1000.0, increment=10, textvariable=self.normal_parameters['x1_mean'], width=5)
		x1_mean_spinbox.grid(column=1, row=0, padx=5, pady=5)
		
		ttk.Label(x1_frame, text='Standard deviation').grid(column=0, row=1, padx=5, pady=5, sticky='W')
		self.normal_parameters['x1_std_dev'] = tk.DoubleVar()
		self.normal_parameters['x1_std_dev'].set(30)
		x1_std_dev_spinbox = tk.Spinbox(x1_frame, from_=0.001, to=1000.0, increment=10, textvariable=self.normal_parameters['x1_std_dev'], width=5)
		x1_std_dev_spinbox.grid(column=1, row=1, padx=5, pady=5)
		
		#~ x_2 dimension
		x2_frame = ttk.LabelFrame(frame, padding=5, text='X2 dimension')
		x2_frame.grid(column=0, row=1, sticky='N E W S', padx=5, pady=5)
		
		ttk.Label(x2_frame, text='Mean').grid(column=0, row=0, padx=5, pady=5, sticky='W')
		self.normal_parameters['x2_mean'] = tk.DoubleVar()
		self.normal_parameters['x2_mean'].set(0)
		x2_mean_spinbox = tk.Spinbox(x2_frame, from_=-1000.0, to=1000.0, increment=10, textvariable=self.normal_parameters['x2_mean'], width=5)
		x2_mean_spinbox.grid(column=1, row=0, padx=5, pady=5)
		
		ttk.Label(x2_frame, text='Standard Deviation').grid(column=0, row=1, padx=5, pady=5, sticky='W')
		self.normal_parameters['x2_std_dev'] = tk.DoubleVar()
		self.normal_parameters['x2_std_dev'].set(30)
		x2_std_dev_spinbox = tk.Spinbox(x2_frame, from_=0.001, to=1000.0, increment=10, textvariable=self.normal_parameters['x2_std_dev'], width=5)
		x2_std_dev_spinbox.grid(column=1, row=1, padx=5, pady=5)
		
		return frame
	
	def color_choose_action(self):
		_, self.color = tkcc.askcolor()
	
	def ok_action(self):
		self.distribution = self.nb.tab(self.nb.select(), 'text')
		self.destroy()
	
	def cancel_action(self):
		self.distribution = None
		self.destroy()
	
	@classmethod
	def get_values(cls, program):
		window = cls(program)
		window.wait_window()
		
		if window.distribution is not None:
			parameters = {}
			count = window.number_of_points.get()
			color = window.color
			
			if window.distribution == 'Uniform':
				for param_name in window.uniform_parameters.keys():
					parameters[param_name] = window.uniform_parameters[param_name].get()
			elif window.distribution == 'Normal':
				for param_name in window.normal_parameters.keys():
					parameters[param_name] = window.normal_parameters[param_name].get()
			
			return window.distribution, parameters, count, color
		else:
			return None

class Transformation_Query_Window(tk.Toplevel):
	def __init__(self, parent, data):
		super().__init__(parent)
			
		self.title('Data from distribution')
		self.resizable(tk.FALSE, tk.FALSE)
		self.protocol('WM_DELETE_WINDOW', self.cancel_action)
		self.grab_set() # Make window modal
		
		self.nb = ttk.Notebook(self)
		self.nb.grid(column=0, row=0, sticky='N E W S', padx=10, pady=10)
		self.nb.add(self.make_arbitrary_frame(self.nb), text='Arbitrary', sticky='EW')
		
		data_select_frame = ttk.LabelFrame(self, padding=5, text='Data sets to transform')
		data_select_frame.grid(column=0, row=1, sticky='N E W S', padx=5, pady=5)
		data_select_frame.columnconfigure(1, weight=1)
		row = 0
		self.selected_datasets = []
		for index, dataset in enumerate(data):
			points, color = dataset
			tk.Canvas(data_select_frame, background=color, width=15, height=15).grid(column=0, row=index)
			selection_variable = tk.BooleanVar()
			selection_variable.set(True)
			ttk.Checkbutton(data_select_frame, variable=selection_variable, onvalue=True, offvalue=False).grid(column=1, row=index)
			self.selected_datasets.append(selection_variable)
		
		confirmation_frame = ttk.Frame(self)
		confirmation_frame.grid(column=0, row=2, sticky='N E W S', padx=10, pady=10)
		confirmation_frame.columnconfigure(1, weight=1)
		ttk.Button(confirmation_frame, text='Cancel', command=self.cancel_action).grid(column=0, row=0, sticky='N W S')
		ttk.Button(confirmation_frame, text='Ok', command=self.ok_action).grid(column=1, row=0, sticky='N E S')
	
	def make_arbitrary_frame(self, notebook):
		frame = ttk.Frame(notebook, padding=10)
		ttk.Label(frame, text='Matrix').grid(column=0, row=0, padx=5, pady=5, sticky='W')
		
		matrix_frame = ttk.Frame(frame, padding=5)
		matrix_frame.grid(column=1, row=0, sticky='N E S')
		self.arbitrary_matrix = []
		for row in range(0,2):
			self.arbitrary_matrix.append([])
			for column in range(0,2):
				cell_var = tk.DoubleVar()
				cell_var.set(0)
				ttk.Entry(matrix_frame, width=6, textvariable=cell_var).grid(column=column, row=row)
				self.arbitrary_matrix[row].append(cell_var)
		return frame
	
	def color_choose_action(self):
		_, self.color = tkcc.askcolor()
	
	def ok_action(self):
		self.trafo = self.nb.tab(self.nb.select(), 'text')
		self.destroy()
	
	def cancel_action(self):
		self.trafo = None
		self.destroy()
	
	@classmethod
	def get_values(cls, program, data):
		window = cls(program, data)
		window.wait_window()
		
		if window.trafo is not None:
			selected_datasets = [b.get() for b in window.selected_datasets]
			
			if window.trafo == 'Arbitrary':
				matrix = window.arbitrary_matrix
				parameters = [[var.get() for var in row] for row in matrix]
			
			return window.trafo, parameters, selected_datasets
		else:
			return None

class Point_Cloud(plugin.Plugin):
	def __init__(self):
		self.name = 'Point cloud'
		
		self.data['gui'].data_frame.add_action('New from distribution', 'pq_new_from_distribution', None)
		self.data['gui'].data_frame.add_action('Transform', 'pq_transform', None)
		self.data['gui'].data_frame.add_action('Clear', 'pq_clear', None)
		self.register_event_handler('pq_new_from_distribution', self.new_from_distribution)
		self.register_event_handler('pq_transform', self.transform)
		self.register_event_handler('pq_clear', self.clear)
		self.register_event_handler('redraw', self.draw)
	
	def new_from_distribution(self, event):
		result = Distribution_Query_Window.get_values(self.data['gui'])
		
		if result is not None:
			distribution, parameters, count, color = result
			
			if distribution == 'Uniform':
				points_x1 = np.random.uniform(parameters['x1_min'], parameters['x1_max'], (count, 1))
				points_x2 = np.random.uniform(parameters['x2_min'], parameters['x2_max'], (count, 1))
				points = np.column_stack([points_x1, points_x2])
			elif distribution == 'Normal':
				#~ pass # TODO implement this
				points_x1 = np.random.normal(parameters['x1_mean'], parameters['x1_std_dev'], (count, 1))
				points_x2 = np.random.normal(parameters['x2_mean'], parameters['x2_std_dev'], (count, 1))
				points = np.column_stack([points_x1, points_x2])
			else:
				raise Exception('Unknown distribution')
			
			try:
				self.data['points'].append( (points, color) )
			except KeyError:
				self.data['points'] = [ (points, color) ]
			self.data['gui'].redraw()
	
	def transform(self, event):
		try:
			datasets = self.data['points']
		except KeyError:
			datasets = []
		result = Transformation_Query_Window.get_values(self.data['gui'], datasets)
		
		if result is not None:
			trafo, transform_data, selected_datasets = result
			
			if trafo == 'Arbitrary':
				transform_matrix = np.empty(shape=(2,2))
				for row, row_data in enumerate(transform_data):
					transform_matrix[row,:] = row_data
				
				for index, decision in enumerate(selected_datasets):
					if decision:
						points, color = self.data['points'][index]
						points = ( np.dot(transform_matrix, points.T) ).T
						self.data['points'][index] = (points, color)
			self.data['gui'].redraw()
	
	def clear(self, event):
		self.data['points'] = []
		self.data['gui'].redraw()
	
	def draw(self, event):
		canvas = self.data['gui'].get_canvas()
		try:
			data = self.data['points']
		except KeyError:
			return # No data (yet), that's ok.
		for point_set, color in data:
			for point in point_set:
				canvas.create_oval(point[0], point[1], point[0], point[1], fill=color, outline=color)
	
	def unload(self):
		self.data['gui'].data_frame.remove_action('New from distribution')
		self.data['gui'].data_frame.remove_action('Clear')
		try:
			del self.data['points']
		except KeyError:
			pass
		self.data['gui'].redraw()






