#!/usr/bin/python3

from IPython import embed
from gi.repository import Gst, Gtk, GObject, GdkPixbuf, Gd
from gi.repository import Gtk, Gio, GLib, Gdk, Notify

class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="Gamepads")
        self.setup_view()

    def setup_view(self):

        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        ps3_image = Gtk.Image()
        ps3_image.set_from_file("data/gamepads/PlayStation_3_gamepad.svg")
        stack.add_titled(ps3_image, "check", "PS3 Controller")

        xbox_image = Gtk.Image()
        xbox_image.set_from_file("data/gamepads/Xbox360_gamepad.svg")
        stack.add_titled(xbox_image, "label", "XBox Controller")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)
        self.show_all()
