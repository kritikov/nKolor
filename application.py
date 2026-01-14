from gi.repository import Gtk, Gdk
from nKolor.ui.windows.main_window import MainWindow
from nKolor.resources.resources import Resources

class ColorPickerApp(Gtk.Application):

    def __init__(self) -> None:
        super().__init__(application_id="com.nick.colorpicker")

    def do_activate(self):
        self.load_css()
        win = MainWindow(self)
        win.present()

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_path = Resources.css("main.css")
        css_provider.load_from_path(css_path)

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
