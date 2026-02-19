from importlib.resources import files

class Resources:

    @classmethod
    def icon(cls, filename: str) -> str:
        return str(files("nkolor.resources.icons").joinpath(filename))

    @classmethod
    def css(cls, filename: str) -> str:
        return str(files("nkolor.resources.css").joinpath(filename))
