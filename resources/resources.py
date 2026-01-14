import os

class Resources:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
    ICONS_DIR = os.path.join(RESOURCES_DIR, "icons")
    CSS_DIR = os.path.join(RESOURCES_DIR, "css")

    @classmethod
    def icon(self, filename: str) -> str:
        return os.path.join(self.ICONS_DIR, filename)

    @classmethod
    def css(self, filename: str) -> str:
        print(self.BASE_DIR)
        return os.path.join(self.CSS_DIR, filename)
