from Xlib import display, X, protocol, error

# This class provides the low level functions from the X11

class Backend:
    def __init__(self):
        self.dpy = display.Display()
        self.root = self.dpy.screen().root
        self.xid = None

    # -----------------------------
    # Window handling
    # -----------------------------

    def bind_window(self, xid: int):
        """Bind GTK window XID to backend"""
        self.xid = xid

    def move_window(self, x: int, y: int):
        if not self.xid:
            return
        win = self.dpy.create_resource_object("window", self.xid)
        win.configure(x=int(x), y=int(y))
        self.dpy.flush()

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


    # -----------------------------
    # Mouse
    # -----------------------------

    def get_mouse_position(self):
        data = self.root.query_pointer()._data
        return data["root_x"], data["root_y"]


    # -----------------------------
    # Screen capture
    # -----------------------------

    def capture_area(self, x, y, width, height):
        try:
            return self.root.get_image(x, y, width, height, X.ZPixmap, 0xFFFFFFFF)
        except error.BadMatch:
            return None

    # get the color of the pixel under the mouse
    def get_color_under_cursor(self):
        data = self.root.query_pointer()
        x, y = data.root_x, data.root_y

        raw = self.root.get_image(x, y, 1, 1, X.ZPixmap, 0xFFFFFFFF)
        b, g, r = raw.data[:3]

        return r, g, b
    
    def screen_width(self):
        return self.root.get_geometry().width

    def screen_height(self):
        return self.root.get_geometry().height