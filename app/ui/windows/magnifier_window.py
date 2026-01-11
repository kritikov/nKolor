import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk, Gdk, GLib
from app.utils.backend import Backend
from app.ui.widgets.crosshair import Crosshair
from app.utils.color import Color
from app.ui.widgets.color_view import ColorView, ColorViewType


class MagnifierWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.backend = Backend()
        self.current_color = Color(255, 255, 255)  # default white
        self.capture_size = 30
        self.magnification = 5
        self.offset = 20
        self.running = False

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_focusable(False)
        self.set_opacity(0.95)

        self.size = int(self.capture_size * self.magnification)
        self.set_default_size(self.size, self.size)

        self.buid_ui()


    def buid_ui(self):
        root_child = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=0)
        root_child.add_css_class("magnifier-window")
        self.set_child(root_child)

        # color preview area
        self.color_preview = ColorView(self.size, 25, self.current_color, ColorViewType.SQUARE)
        root_child.append(self.color_preview)

        # zoom area
        zoom = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        overlay = Gtk.Overlay()
        self.picture = Gtk.Picture()
        overlay.set_child(self.picture)
        self.crosshair = Crosshair()
        overlay.add_overlay(self.crosshair)
        zoom.append(overlay)
        root_child.append(zoom)


    # update the preview color
    def update_color_preview(self):
        self.color_preview.set_color(self.current_color)
        

    def start(self):
        if self.running:
            return

        self.running = True
        self.show()

        surface = self.get_surface()
        xid = surface.get_xid()

        self.backend.bind_window(xid)
        self.backend.set_window_on_top()

        GLib.timeout_add(16, self.tick)

    def stop(self):
        self.running = False
        self.hide()

    # -------------------------------------------------

    def tick(self):
        if not self.running:
            return False

        # --- screen info ---
        screen_w = self.backend.screen_width()
        screen_h = self.backend.screen_height()
        win_w = int(self.capture_size * self.magnification)
        win_h = int(self.capture_size * self.magnification)
        half = self.capture_size // 2

        # --- cursor position ---
        mx, my = self.backend.get_mouse_position()

        # --- calculate capture area (clamped) ---
        x = mx - half
        y = my - half

        if x + self.capture_size > screen_w:
            x = screen_w - self.capture_size
        if y + self.capture_size > screen_h:
            y = screen_h - self.capture_size
        x = max(0, x)
        y = max(0, y)

        # --- dynamic window offset ---
        offset_x = self.offset
        offset_y = self.offset

        if mx + win_w + self.offset > screen_w:
            offset_x = -win_w - self.offset
        if my + win_h + self.offset > screen_h:
            offset_y = -win_h - self.offset

        self.backend.move_window(mx + offset_x, my + offset_y)

        # --- capture image ---
        img = self.backend.capture_area(x, y, self.capture_size, self.capture_size)

        # --- update texture ---
        size = int(self.capture_size * self.magnification)
        if img:
            try:
                data = bytes(img.data)
                texture = Gdk.MemoryTexture.new(
                    self.capture_size,
                    self.capture_size,
                    Gdk.MemoryFormat.B8G8R8A8,
                    GLib.Bytes.new(data),
                    self.capture_size * 4
                )
                self.picture.set_paintable(texture)
            except Exception as e:
                print(f"[Magnifier] update_texture failed: {e}")
                img = None

        # fallback: solid gray if capture failed
        if not img:
            try:
                fallback_data = bytes([128, 128, 128, 255] * (self.capture_size * self.capture_size))
                texture = Gdk.MemoryTexture.new(
                    self.capture_size,
                    self.capture_size,
                    Gdk.MemoryFormat.B8G8R8A8,
                    GLib.Bytes.new(fallback_data),
                    self.capture_size * 4
                )
                self.picture.set_paintable(texture)
            except Exception as e:
                print(f"[Magnifier] fallback texture failed: {e}")

        # --- update crosshair ---
        self.picture.set_size_request(size, size)
        self.crosshair.set_position(size/2, size/2)

        # --- update current color ---
        try:
            r, g, b = self.backend.get_color_under_cursor()
            self.current_color = Color(r, g, b)
            self.update_color_preview()
        except Exception:
            pass

        return True  # continue timeout

