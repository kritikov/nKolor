import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio

class AboutWindow(Gtk.ApplicationWindow):

    def __init__(self, app: Gtk.Application):
        super().__init__(title="about")
        self.set_resizable(False)
        self.set_default_size(450, -1)


        # Root container
        root_child = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        root_child.add_css_class("window-root-child")
        self.set_child(root_child)

        # App name and version
        app_name = Gtk.Label(label="nKolor")
        app_name.add_css_class("about-title")
        root_child.append(app_name)

        version = Gtk.Label(label="Version: 1.0.0")
        version.add_css_class("about-subtitle")
        root_child.append(version)

        author = Gtk.Label(label="© 2026 by Nick Kritikou")
        author.add_css_class("about-author")
        root_child.append(author)

        visit_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        root_child.append(visit_box)
        visit_label = Gtk.Label(label="visit me at:")
        visit_box.append(visit_label)
        nkode_link = Gtk.LinkButton.new_with_label(
            uri="https://nkode.gr",
            label="nkode.gr"
        )
        visit_box.append(nkode_link)
        visit_box.set_halign(Gtk.Align.CENTER)  


        # Short description
        description = Gtk.Label(label="A simple color picker for Linux using GTK4 and X11. The nKolor is open source under the GPL 3.0 License and you can find it at:")
        description.set_wrap(True)
        description.set_xalign(0.0)  
        root_child.append(description)


        # GitHub link
        github_link = Gtk.LinkButton.new_with_label(
            uri="https://github.com/kritikov/nKolor"
        )
        root_child.append(github_link)

        # more info
        more_info = Gtk.Label(label="You can find more informations for the nKolor at: ")
        more_info.set_wrap(True)
        more_info.set_xalign(0.0)       
        root_child.append(more_info)

        # project informations link
        github_link = Gtk.LinkButton.new_with_label(
            uri="https://nkode.gr/EN/articleView?id=277",
            label="nKolor informations"
        )
        root_child.append(github_link)

        # Close button
        close_btn = Gtk.Button(label="Close")
        close_btn.set_halign(Gtk.Align.CENTER)  
        close_btn.set_hexpand(False)
        close_btn.connect("clicked", lambda w: self.destroy())
        root_child.append(close_btn)


