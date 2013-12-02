#!/usr/bin/python3

from IPython import embed
from gi.repository import Gst, Gtk, GObject, GdkPixbuf, Gd
import subprocess
from gi.repository.Gtk import Stack, StackTransitionType
from gi.repository import Gtk, Gio, GLib, Gdk, Notify
import src.view as Views
from src.toolbar import Toolbar, ToolbarState
from gettext import gettext as _

def commandToLines(command):
    output = subprocess.check_output(command).decode("utf-8")
    lines = output.split("\n")
    return lines

def read_plugins():
    Gst.init(None)

    rank = Gst.Rank.NONE

    muxers = Gst.ElementFactory.list_get_elements(
        Gst.ELEMENT_FACTORY_TYPE_MUXER, rank)
    encoders = Gst.ElementFactory.list_get_elements(
        Gst.ELEMENT_FACTORY_TYPE_VIDEO_ENCODER, rank)
    sources = Gst.ElementFactory.list_get_elements(
        Gst.ELEMENT_FACTORY_TYPE_SRC, rank)

    for muxer in sources:
        plugin = muxer.get_plugin()
        #print(plugin.get_source(), plugin.get_name(), "\t", plugin.get_description(), plugin.get_path_string())

    pluginLines = commandToLines("gst-inspect-1.0")

    plugins = {}

    for plugin in pluginLines:
        pluginSplit = plugin.split(":")
        if len(pluginSplit) == 3:
            cat = pluginSplit[0].strip()
            name = pluginSplit[1].strip()
            desc = pluginSplit[2].strip()

            try:
                plugins[cat]
            except KeyError:
                plugins[cat] = {}
            plugins[cat][name] = desc

    for cat in plugins:
        print (cat, "(%d)" % len(plugins[cat]))
        for name in plugins[cat]:
            print("\t", name)

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
        self.views.append(Views.ElementView(self.toolbar, _("All")))
        self.views.append(Views.ElementView(self.toolbar, _("Decoders")))
        self.views.append(Views.ElementView(self.toolbar, _("Encoders")))
        self.views.append(Views.ElementView(self.toolbar, _("Muxers")))
        self.views.append(Views.ElementView(self.toolbar, _("Demuxers")))
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
