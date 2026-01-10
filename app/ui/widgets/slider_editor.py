from gi.repository import Gtk, GObject
from enum import Enum


class SliderEditorFormat(Enum):
    INTEGER = "integer"
    HEX = "hex"

class SliderEditor(Gtk.Box):
    __gsignals__ = {
            "value_changed": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        }
    
    def __init__(self, 
                 title: str="", 
                 value: int=0, 
                 min_value: int = 0, 
                 max_value: int=0, 
                 format: SliderEditorFormat = SliderEditorFormat.INTEGER,
                 label_size:int = 20):
        
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        self.title = title
        self.min_value = min_value
        self.max_value = max_value
        self.format = format
        self.value = value
        self.label_size = label_size
        
        self.build_ui()


    def build_ui(self):

        # label
        label = Gtk.Label(label=self.title)
        label.set_size_request(self.label_size, -1)
        label.set_xalign(0.0)
        self.append(label)

        self.adjustment = Gtk.Adjustment.new(
            value=self.value,
            lower=self.min_value,
            upper=self.max_value,
            step_increment=1,
            page_increment=10,
            page_size=0
        )
        self.adjustment.connect("value-changed", self.on_slider_input_changed)

        # slider input
        self.slider_input = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.adjustment)
        self.slider_input.set_draw_value(False)
        self.slider_input.set_hexpand(True)
        self.append(self.slider_input)

        # text input
        self.text_input = Gtk.Entry()
        self.text_input.set_width_chars(4)
        self.text_input.set_max_width_chars(5)
        self.text_input.set_alignment(1.0)
        self.text_input.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.text_input.set_text(self.format_text(self.value))
        self.text_input.connect("activate", self.on_text_input_set_value)
        focus_controller = Gtk.EventControllerFocus()
        focus_controller.connect("leave", self.on_text_input_set_value)
        self.text_input.add_controller(focus_controller)
        self.append(self.text_input)


    # format the text input value based on the format type of the widget
    def format_text(self, value: int) -> str:
        if self.format == SliderEditorFormat.INTEGER:
            return str(value)
        elif self.format == SliderEditorFormat.HEX:
            return f"{value:02X}"
        else:
            return str(value)


    # actions to do when the value of the slider changed
    def on_slider_input_changed(self, adjustment):
        value = int(adjustment.get_value())
        if value == self.value:
            return

        self.value = value
        self.text_input.set_text(self.format_text(value))
        self.emit("value_changed", value)


    # get the integer value of a text based on the format type of the widget
    def numeric_text(self, text:str) -> int:
        if self.format == SliderEditorFormat.INTEGER:

            # if the input from user is not a number then return the stored value of the widget
            clean_number = ''.join(c for c in text if c.isdigit())
            if not clean_number:
                return None
            else:
                return int(clean_number)

        elif self.format == SliderEditorFormat.HEX:
            try:
                value = int(text, 16)
                return value
            except ValueError:
                return None
        else:
            return None
        

    # actions to do when the value of the text input changed
    def on_text_input_set_value(self, widget):
        text = self.text_input.get_text()
        numeric_value = self.numeric_text(text)

        # if the text is not corresponding to a number then restore the original value and exit
        if numeric_value == None:
            self.text_input.set_text(self.format_text(self.value))
            return

        # if the new value is not in the specified limits then restore the original value and exit
        if numeric_value < self.min_value or numeric_value > self.max_value:
            self.text_input.set_text(self.format_text(self.value))
            return
        
        # if the value is same as the original then display the original value and exit
        if numeric_value == self.value:
            self.text_input.set_text(self.format_text(self.value))
            return
        
        # if the value is valid then update everything
        self.adjustment.set_value(numeric_value)
        self.text_input.set_text(self.format_text(numeric_value))




    
