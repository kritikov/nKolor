import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject

from collections import deque
from nKolor.utils.color import Color
from nKolor.ui.widgets.color_view import ColorView
from nKolor.ui.widgets.color_view import ColorViewType

class HistoryBar(Gtk.ScrolledWindow):
    
    __gsignals__ = {
        "color_selected": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
    }

    @property
    def last_color(self) -> Color:
        last_color = self.colors[-1] if self.colors else None
        return last_color


    def __init__(self):
        super().__init__()

        self.max_colors: int = 100
        self.colors: deque[Color] = deque(maxlen=self.max_colors)
        self.set_hexpand(True)
        self.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.NEVER
        )
        self.build_ui()
        

    def build_ui(self)-> None:
        self.colors_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8
        )
        self.set_child(self.colors_box)

        self.add_css_class("history_bar")

    # add a color in the history
    def add_color(self, color: Color)-> None:
        self.adjust_widgets_size()
        self.colors.append(color)
        self.add_color_widget(color)


    # if colors in history are full then remove the first widget
    def adjust_widgets_size(self)-> None:
        if len(self.colors) == self.colors.maxlen:
            first_child = self.colors_box.get_first_child()
            if first_child:
                self.colors_box.remove(first_child)


    # add a widget in the history based on a color
    def add_color_widget(self, color:Color)-> None:
        circle = ColorView(28, 28, color, ColorViewType.CIRCLE)
        circle.connect("clicked", self.on_color_select)
        self.colors_box.prepend(circle)


    # signal when a color is selected
    def on_color_select(self, widget, color:Color)-> None:
        self.emit("color_selected", color)
