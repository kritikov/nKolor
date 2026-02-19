import gi
gi.require_version("Gtk", "4.0")

from nkolor.application import ColorPickerApp

app = ColorPickerApp()
app.run()
