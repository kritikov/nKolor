from gi.repository import Gtk, GObject

class SliderEditor(Gtk.Box):
    __gsignals__ = {
            "value_changed": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        }
    
    def __init__(self, title: str="", value: int=0, min_value: int = 0, max_value: int=0):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        self.title = title
        self.min_value = min_value
        self.max_value = max_value

        self.updating_from_text = False  # flag για αποφυγή feedback
        self.adjustment = Gtk.Adjustment.new(
            value=value,
            lower=self.min_value,
            upper=self.max_value,
            step_increment=1,
            page_increment=10,
            page_size=0
        )
        self.value = int(self.adjustment.get_value())

        self.build_ui()

        # connect adjustment after UI built
        self.adjustment.connect("value-changed", self.on_slider_input_changed)


    def build_ui(self):
        label = Gtk.Label(label=self.title)
        label.set_size_request(20, -1)
        self.append(label)

        self.slider_input = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.adjustment)
        self.slider_input.set_draw_value(False)
        self.slider_input.set_hexpand(True)
        self.append(self.slider_input)

        self.text_input = Gtk.Entry()
        self.text_input.set_width_chars(4)
        self.text_input.set_max_width_chars(5)
        self.text_input.set_alignment(1.0)
        self.text_input.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.text_input.set_text(str(self.value))
        self.text_input.connect("activate", self.on_text_input_set_value)
        focus_controller = Gtk.EventControllerFocus()
        focus_controller.connect("leave", self.on_text_input_set_value)
        self.text_input.add_controller(focus_controller)
        self.append(self.text_input)


    # actions to do when the value of the slider changed
    def on_slider_input_changed(self, adjustment):
        if self.updating_from_text:
            return  # αποφυγή feedback loop

        value = int(adjustment.get_value())
        if value == self.value:
            return

        self.value = value
        Gtk.idle_add(self.text_input.set_text, str(value))
        self.emit("value_changed", value)

    # actions to do when the value of the text input changed
    def on_text_input_set_value(self, widget):
        text = self.text_input.get_text()
        clean_number = ''.join(c for c in text if c.isdigit())

        # if the input from user is not a number then restore the original value and exit
        if not clean_number:
            self.text_input.set_text(str(self.value))
            return

        # if the new value is not in the specified limits then restore the original value and exit
        value = int(clean_number)
        if value < self.min_value or value > self.max_value:
            self.text_input.set_text(str(self.value))
            return

        # if the value is same as the original then restore the original value and exit
        if value == self.value:
            self.text_input.set_text(str(self.value))
            return

        # flag to avoid loop from on_slider_input_changed
        self.updating_from_text = True
        self.adjustment.set_value(value)
        self.updating_from_text = False

        self.text_input.set_text(str(value))




    
