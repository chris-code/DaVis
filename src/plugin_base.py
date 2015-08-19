import sys
import os
import inspect
import importlib

plugin_config_path = '../plugins/plugins.conf'

#~ Plugins should subclass this
class Plugin_Base():
	#~ The list of all plugins.
	_plugin_list = []
	
	#~ Dispatches an event to all plugins
	@classmethod
	def _notify_all(cls, event):
		for plugin in cls._plugin_list:
			plugin._handle(event)
	
	#~ If a plugin overwrites this constructor, it shall call this one via super().
	#~ Thus, 'super().__init__()' would be a reasonable first line for a plugin's __init__ method.
	def __init__(self):
		self._plugin_list.append(self)
		self._event_handlers = {}
	
	#~ Dispatches an event to this plugin's registered handler.
	def _handle(self, event):
		event_id, event_appendix = event
		try:
			handler = self._event_handlers[event_id]
		except KeyError:
			return # Plugin doesn't handle this event, that's ok.
		handler(event)
	
	#~ With this method, your plugin can register handlers for certain events.
	#~ The handler should accept one parameter, event, which is a 2-tuple of
	#~ - the event_id (a string that identifies a type of event)
	#~ - an event-dependent arbitrary object (might be None) that helps process the event
	def register_event_handler(self, event_id, handler):
		self._event_handlers[event_id] = handler

#~ Procedure that will load plugins found in plugin_config_path file.
def load_plugins(program):
	Plugin_Base.program = program # Make program accessible to all plugins
	
	with open(plugin_config_path) as config:
		for plugin_path in config:
			sys.path.append(os.path.dirname(plugin_path))
			try:
				#~ Load module
				mname = os.path.splitext(os.path.basename(plugin_path))[0]
				imported = importlib.import_module(mname)
			except ImportError:
				error_string = 'Could not load plugin\n{0}\nCheck your plugin.conf'
				program.show_warning(error_string.format(plugin_path), 'Plugin error')
			except Exception as e:
				error_string = 'Error while loading\n{0}\nThe plugin said:\n{1}'
				program.show_warning(error_string.format(plugin_path, e), 'Plugin error')
			else:
				#~ Instantiate (and thus load) every plugin in there
				for name, obj in inspect.getmembers(imported):
					if inspect.isclass(obj) and issubclass(obj, Plugin_Base):
						obj()
			finally:
				sys.path.pop()
			










