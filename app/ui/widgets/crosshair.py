from gi.repository import Gtk

class Crosshair(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.color = (1, 0, 0, 0.8)  # default κόκκινο
        self.set_draw_func(self.draw)

    def set_color_rgba(self, r, g, b, alpha=0.8):
        self.color = (r/255, g/255, b/255, alpha)
        self.queue_draw()  # repaint

    def draw(self, area, cr, width, height):
        cx = width / 2
        cy = height / 2
        cr.set_line_width(1)
        cr.set_source_rgba(*self.color)

        # οριζόντια
        cr.move_to(cx - 10, cy)
        cr.line_to(cx + 10, cy)
        # κάθετη
        cr.move_to(cx, cy - 10)
        cr.line_to(cx, cy + 10)
        cr.stroke()
