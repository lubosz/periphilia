#!/usr/bin/python3

from IPython import embed
from gi.repository import Gst, Gtk, GObject, GdkPixbuf, Gd
from gi.repository.Gtk import Stack, StackTransitionType
from gi.repository import Gtk, Gio, GLib, Gdk, Notify
import src.view as Views
from src.toolbar import Toolbar, ToolbarState
from gettext import gettext as _
from src.plugin import Plugins

class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="Earthquake")
        self.setup_view()
        """
        self.button = Gtk.Button(label="Play")
        self.button.connect("clicked", self.on_button_clicked)

        """

    def setup_view(self):
        self._box = Gtk.VBox()
        self.toolbar = Toolbar()
        self.toolbar2 = Toolbar()
        self.views = []
        self._stack = Stack(
            transition_type=StackTransitionType.CROSSFADE,
            transition_duration=100,
            visible=True)
            
        self.set_titlebar(self.toolbar.header_bar)
        self._box.pack_start(self.toolbar.searchbar, False, False, 0)
            
        self._box.pack_start(self._stack, True, True, 0)
        self.add(self._box)
        count = 1
        
        plugins = Plugins()
        
        #self.views.append(Views.ElementView(self.toolbar, _("All"), all_plugins))
        self.views.append(Views.ElementView(self.toolbar, _("Bins"), plugins.get("bins")))
        self.views.append(Views.ElementView(self.toolbar, _("Decoders"), plugins.get("decoders")))
        self.views.append(Views.ElementView(self.toolbar, _("Encoders"), plugins.get("encoders")))
        self.views.append(Views.ElementView(self.toolbar, _("Muxers"), plugins.get("muxers")))
        self.views.append(Views.ElementView(self.toolbar, _("Demuxers"), plugins.get("demuxers")))
        self.views.append(Views.ElementView(self.toolbar, _("Sources"), plugins.get("sources")))
        self.views.append(Views.ElementView(self.toolbar, _("Sinks"), plugins.get("sinks")))
        self.views.append(Views.ElementView(self.toolbar, _("Parsers"), plugins.get("parsers")))
        
        self.views.append(Views.ElementView(self.toolbar, _("frei0r"), plugins.get("frei0r")))
        self.views.append(Views.ElementView(self.toolbar, _("libav"), plugins.get("libav")))
        self.views.append(Views.ElementView(self.toolbar, _("OpenGL"), plugins.get("opengl")))
        self.views.append(Views.ElementView(self.toolbar, _("effectv"), plugins.get("effectv")))
        self.views.append(Views.ElementView(self.toolbar, _("Misc"), plugins.get("misc")))
        for i in self.views:
            self._stack.add_titled(i, i.title, i.title)

        self.toolbar.set_stack(self._stack)
        self.toolbar.searchbar.show()
        
        self.toolbar._search_button.connect('toggled', self._on_search_toggled)

        self.toolbar.set_state(ToolbarState.ALBUMS)
        self.toolbar.header_bar.show()

        self._box.show()
        self.show()

        
    def init_gst(self):
        Gst.init(None)
        self.pipeline = Gst.Pipeline.new("pipeline")
        videotestsrc = Gst.ElementFactory.make("videotestsrc", "src")
        glimagesink = Gst.ElementFactory.make("autovideosink", "sink")

        self.pipeline.add(videotestsrc)
        self.pipeline.add(glimagesink)

        Gst.Element.link(videotestsrc, glimagesink)

    def on_button_clicked(self, widget):
        if self.playing:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.playing = False
            self.button.set_label("Play")
        else:
            self.pipeline.set_state(Gst.State.PLAYING)
            self.playing = True
            self.button.set_label("Pause")
    def _toggle_view(self, btn, i):
        self._stack.set_visible_child(self.views[i])

    def _on_search_toggled(self, button, data=None):
        self._show_searchbar(button.get_active())

    def _show_searchbar(self, show):
        self.toolbar.searchbar.set_reveal_child(show)
        self.toolbar._search_button.set_active(show)
        if show:
            self.toolbar.searchbar._search_entry.grab_focus()
        else:
            self.toolbar.searchbar._search_entry.set_text('')
