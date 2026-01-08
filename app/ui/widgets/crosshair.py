from gi.repository import Gtk

class Crosshair(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.light_color = (255, 255, 255, 1)  
        self.dark_color = (0, 0, 0, 1)  

        self.set_draw_func(self.draw)

    def draw(self, area, cr, width, height):
        cx = width / 2
        cy = height / 2
        size = 12
        internal_radious = 4

        # Draw a cross with an empty space in the center to view the pixel under of it.
        # The cross has two colors to be visible in all cases of brightness beneath.

        # horizontal
        cr.set_line_width(1)
        cr.set_source_rgba(*self.light_color)
        cr.move_to(cx - size, cy-2)
        cr.line_to(cx - internal_radious, cy-2)
        cr.move_to(cx + internal_radious, cy-2)
        cr.line_to(cx + size, cy-2)
        cr.stroke()

        cr.set_line_width(3)
        cr.set_source_rgba(*self.dark_color)
        cr.move_to(cx - size, cy)
        cr.line_to(cx - internal_radious, cy)
        cr.move_to(cx + internal_radious, cy)
        cr.line_to(cx + size, cy)
        cr.stroke()

        cr.set_line_width(1)
        cr.set_source_rgba(*self.light_color)
        cr.move_to(cx - size, cy+1)
        cr.line_to(cx - internal_radious, cy+1)
        cr.move_to(cx + internal_radious, cy+1)
        cr.line_to(cx + size, cy+1)
        cr.stroke()


        # vertical
        cr.set_line_width(1)
        cr.set_source_rgba(*self.light_color)
        cr.move_to(cx-2, cy - size)
        cr.line_to(cx-2, cy - internal_radious)
        cr.move_to(cx-2, cy + internal_radious)
        cr.line_to(cx-2, cy + size)
        cr.stroke()

        cr.set_line_width(3)
        cr.set_source_rgba(*self.dark_color)
        cr.move_to(cx, cy - size)
        cr.line_to(cx, cy - internal_radious)
        cr.move_to(cx, cy + internal_radious)
        cr.line_to(cx, cy + size)
        cr.stroke()

        cr.set_line_width(1)
        cr.set_source_rgba(*self.light_color)
        cr.move_to(cx+1, cy - size)
        cr.line_to(cx+1, cy - internal_radious)
        cr.move_to(cx+1, cy + internal_radious)
        cr.line_to(cx+1, cy + size)
        cr.stroke()

