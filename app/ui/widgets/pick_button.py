from gi.repository import Gtk, Gdk, GObject 

class PickButton(Gtk.Frame): 
    __gsignals__ = { 
        "start": (GObject.SignalFlags.RUN_FIRST, None, ()), 
        "stop": (GObject.SignalFlags.RUN_FIRST, None, ()), 
        "aborted": (GObject.SignalFlags.RUN_FIRST, None, ()), 
        "color-selected": (GObject.SignalFlags.RUN_FIRST, None, ()), 
    } 
    
    def __init__(self): 
        super().__init__() 
        
        self._picking = False

        # self.set_size_request(100, 30) 
        self.add_css_class("pick-button") 
        self.label = Gtk.Label(label="Pick") 
        self.set_child(self.label) 
        
        # GestureClick for events 
        self.gesture = Gtk.GestureClick() 
        self.gesture.set_button(0) 
        
         # Legacy controller για όλα τα mouse events
        controller = Gtk.EventControllerLegacy()
        controller.connect("event", self.on_event)
        self.add_controller(controller)


    def on_event(self, controller, event):
        event = controller.get_current_event()
        event_type = event.get_event_type()
        
        if event_type == Gdk.EventType.BUTTON_PRESS:
            button_num = event.get_button()
            if button_num == 1 and self._picking == False:     # left click
                self._picking = True
                self.emit("start")
        elif event_type == Gdk.EventType.BUTTON_RELEASE:
            button_num = event.get_button()

            if self._picking == True:
                if button_num == 1:
                    self._picking = False
                    self.emit("stop")
                    self.emit("color-selected")
                else:
                    self.emit("aborted")
                    self._picking = False

    # set the text of the button 
    def set_text(self, text: str): 
        self.label.set_text(text)