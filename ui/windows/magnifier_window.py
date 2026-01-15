import gi, os
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk, Gdk, GLib
from nKolor.ui.widgets.crosshair import Crosshair
from nKolor.utils.color import Color
from nKolor.ui.widgets.color_view import ColorView, ColorViewType

# if os.environ.get("WAYLAND_DISPLAY"):
#     from app.utils.backend import BackendWayland as Backend
# else:
from nKolor.utils.backend import BackendX11 as Backend


class MagnifierWindow(Gtk.ApplicationWindow):
    def __init__(self):
        super().__init__()

        self.backend = Backend()
        self.current_color = Color()
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


    def buid_ui(self)->None:
        root_child = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=0)
        root_child.add_css_class("magnifier-window")
        self.set_child(root_child)

        # color preview
        self.color_preview = ColorView(self.size, 25, self.current_color, ColorViewType.SQUARE)
        root_child.append(self.color_preview)

        # zoom area
        zoom = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        overlay = Gtk.Overlay()
        self.background = Gtk.Picture()
        self.background.set_size_request(self.size, self.size)
        overlay.set_child(self.background)
        self.crosshair = Crosshair()
        overlay.add_overlay(self.crosshair)
        zoom.append(overlay)
        root_child.append(zoom)


    # update the preview color
    def update_preview(self)->None:
        self.color_preview.set_color(self.current_color)
        

    # display the window and start scanning the surface of the screen
    def start(self)->None:
        if self.running:
            return

        self.running = True
        self.show()
        self.backend.bind_window(self)
        self.backend.set_window_on_top()

        GLib.timeout_add(16, self.tick)


    # close the window and stop scanning the surface of the screen
    def stop(self):
        self.running = False
        self.hide()


    # actions to take in every frame
    def tick(self)-> bool:
        if not self.running:
            return False

        mouseX, mouseY = self.backend.get_mouse_position()

        self.backend.move_window(mouseX, mouseY, self.offset, self.offset, self.size)
        captured_image = self.backend.capture_image(mouseX, mouseY, self.capture_size)
        self.update_background(captured_image)
        self.update_cursor()
        self.update_color()

        return True  # continue timeout


    # update the position of the cursor
    def update_cursor(self):
        self.crosshair.set_position(self.size // 2, self.size // 2)
    

    # update the color from the pixel under the mouse
    def update_color(self):
        try:
            r, g, b = self.backend.get_color_under_cursor()
            self.current_color = Color(r, g, b)
            self.update_preview()
        except Exception:
            pass


    # update the zoom background from an array of bytes
    def update_background(self, data: bytes | None) -> bool:
        try:
            if data is None:
                data = bytes(
                    [128, 128, 128, 255] *
                    (self.capture_size * self.capture_size)
                )

            texture = Gdk.MemoryTexture.new(
                self.capture_size,
                self.capture_size,
                Gdk.MemoryFormat.B8G8R8A8,
                GLib.Bytes.new(data),
                self.capture_size * 4
            )
            self.background.set_paintable(texture)
            return True
        except Exception as e:
            print(f"[Magnifier] texture update failed: {e}")
            return False
