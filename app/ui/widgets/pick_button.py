from gi.repository import Gtk, Gdk, GObject 

class PickButton(Gtk.Frame): 
    __gsignals__ = { 
        "pressed": (GObject.SignalFlags.RUN_FIRST, None, ()), 
        "released": (GObject.SignalFlags.RUN_FIRST, None, ()), 
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
        
        # όλα τα buttons 
        self.gesture.connect("pressed", self._on_pressed) 
        self.gesture.connect("released", self._on_released) 
        self.gesture.connect("stopped", self._on_stopped) 
        self.add_controller(self.gesture) 
        

    def _cancel(self):

        print("_cancel")

        self._picking = False
        self.emit("aborted")

      

    def _on_pressed(self, gesture, n_press, x, y):

        print("_on_pressed")

        button = gesture.get_current_button()
        if button == Gdk.BUTTON_PRIMARY:
            gesture.set_state(Gtk.EventSequenceState.CLAIMED)
            self._picking = True
            self.emit("pressed")
        else:
            # οποιοδήποτε άλλο button = ακύρωση
            if self._picking:
                self._cancel()

        
    def _on_released(self, gesture, n_press, x, y):
        print("_on_released")

        if not self._picking:
            return

        button = gesture.get_current_button()
        if button == Gdk.BUTTON_PRIMARY:
            self._picking = False
            self.emit("released")
            self.emit("color-selected")
        else:
            # δεξί click ή άλλο κουμπί ακυρώνει
            self._picking = False
            self._cancel()


    def _on_stopped(self, *args):
        ...

    # set the text of the button 
    def set_text(self, text: str): 
        self.label.set_text(text)