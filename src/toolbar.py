from gi.repository import Gtk, Gdk, GObject
from gi.repository.Gtk import StackSwitcher


class Toolbar(GObject.GObject):

    __gsignals__ = {
        'state-changed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    _selectionMode = False
    _maximized = False

    def __init__(self):
        GObject.GObject.__init__(self)
        self._stack_switcher = StackSwitcher(margin_top=2, margin_bottom=2)
        self._ui = Gtk.Builder()
        self._ui.add_from_resource('/org.gnome.Gamepads/headerbar.ui')
        self.header_bar = self._ui.get_object('header-bar')
        self._close_button = self._ui.get_object('close-button')
        self._close_button.connect('clicked', self._close_button_clicked)

    def _close_button_clicked(self, btn):
        if Gtk.get_minor_version() > 8:
            self._close_button.get_toplevel().close()
        else:
            self._close_button.get_toplevel().destroy()

