from Xlib import display, X, protocol, error
from gi.repository import Gtk
from typing import Tuple

from typing import Protocol, Tuple

class IBackend(Protocol):
    def bind_window(self, window) -> None: ...
    def get_screen_dimensions(self) -> Tuple[int,int]: ...
    def get_mouse_position(self) -> Tuple[int,int]: ...
    def move_window(self, posX:int, posY:int, offset_x:int, offset_y:int, size:int) -> None: ...
    def capture_image(self, posX:int, posY:int, capture_size:int) -> bytes | None: ...
    def get_color_under_cursor(self) -> Tuple[int,int,int]: ...
    def set_window_on_top(self) -> None: ...


# This class provides the low level functions from the X11

class BackendX11:
    def __init__(self):
        self.dpy = display.Display()
        self.root = self.dpy.screen().root
        self.xid = None


    def bind_window(self, window: Gtk.ApplicationWindow):
        surface = window.get_surface()
        self.xid = surface.get_xid()  # X11 only


    # get the width and the heigh of the screen
    def get_screen_dimensions(self) -> Tuple[int, int]:
        width = self.root.get_geometry().width
        height = self.root.get_geometry().height
        return width, height


   # get the position of the mouse
    def get_mouse_position(self) -> Tuple[int, int]:
        data = self.root.query_pointer()._data
        return data["root_x"], data["root_y"]
    

    # move the window
    def move_window(self, posX: int, posY:int, offset_x:int, offset_y:int, size:int) -> None:
        if not self.xid:
            return

        screen_w, screen_h = self.get_screen_dimensions()

        if posX + size + offset_x > screen_w:
            offset_x = -size - offset_x
        if posY + size + offset_y > screen_h:
            offset_y = -size - offset_y

        win = self.dpy.create_resource_object("window", self.xid)
        win.configure(x=int(posX + offset_x), y=int(posY + offset_y))
        self.dpy.flush()


    # capture the image under the mouse and in a specific size around it
    def capture_image(self, posX: int, posY: int, capture_size: int) -> bytes | None:
        screen_width, screen_height = self.get_screen_dimensions()
        half = capture_size // 2

        x = max(0, min(posX - half, screen_width - capture_size))
        y = max(0, min(posY - half, screen_height - capture_size))

        try:
            image = self.root.get_image(
                x, y,
                capture_size, capture_size,
                X.ZPixmap,
                0xFFFFFFFF
            )
            if not image:
                return None

            return bytes(image.data)

        except error.BadMatch:
            return None

 
    # get the color of the pixel under the mouse
    def get_color_under_cursor(self):
        data = self.root.query_pointer()
        x, y = data.root_x, data.root_y

        raw = self.root.get_image(x, y, 1, 1, X.ZPixmap, 0xFFFFFFFF)
        b, g, r = raw.data[:3]

        return r, g, b
    

    # set the window on top of every other
    def set_window_on_top(self):
        if not self.xid:
            return

        net_wm_state = self.dpy.intern_atom("_NET_WM_STATE")
        above = self.dpy.intern_atom("_NET_WM_STATE_ABOVE")

        ev = protocol.event.ClientMessage(
            window=self.xid,
            client_type=net_wm_state,
            data=(32, [1, above, 0, 0, 0])
        )

        self.root.send_event(
            ev,
            event_mask=X.SubstructureRedirectMask | X.SubstructureNotifyMask
        )
        self.dpy.flush()


class BackendWayland:
    def __init__(self):
        self.initialized = False
        ...

    def bind_window(self, window):
        pass

    def get_screen_dimensions(self):
        return 0, 0  # θα το γεμίσουμε από screencast info

    def get_mouse_position(self):
        return 0, 0  # pointer tracking μέσω portal ή frame

    def move_window(self, posX, posY, offset_x, offset_y, size):
        pass

    def capture_image(self, posX, posY, capture_size):
        return None  # ή από PipeWire frame

    def get_color_under_cursor(self):
        return 0, 0, 0

    def set_window_on_top(self):
        pass



    

    
    
   