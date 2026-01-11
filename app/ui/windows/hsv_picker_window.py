import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject
from app.utils.color import Color
from app.ui.widgets.crosshair import Crosshair
from app.ui.widgets.hue_slider import HueSlider
from app.ui.widgets.color_view import ColorView, ColorViewType
import colorsys, cairo


class HSVPickerWindow(Gtk.Window):

    __gsignals__ = {
        "color_selected": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
    }

    def __init__(self, app: Gtk.Application):
        super().__init__(title="HSV Picker")

        self.set_default_size(360, 280)
        self.hue = 0.0
        self.saturation = 0.0
        self.value = 1.0

        rgb = Color.hsv_to_rgb(self.hue, self.saturation, self.value)
        self.color = Color(*rgb)

        self.sv_surface = None

        self.build_ui()


    def build_ui(self) -> None:
        root_child = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        root_child.add_css_class("window-root-child")
        self.set_child(root_child)
        
        first_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        root_child.append(first_row)
        second_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        root_child.append(second_row)

        # 2D HSV area
        hs_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        overlay = Gtk.Overlay()
        hs_box.append(overlay)
        first_row.append(hs_box)

        self.sv_area = Gtk.DrawingArea()
        self.sv_area.set_content_width(256)
        self.sv_area.set_content_height(256)
        self.sv_area.set_draw_func(self.draw_sv)
        self.rebuild_sv_surface()
        overlay.set_child(self.sv_area)

        self.crosshair = Crosshair()
        self.crosshair.set_position(0, 0)
        self.crosshair.set_can_target(False)
        overlay.add_overlay(self.crosshair)

        gesture = Gtk.GestureDrag()
        gesture.connect("drag-begin", self.on_drag_begin)
        gesture.connect("drag-update", self.on_drag_update)
        self.sv_area.add_controller(gesture)

        # hue slider
        self.hue_slider = HueSlider(initial_hue=self.hue)
        self.hue_slider.connect("hue_changed", self.on_hue_changed)
        first_row.append(self.hue_slider)

        # color preview
        self.color_preview = ColorView(120, 30, self.color, ColorViewType.SQUARE, False)
        second_row.append(self.color_preview)

        # buttons
        buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        buttons.set_halign(Gtk.Align.CENTER)
        cancel = Gtk.Button(label="Cancel")
        cancel.connect("clicked", lambda *_: self.close())
        ok = Gtk.Button(label="Apply")
        ok.add_css_class("suggested-action")
        ok.connect("clicked", self.on_apply_color)
        buttons.append(cancel)
        buttons.append(ok)
        second_row.append(buttons)


    # fill the hs area with colors
    def draw_sv(self, area, cr, width, height):
        if self.sv_surface:
            cr.set_source_surface(self.sv_surface, 0, 0)
            cr.paint()


    # ================= EVENTS =================

    def on_drag_begin(self, gesture, start_x, start_y)->None:
        self.drag_start_x = start_x
        self.drag_start_y = start_y
        self.crosshair.set_position(start_x, start_y)


    def on_drag_update(self, gesture, offset_x, offset_y):
        abs_x = self.drag_start_x + offset_x
        abs_y = self.drag_start_y + offset_y

        alloc = self.sv_area.get_allocation()
        abs_x = max(0, min(abs_x, alloc.width))
        abs_y = max(0, min(abs_y, alloc.height))

        # S: αριστερά → δεξιά (0 → 1)
        self.saturation = abs_x / alloc.width

        # V: πάνω → κάτω (1 → 0)
        self.value = 1.0 - (abs_y / alloc.height)

        self.crosshair.set_position(abs_x, abs_y)
        self.update_color()




    def update_color(self)->None:
        rgb = Color.hsv_to_rgb(self.hue, self.saturation, self.value)
        self.color.rgb = rgb
        self.color_preview.set_color(self.color)
        


    def on_apply_color(self, *_)->None:
        self.emit("color_selected", self.color)
        self.close()


    def on_hue_changed(self, widget, hue):
        self.hue = hue
        self.rebuild_sv_surface()
        self.sv_area.queue_draw()
        self.update_color()


    def rebuild_sv_surface(self):
        w = h = 256
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
        cr = cairo.Context(surface)

        # --- Saturation gradient (X)
        r, g, b = Color.hsv_to_rgb_normalized(self.hue, 1, 1)
        sat_grad = cairo.LinearGradient(0, 0, w, 0)
        sat_grad.add_color_stop_rgb(0, 1, 1, 1)       # S=0 → white
        sat_grad.add_color_stop_rgb(1, r, g, b)       # S=1 → hue

        cr.set_source(sat_grad)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        # --- Value gradient (Y)
        val_grad = cairo.LinearGradient(0, 0, 0, h)
        val_grad.add_color_stop_rgba(0, 0, 0, 0, 0)   # V=1
        val_grad.add_color_stop_rgba(1, 0, 0, 0, 1)   # V=0

        cr.set_source(val_grad)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        self.sv_surface = surface

