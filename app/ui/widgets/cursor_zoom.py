import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, GLib
from Xlib import display, X
from PIL import Image
import io

class ZoomPreview(Gtk.Window):
    def __init__(self, main_window, zoom:int=5, size:int=120):
        super().__init__()
        self.main_window = main_window
        self.zoom = zoom
        self.size = size

        self.set_decorated(False)
        self.set_default_size(size, size)
        self.add_css_class("zoom-preview")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.image = Gtk.Image()
        self.label = Gtk.Label(label="")
        self.label.set_xalign(0.5)
        vbox.append(self.image)
        vbox.append(self.label)
        self.set_child(vbox)

        self.present()  # πρέπει για να δημιουργηθεί το Gdk.Window
        # gdk_window = self.get_window()
        # if gdk_window:
        #     gdk_window.set_type_hint(Gdk.WindowTypeHint.UTILITY)

        # X11 display
        self.dpy = display.Display()
        self.root = self.dpy.screen().root

        self.timeout_id = GLib.timeout_add(30, self.update_preview)

    def update_preview(self)-> None:
        data = self.root.query_pointer()
        x, y = data.root_x, data.root_y

        # Move preview window δίπλα στον cursor
        self.move(x + 20, y + 20)

        # Capture μικρή περιοχή γύρω από τον cursor
        half = self.size // (2 * self.zoom)
        raw = self.root.get_image(x - half, y - half, self.size // self.zoom, self.size // self.zoom, X.ZPixmap, 0xFFFFFFFF)
        img = Image.frombytes("RGB", (self.size // self.zoom, self.size // self.zoom), raw.data, "raw", "BGRX")
        img = img.resize((self.size, self.size), Image.NEAREST)

        # Μετατροπή σε Gdk.Texture για GTK4
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        stream = Gio.MemoryInputStream.new_from_bytes(GLib.Bytes.new(buf.read()))
        pixbuf = Gdk.Texture.new_from_stream(stream, None)

        self.image.set_paintable(pixbuf)

        # RGB & HEX pixel στο κέντρο
        center_pixel = img.getpixel((self.size//2, self.size//2))
        r, g, b = center_pixel
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        self.label.set_text(f"RGB: {r},{g},{b} | HEX: {hex_color}")

        return True

