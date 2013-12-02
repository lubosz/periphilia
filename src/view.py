from gi.repository import Gtk, GObject, Gd, GdkPixbuf
from gettext import gettext as _

from gi.repository.Gtk import Stack, StackTransitionType

class ViewContainer(Stack):
    def __init__(self, title):
        Stack.__init__(self,
                       transition_type=StackTransitionType.CROSSFADE)
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

        self.model = Gtk.ListStore(
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GdkPixbuf.Pixbuf,
            GObject.TYPE_OBJECT,
            GObject.TYPE_BOOLEAN,
            GObject.TYPE_INT,
            GObject.TYPE_STRING,
            GObject.TYPE_BOOLEAN,
            GObject.TYPE_BOOLEAN
        )
        self.view = Gd.MainView(
            shadow_type=Gtk.ShadowType.NONE
        )
        self.title = title
        self.view.set_view_type(Gd.MainViewType.ICON)
        self.view.set_model(self.model)
        #self.filter = self.model.filter_new(None)
        #self.view.set_model(self.filter)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self.view, True, True, 0)
        self.grid.add(box)
        self.add(self.grid)

        #self.view.connect('item-activated', self.on_item_activated)

        self.show_all()

    def add_item(self, source, param, item):
        artist = "A GStreamer Element"
        title = "Cool Element"
        pb = GdkPixbuf.Pixbuf.new_from_file("data/seal.png")

        _iter = self.model.append(None)
        self.model.set(_iter,
                        [0, 1, 2, 3, 4, 5, 7, 8, 9, 10],
                        ["theitem", '', title,
                         artist, pb, None,
                         -1, "seal", False, False])

    def on_item_activated(self, widget, id, path):
        print("activated")


class ElementView(ViewContainer):
    def __init__(self):
        ViewContainer.__init__(self, _("Decoders"))
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gstreamer/Earthquake/ElementWidget.ui')
        self.add(builder.get_object('ElementWidget'))

        for i in range(0, 20):
            self.add_item(None, None, None)
