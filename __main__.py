import gi
gi.require_version("Gtk", "4.0")

from nKolor.application import ColorPickerApp

app = ColorPickerApp()
app.run()
