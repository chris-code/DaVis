import gui
import plugin_base

mw = gui.Main_window(plugin_base.Plugin_Base)
plugin_base.load_plugins(mw)

mw.after(100, mw.redraw)
mw.mainloop()






