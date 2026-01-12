from gi.repository import Gtk, Gdk, GObject 

class PickButton(Gtk.Frame): 
    __gsignals__ = { 
        "start": (GObject.SignalFlags.RUN_FIRST, None, ()), 
        "stop": (GObject.SignalFlags.RUN_FIRST, None, ()), 
        "aborted": (GObject.SignalFlags.RUN_FIRST, None, ()), 
    } 
    
    def __init__(self): 
        super().__init__() 
        
        self.picking = False
        self.set_hexpand(False)
        self.set_halign(Gtk.Align.START)
        self.set_cursor(Gdk.Cursor.new_from_name("pointer"))
      
        self.add_css_class("icon-button") 

        # icon
        icon = Gtk.Image.new_from_file("app/resources/icons/dropper.png")
        icon.set_tooltip_text("prick for screen")
        self.set_child(icon)

         # Legacy controller για όλα τα mouse events
        controller = Gtk.EventControllerLegacy()
        controller.connect("event", self.on_event)
        self.add_controller(controller)


    def on_event(self, controller, event)-> None:
        event = controller.get_current_event()
        if event is None:
            return

        event_type = event.get_event_type()
        
        if event_type == Gdk.EventType.BUTTON_PRESS:
            button_num = event.get_button()

            if button_num == 1 and not self.picking:    # left click
                self.picking = True
                self.emit("start")
            elif self.picking and button_num != 1:      # if not left click then abort
                self.picking = False
                self.emit("aborted")

        elif event_type == Gdk.EventType.BUTTON_RELEASE:
            button_num = event.get_button()

            if self.picking:
                if button_num == 1:
                    self.picking = False
                    self.emit("stop")
                else:
                    self.picking = False
                    self.emit("aborted")

