import tkinter as tk
import tkinter.ttk as ttk
import plugin

class Axes(plugin.Plugin):
	def __init__(self):
		self.name = 'Axes'
		
		self.axes_active = True
		self.data['gui'].data_frame.add_action('Toggle axes', 'ax_toggle_axes', None)
		self.register_event_handler('redraw', self.draw)
		self.register_event_handler('ax_toggle_axes', self.toggle_axes)
		
		self.register_event_handler('plugin_loaded', self.plugin_load_handler)
		
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
	
	def plugin_load_handler(self, event):
		if event[1] == self.name:
			self.plugin_manager.notify_all( ('redraw', None) )
	
	def unload(self):
		self.axes_active = False
		self.data['gui'].data_frame.remove_action('Toggle axes')
		self.data['gui'].redraw()
