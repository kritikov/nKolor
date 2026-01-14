from gi.repository import Gtk, Gdk
from nKolor.ui.windows.main_window import MainWindow

class ColorPickerApp(Gtk.Application):

    def __init__(self) -> None:
        super().__init__(application_id="com.nick.colorpicker")

    def do_activate(self):
        self.load_css()
        win = MainWindow(self)
        win.present()

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("nKolor/resources/css/main.css")

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
