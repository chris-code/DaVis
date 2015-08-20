import tkinter as tk
import tkinter.ttk as ttk
import plugin

class Axes(plugin.Plugin):
	def __init__(self):
		super().__init__()
		
		self.axes_active = True
		self.data['gui'].data_frame.add_action('Toggle axes', 'ax_toggle_axes', None)
		self.register_event_handler('redraw', self.draw)
		self.register_event_handler('ax_toggle_axes', self.toggle_axes)
	
	#~ TODO more intelligent redrawing based on canvas object ids?
	def toggle_axes(self, event):
		self.axes_active = not self.axes_active
		self.data['gui'].redraw()
	
	#~ TODO make axes length dependent on data
	def draw(self, event):
		if self.axes_active:
			canvas = self.data['gui'].get_canvas()
			canvas.create_line(-100, 0, 100, 0)
			canvas.create_line(0, -100, 0, 100)
