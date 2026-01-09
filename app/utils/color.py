# app/utils/color_utils.py

from typing import Tuple
import colorsys

class Color:

    def __init__(self, r: int = 255, g: int = 255, b: int = 255):
        self.h, self.s, self.v = self.rgb_to_hsv(r, g, b)   # h, s, v in [0,1]


    # Equality check based on RGB
    def __eq__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return self.rgb == other.rgb
    
    # default presentation
    def __repr__(self):
        r, g, b = self.rgb
        return f"Color(RGB=({r}, {g}, {b}), HEX={self.hex_text})"

    # copy the color from the rgb values
    def copy(self) -> "Color":
        r, g, b = self.rgb
        return Color(r, g, b)


    # ------------------
    # properties
    # ------------------

    @property
    def hsv(self) -> Tuple[float, float, float]:
        return self.h, self.s, self.v
    
    @property
    def hsv_text(self) -> str:
        h_deg = int(self.h * 360)
        s_pct = int(self.s * 100)
        v_pct = int(self.v * 100)
        return f"hsv({h_deg}, {s_pct}%, {v_pct}%)"


    @property
    def rgb(self) -> Tuple[int, int, int]:
        r, g, b = self.hsv_to_rgb(self.h, self.s, self.v)
        return r, g, b

    @property
    def rgb_normalized(self) -> Tuple[int, int, int]:
        r, g, b = self.rgb
        return self.rgb_to_rgb_normalized(r, g, b)

    @property
    def rgb_text(self) -> Tuple[int, int, int]:
        r, g, b = self.rgb
        return f"rgb({r}, {g}, {b})"

    @rgb.setter
    def rgb(self, value: Tuple[int, int, int]):
        self.h, self.s, self.v = self.rgb_to_hsv(*value)


    @property
    def hex_text(self) -> str:
        r, g, b = self.rgb
        return f"#{r:02X}{g:02X}{b:02X}"

    # @hex.setter
    # def hex(self, value: str):
    #     """
    #     value: string όπως "#RRGGBB" ή "RRGGBB"
    #     """
    #     value = value.lstrip("#")
    #     r = int(value[0:2], 16)
    #     g = int(value[2:4], 16)
    #     b = int(value[4:6], 16)
    #     # ενημέρωση HSV source-of-truth
    #     self.h, self.s, self.v = self.rgb_to_hsv(r, g, b)

   
    @property
    def hsl(self) -> Tuple[float, float, float]:
        r, g, b = self.rgb
        return self.rgb_to_hsl(r, g, b)
    
    @property
    def hsl_text(self) -> str:
        h, s, l = self.hsl
        h_deg = int(h * 360)
        s_pct = int(s * 100)
        l_pct = int(l * 100)
        return f"hsl({h_deg}, {s_pct}%, {l_pct}%)"

    @property
    def hsl_for_ui(self) -> Tuple[int, int, int]:
        h, s, l = self.hsl
        h_deg = round(h * 360)
        s_pct = round(s * 100)
        l_pct = round(l * 100)
        return h_deg, s_pct, l_pct

    @hsl_for_ui.setter
    def hsl_for_ui(self, value: Tuple[float, float, float]):
        h_deg, s_pct, l_pct = value
        h = h_deg / 360
        s = s_pct / 100
        l = l_pct / 100
        r, g, b = self.hsl_to_rgb(h, s, l)
        self.rgb = r, g, b


    # ------------------
    # methods
    # ------------------

    # convert rgb values to hsv values
    def rgb_to_hsv(self, r: int, g: int, b: int) -> Tuple[float, float, float]:

        # 1. normalize RGB
        r_n, g_n, b_n = self.rgb_to_rgb_normalized(r, g, b)

        c_max = max(r_n, g_n, b_n)
        c_min = min(r_n, g_n, b_n)
        delta = c_max - c_min

        # 2. Hue
        if delta == 0:
            h = 0.0
        elif c_max == r_n:
            h = ((g_n - b_n) / delta) % 6
        elif c_max == g_n:
            h = ((b_n - r_n) / delta) + 2
        else:  # c_max == b_n
            h = ((r_n - g_n) / delta) + 4

        h /= 6.0  # normalize hue to 0–1

        # 3. Saturation
        s = 0.0 if c_max == 0 else delta / c_max

        # 4. Value
        v = c_max

        return h, s, v


    # convert rgb values to hsl values
    def rgb_to_hsl(self, r: int, g: int, b: int) -> Tuple[float, float, float]:
        r_n, g_n, b_n = self.rgb_to_rgb_normalized(r, g, b)

        c_max = max(r_n, g_n, b_n)
        c_min = min(r_n, g_n, b_n)
        delta = c_max - c_min

        # Lightness
        l = (c_max + c_min) / 2

        # Saturation
        if delta == 0:
            s = 0.0
        else:
            s = delta / (1 - abs(2*l - 1))

        # Hue
        if delta == 0:
            h = 0.0
        elif c_max == r_n:
            h = ((g_n - b_n) / delta) % 6
        elif c_max == g_n:
            h = ((b_n - r_n) / delta) + 2
        else:
            h = ((r_n - g_n) / delta) + 4

        h /= 6  # normalize 0–1

        return h, s, l


    # normalize rgb values
    def rgb_to_rgb_normalized(self, r: int, g: int, b: int) -> Tuple[int, int, int]:
        r_n = r / 255.0
        g_n = g / 255.0
        b_n = b / 255.0

        return r_n, g_n, b_n
    

    # convert hsv values to rgb values
    def hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        
        if s == 0.0:
            # γκρι / μαύρο / άσπρο
            r = g = b = int(round(v * 255))
            return r, g, b

        h = h * 6  # scale hue to 0–6
        i = int(h)  # sector 0–5
        f = h - i   # fractional part
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))

        if i == 0:
            r_n, g_n, b_n = v, t, p
        elif i == 1:
            r_n, g_n, b_n = q, v, p
        elif i == 2:
            r_n, g_n, b_n = p, v, t
        elif i == 3:
            r_n, g_n, b_n = p, q, v
        elif i == 4:
            r_n, g_n, b_n = t, p, v
        else:  # i == 5
            r_n, g_n, b_n = v, p, q

        r = int(round(r_n * 255))
        g = int(round(g_n * 255))
        b = int(round(b_n * 255))

        return r, g, b


    # convert hsv values to rgb values
    def hsl_to_rgb(self, h: float, s: float, l: float) -> Tuple[int, int, int]:
        if s == 0.0:
            # grayscale
            r = g = b = int(round(l * 255))
            return r, g, b

        def hue_to_rgb(p: float, q: float, t: float) -> float:
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q - p) * 6 * t
            if t < 1/2: return q
            if t < 2/3: return p + (q - p) * (2/3 - t) * 6
            return p

        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q

        r_n = hue_to_rgb(p, q, h + 1/3)
        g_n = hue_to_rgb(p, q, h)
        b_n = hue_to_rgb(p, q, h - 1/3)

        r = int(round(r_n * 255))
        g = int(round(g_n * 255))
        b = int(round(b_n * 255))

        return r, g, b


    # get similar colors
    def get_variants(self) -> Tuple["Color", "Color", "Color", "Color"]:
        h, s, v = self.hsv  # source-of-truth HSV

        LIGHT_DELTA = 0.15
        SAT_DELTA = 0.25

        # helper για clamp
        clamp = lambda x: max(0.0, min(1.0, x))

        variants = [
            Color(*self.hsv_to_rgb(h, clamp(s), clamp(v + LIGHT_DELTA))),  # lighter
            Color(*self.hsv_to_rgb(h, clamp(s), clamp(v - LIGHT_DELTA))),  # darker
            Color(*self.hsv_to_rgb(h, clamp(s - SAT_DELTA), clamp(v))),    # less saturated
            Color(*self.hsv_to_rgb(h, clamp(s + SAT_DELTA), clamp(v))),    # more saturated
        ]

        return tuple(variants)



    

    #@hex.setter
    # def hex(self, value: str):
    #     value = value.lstrip("#")
    #     if len(value) != 6:
    #         raise ValueError(f"Invalid hex: {value}")
    #     self.r, self.g, self.b = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))


    #@hsv_values.setter
    # def hsv_values(self, value: Tuple[float, float, float]):
    #     r_n, g_n, b_n = colorsys.hsv_to_rgb(*value)
    #     self.r, self.g, self.b = int(r_n*255), int(g_n*255), int(b_n*255)


    #@hsl_values.setter
    # def hsl_values(self, value: Tuple[float, float, float]):
    #     h_deg, s_pct, l_pct = value

    #     # πίσω σε 0.0–1.0
    #     h = (h_deg % 360) / 360.0
    #     s = max(0.0, min(s_pct / 100.0, 1.0))
    #     l = max(0.0, min(l_pct / 100.0, 1.0))

    #     r_n, g_n, b_n = colorsys.hls_to_rgb(h, l, s)

    #     self.r = int(round(r_n * 255))
    #     self.g = int(round(g_n * 255))
    #     self.b = int(round(b_n * 255))


    # -------------------------------
    # Helpers
    # -------------------------------
    # def complementary(self) -> "Color":
    #     return Color(255 - self.r, 255 - self.g, 255 - self.b)

    # def brightness(self) -> float:
    #     """0..1"""
    #     return (0.299*self.r + 0.587*self.g + 0.114*self.b) / 255


