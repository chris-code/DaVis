import sys
import os
import importlib
import inspect

class Plugin_Manager():
	def __init__(self):
		#~ Set values that should be available to all plugins
		Plugin.plugin_manager = self
		Plugin.data = {}
		
		#~ The list of loaded plugins
		self.plugins = []
	
	def notify_all(self, event):
		for plugin in self.plugins:
			plugin._handle(event)
	
	def load(self, path):
		sys.path.append(os.path.dirname(path))
		try:
			#~ Load module
			mname = os.path.splitext(os.path.basename(path))[0]
			imported = importlib.import_module(mname)
		except ImportError:
			error_string = 'Could not load plugin\n{0}\nCheck your plugin.conf'
			print(error_string.format(path))
			#~ program.show_warning(error_string.format(plugin_path), 'Plugin error')
		except Exception as e:
			error_string = 'Error while loading\n{0}\nThe plugin said:\n{1}'
			print(error_string.format(path, e))
			#~ program.show_warning(error_string.format(plugin_path, e), 'Plugin error')
		else:
			#~ Instantiate (and thus load) every plugin in there
			for name, obj in inspect.getmembers(imported):
				if inspect.isclass(obj) and issubclass(obj, Plugin):
					plugin = obj() # Instantiate plugin
					self.plugins.append(plugin) # Add plugin to list
					self.notify_all( ('plugin_loaded', plugin) )
		finally:
			sys.path.pop()
	
	def unload(self, plugin):
		plugin.unload()
		self.plugins.remove(plugin)
		self.notify_all( ('plugin_unloaded', plugin) )

class Plugin():
	def register_event_handler(self, event_id, handler):
		try:
			self._event_handlers[event_id] = handler
		except AttributeError:
			self._event_handlers = {event_id: handler}
	
	#~ Plugins that made lasting changes to the program should overwrite this and
	#~ undo those changes here. Your plugin most likely falls into this category.
	#~ Examples of 'lasting' changes include
	#~ - adding / modifying GUI elements
	#~ - adding data to the shared data pool self.data
	#~ A counter example would be a plugin that just displays a splash screen. In short,
	#~ after unload finishes the program should be like the plugin was never loaded in
	#~ the first place.
	def unload(self):
		pass
	
	def _handle(self, event):
		event_id, event_appendix = event
		try:
			handler = self._event_handlers[event_id]
		except AttributeError:
			pass # Plugin never registered a single handler, so self._event_handlers doesn't exist.
		except KeyError:
			pass # Plugin doesn't handle this event, that's ok.
		else:
			handler(event)
