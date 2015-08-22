import plugin

plugin_config_path = '../plugins/plugins.conf'

plugin_manager = plugin.Plugin_Manager()
with open(plugin_config_path) as config:
		for plugin_path in config:
			plugin_manager.load(plugin_path=plugin_path)

#~ This is a dirty hack because tkinter has threading issues
for func in plugin.Plugin.data['run_after_init']:
	func()
