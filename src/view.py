from gi.repository import Gtk, GObject, Gd, GdkPixbuf, GLib
from gettext import gettext as _

from gi.repository.Gtk import Stack, StackTransitionType

class ViewContainer(Stack):
    def __init__(self, title, header_bar):
        Stack.__init__(self,
                       transition_type=StackTransitionType.CROSSFADE)
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

        self.view = Gd.MainView(
            shadow_type=Gtk.ShadowType.NONE
        )
        self.title = title
        self.header_bar = header_bar
        
        self.view.set_model(self.model)
        self.filter = self.model.filter_new(None)
        self.view.set_model(self.filter)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self.view, True, True, 0)
        self.grid.add(box)
        self.add(self.grid)

        self.view.connect('item-activated', self.on_item_activated)

        self.show_all()


class ElementView(ViewContainer):
    def __init__(self, header_bar, title, plugins):
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
        ViewContainer.__init__(self, title, header_bar)
        self.view.set_view_type(Gd.MainViewType.ICON)
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gstreamer/Gamepads/ElementWidget.ui')
        self.add(builder.get_object('ElementWidget'))
        self.plugins = plugins
        self.populate()

    def populate(self):
        for plugin in self.plugins:
            self.add_item(plugin.name, plugin.category)

    def add_item(self, name, cat):
        pb = GdkPixbuf.Pixbuf.new_from_file("data/seal.png")

        _iter = self.model.append(None)
        self.model.set(_iter,
                        [0, 1, 2, 3, 4, 5, 7, 8, 9, 10],
                        ["theitem", '', name,
                         cat, pb, None,
                         -1, "seal", False, False])

    def on_item_activated(self, widget, id, path):
        print("activated")
       
class ElementStackView (ViewContainer):
    def __init__(self, header_bar, title, plugins):
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
        ViewContainer.__init__(self, title, header_bar)
        
        self.elementStack = Stack(
            transition_type=StackTransitionType.CROSSFADE,
        )

        self.plugins = plugins
        self.subcats = {}
        self.populate()
        
        self.create_and_show(Gtk.TreePath.new_from_string ("0"))
        
        self.view.set_view_type(Gd.MainViewType.LIST)
        self.view.set_hexpand(False)

        
        #self.view.get_style_context().add_class('artist-panel')
        self.view.get_generic_view().get_selection().set_mode(
            Gtk.SelectionMode.SINGLE)
        self.grid.attach(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL),
                          1, 0, 1, 1)
        self.grid.attach(self.elementStack, 2, 0, 2, 2)

        self.view.get_generic_view().get_style_context().\
            add_class('artist-panel-dark')

        self.show_all()

    def populate(self):
        for cat in self.plugins:
            self.add_item(cat)

    def create_and_show(self, path):
        new_elementWidget = Gtk.Frame(
            shadow_type=Gtk.ShadowType.NONE,
            hexpand=True
        )

        child_path = self.filter.convert_path_to_child_path(path)
        
        subcatname = "subcat%s" % child_path
        
        if not subcatname in self.subcats:
            self.elementStack.add_named(new_elementWidget, subcatname)
            _iter = self.model.get_iter(child_path)
            self._last_selection = _iter
            category = self.model.get_value(_iter, 2)
            
            print("Adding %s: %s" % (subcatname, category))
            elementView = ElementView(None, None, self.plugins[category])
            
            new_elementWidget.add(elementView)
            self.subcats[subcatname] = new_elementWidget 
        
        self.subcats[subcatname].show()
        self.elementStack.set_visible_child_name(subcatname)

    def on_item_activated(self, widget, item_id, path):
        self.create_and_show(path)

    def add_item(self, name):
        _iter = self.model.insert_with_valuesv(-1, [2], [name])
