import sys
import os
import importlib
import inspect

class Plugin_Manager():
	def __init__(self):
		#~ Set values that should be available to all plugins
		Plugin.plugin_manager = self
		Plugin.data = {}
		
		#~ The dict of plugins, as a tuple of (plugin_object, path)
		self.plugins = {}
	
	def notify_all(self, event):
		for plugin, path in self.plugins.values():
			if plugin is not None:
				plugin._handle(event)
	
	def list_of_plugins(self):
		return self.plugins
	
	def load(self, plugin_name=None, plugin_path=None):
		if plugin_path is None:
			plugin_path = self.plugins[plugin_name][1]
		
		sys.path.append(os.path.dirname(plugin_path))
		try:
			#~ Load module
			mname = os.path.splitext(os.path.basename(plugin_path))[0]
			imported = importlib.import_module(mname)
		except ImportError:
			error_string = 'Could not load plugin\n{0}\nCheck your plugin.conf'
			print(error_string.format(plugin_path))
		except Exception as e:
			error_string = 'Error while loading\n{0}\nThe plugin said:\n{1}'
			print(error_string.format(plugin_path, e))
		else:
			#~ Instantiate (and thus load) every plugin in there
			for name, obj in inspect.getmembers(imported):
				if inspect.isclass(obj) and issubclass(obj, Plugin):
					plugin = obj() # Instantiate plugin
					self.plugins[plugin.name] = (plugin, plugin_path) # Add plugin to active plugins
					self.notify_all( ('plugin_loaded', plugin.name) )
		finally:
			sys.path.pop()
	
	def unload(self, plugin_name=None, plugin_object=None):
		if plugin_object is None:
			plugin_object = self.plugins[plugin_name][0]
		if plugin_name is None:
			for key, value in self.plugins.items():
				if value is plugin_object:
					plugin_name = key
		self.notify_all( ('plugin_unloading', plugin_name) )
		plugin_object.unload()
		path = self.plugins[plugin_name][1]
		self.plugins[plugin_name] = (None, path)
		self.notify_all( ('plugin_unloaded', plugin_name) )
	
	def unload_all(self):
		for plugin_name in self.plugins.keys():
			self.unload(plugin_name=plugin_name)

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
		raise Exception('ERROR: Plugin {0} did not overwrite \'unload\' method'.format(self.name))
	
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
