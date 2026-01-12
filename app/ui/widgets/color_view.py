from gi.repository import Gtk, Gdk, GObject
from app.utils.color import Color
import math
from enum import Enum


class ColorViewType(Enum):
    SQUARE = "square"
    CIRCLE = "circle"


class ColorView(Gtk.DrawingArea):

    __gsignals__ = {
        "clicked": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
    }

    def __init__(self, width: int = 20, height: int = 20, 
                 color: Color = Color(242, 242, 242), 
                 view_type: ColorViewType = ColorViewType.SQUARE,
                 clickable: bool = True):
        super().__init__()

        self.color = color
        self.view_type = view_type
        
        self.set_size_request(width, height)
        self.set_hexpand(False)
        self.set_vexpand(False)
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)

        gesture = Gtk.GestureClick()
        gesture.set_button(Gdk.BUTTON_PRIMARY)
        gesture.connect("released", self.on_clicked)
        self.add_controller(gesture)

        self.set_draw_func(self.on_draw)

        # Pointer cursor όταν μπαίνει το ποντίκι
        if clickable == True:
            motion = Gtk.EventControllerMotion()
            motion.connect("enter", self.on_mouse_enter)
            motion.connect("leave", self.on_mouse_leave)
            self.add_controller(motion)

    def on_mouse_enter(self, *args)-> None:
        cursor = Gdk.Cursor.new_from_name("pointer")
        self.set_cursor(cursor)  
        return True

    def on_mouse_leave(self, *args)-> None:
        self.set_cursor(None) 
        return True  


    # fill the contents of the widget with a custom draw
    def on_draw(self, widget, cr, width:float, height:float)-> None:
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()

        border_width = 1
        half_border = border_width / 2

        # fill color
        r_n, g_n, b_n = self.color.rgb_normalized
        cr.set_source_rgb(r_n, g_n, b_n)

        # shape
        if self.view_type == ColorViewType.SQUARE:
            cr.rectangle(
                half_border,
                half_border,
                width - border_width,
                height - border_width
            )
        elif self.view_type == ColorViewType.CIRCLE:
            radius = (min(width, height) - border_width) / 2
            cr.arc(
                width / 2,
                height / 2,
                radius,
                0,
                2 * math.pi
            )

        cr.fill_preserve()

        # border
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(border_width)
        cr.stroke()

        return False
    

    # Set the color of the widget
    def set_color(self, color: Color)-> None:
        self.color = color
        self.queue_draw()


    # signal when the widget is clicked
    def on_clicked(self, gesture, n_press, x, y)-> None:
        self.emit("clicked", self.color)


 