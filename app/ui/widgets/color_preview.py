from gi.repository import Gtk, GObject
from app.utils.color import Color
from app.ui.widgets.color_view import ColorView
from app.ui.widgets.color_view import ColorViewType


class ColorPreview(Gtk.Box):

    __gsignals__ = {
            "similar_color_selected": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
        }

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.color = Color(242, 242, 242)   # initial color: gray
        self.set_size_request(100, -1)
        self.build_ui()


    def build_ui(self):
        self.preview = ColorView(50, 50, self.color, ColorViewType.SQUARE, False)
        self.append(self.preview)

        similar_colors = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=6
        )
        similar_colors.set_halign(Gtk.Align.CENTER)
        similar_colors.set_valign(Gtk.Align.CENTER)

        self.similar_color_1 = ColorView(20, 20, self.color, ColorViewType.SQUARE)
        self.similar_color_1.connect("clicked", self.on_similar_color_select)
        self.similar_color_1.set_tooltip_text("lighter")
        similar_colors.append(self.similar_color_1)

        self.similar_color_2 = ColorView(20, 20, self.color, ColorViewType.SQUARE)
        self.similar_color_2.connect("clicked", self.on_similar_color_select)
        self.similar_color_2.set_tooltip_text("darker")
        similar_colors.append(self.similar_color_2)

        self.similar_color_3 = ColorView(20, 20, self.color, ColorViewType.SQUARE)
        self.similar_color_3.connect("clicked", self.on_similar_color_select)
        self.similar_color_3.set_tooltip_text("less saturated")
        similar_colors.append(self.similar_color_3)

        self.similar_color_4 = ColorView(20, 20, self.color, ColorViewType.SQUARE)
        self.similar_color_4.connect("clicked", self.on_similar_color_select)
        self.similar_color_4.set_tooltip_text("more saturated")
        similar_colors.append(self.similar_color_4)

        self.append(similar_colors)


    # change the color of the preview and the similar colors
    def set_color(self, color: Color):
        self.preview.set_color(color)

        variants = color.get_variants()
        self.similar_color_1.set_color(variants[0])
        self.similar_color_2.set_color(variants[1])
        self.similar_color_3.set_color(variants[2])
        self.similar_color_4.set_color(variants[3])


    # signal when a similar color is selected
    def on_similar_color_select(self, widget, color):
        self.emit("similar_color_selected", color)
 
