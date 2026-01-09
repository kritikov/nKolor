# app/utils/color_utils.py

from typing import Tuple
import colorsys

class Color:
    def __init__(self, r: int = 255, g: int = 255, b: int = 255):
        self.r = r
        self.g = g
        self.b = b

    # -------------------------------
    # Properties
    # -------------------------------
    @property
    def rgb(self) -> Tuple[int, int, int]:
        return f"rgb({self.r}, {self.g}, {self.b})"

    @property
    def rgb_values(self) -> Tuple[int, int, int]:
        return self.r, self.g, self.b

    @property
    def hex(self) -> str:
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    @hex.setter
    def hex(self, value: str):
        value = value.lstrip("#")
        if len(value) != 6:
            raise ValueError(f"Invalid hex: {value}")
        self.r, self.g, self.b = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

    @property
    def hsv(self) -> str:
        r_n, g_n, b_n = self.r / 255, self.g / 255, self.b / 255
        h, s, v = colorsys.rgb_to_hsv(r_n, g_n, b_n)

        h_deg = int(h * 360)
        s_pct = int(s * 100)
        v_pct = int(v * 100)

        return f"hsv({h_deg}, {s_pct}%, {v_pct}%)"

    @property
    def hsv_values(self) -> Tuple[float, float, float]:
        r_n, g_n, b_n = self.r / 255, self.g / 255, self.b / 255
        return colorsys.rgb_to_hsv(r_n, g_n, b_n)

    @hsv_values.setter
    def hsv_values(self, value: Tuple[float, float, float]):
        r_n, g_n, b_n = colorsys.hsv_to_rgb(*value)
        self.r, self.g, self.b = int(r_n*255), int(g_n*255), int(b_n*255)

    @property
    def hsl(self) -> str:
        r_n, g_n, b_n = self.r / 255, self.g / 255, self.b / 255
        h, l, s = colorsys.rgb_to_hls(r_n, g_n, b_n)
        
        h_deg = int(h * 360)
        s_pct = int(s * 100)
        l_pct = int(l * 100)

        return f"hsl({h_deg}, {s_pct}%, {l_pct}%)"

    @property
    def hsl_values(self) -> Tuple[float, float, float]:
        r_n, g_n, b_n = self.r / 255, self.g / 255, self.b / 255
        h, l, s = colorsys.rgb_to_hls(r_n, g_n, b_n)

        h_deg = int(h * 360)
        s_pct = int(s * 100)
        l_pct = int(l * 100)

        return h_deg, s_pct, l_pct

    @hsl_values.setter
    def hsl_values(self, value: Tuple[float, float, float]):
        h_deg, s_pct, l_pct = value

        # πίσω σε 0.0–1.0
        h = (h_deg % 360) / 360.0
        s = max(0.0, min(s_pct / 100.0, 1.0))
        l = max(0.0, min(l_pct / 100.0, 1.0))

        r_n, g_n, b_n = colorsys.hls_to_rgb(h, l, s)

        self.r = int(round(r_n * 255))
        self.g = int(round(g_n * 255))
        self.b = int(round(b_n * 255))


    # -------------------------------
    # Helpers
    # -------------------------------
    def complementary(self) -> "Color":
        return Color(255 - self.r, 255 - self.g, 255 - self.b)

    def brightness(self) -> float:
        """0..1"""
        return (0.299*self.r + 0.587*self.g + 0.114*self.b) / 255

    # get similar colors
    def get_variants(self) -> Tuple["Color", "Color", "Color", "Color"]:
        # RGB 0–255 → 0–1
        r, g, b = self.r / 255, self.g / 255, self.b / 255

        # RGB → HLS (note: colorsys uses HLS, όχι HSL)
        h, l, s = colorsys.rgb_to_hls(r, g, b)

        def clamp(v, min_v=0.0, max_v=1.0):
            return max(min_v, min(max_v, v))

        def to_color(h, l, s):
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return Color(
                int(r * 255),
                int(g * 255),
                int(b * 255),
            )

        # 🔧 Tuned deltas (δοκιμασμένα για UI)
        LIGHT_DELTA = 0.15
        SAT_DELTA = 0.25

        lighter = to_color(h, clamp(l + LIGHT_DELTA), s )
        darker = to_color(h, clamp(l - LIGHT_DELTA), s )
        less_saturated = to_color(h, l, clamp(s - SAT_DELTA))
        more_saturated = to_color(h, l, clamp(s + SAT_DELTA))
        
        return lighter, darker, less_saturated, more_saturated
    

    # -------------------------------
    # Representation
    # -------------------------------
    def __repr__(self):
        return f"Color(RGB=({self.r}, {self.g}, {self.b}), HEX={self.hex})"

    def copy(self) -> "Color":
        return Color(self.r, self.g, self.b)

    

