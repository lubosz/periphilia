resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --sourcedir=$(builddir) --generate-dependencies $(srcdir)/gnome-gamepads.gresource.xml) 
gnome-gamepads.gresource: gnome-gamepads.gresource.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) $<

resourcedir = $(pkgdatadir)
resource_DATA = gnome-gamepads.gresource

appsdir = $(datadir)/applications
apps_DATA = gnome-gamepads.desktop

@INTLTOOL_DESKTOP_RULE@

appdatadir = $(datadir)/appdata
appdata_DATA = $(appdata_in_files:.xml.in=.xml)
appdata_in_files = gnome-gamepads.appdata.xml.in

@INTLTOOL_XML_RULE@

gsettings_SCHEMAS = org.gnome.Gamepads.gschema.xml

# For uninstalled use
gschemas.compiled: $(gsettings_SCHEMAS) Makefile
	$(AM_V_GEN) $(GLIB_COMPILE_SCHEMAS) $(builddir)

@GSETTINGS_RULES@

EXTRA_DIST = \
	$(resource_files) \
	gnome-gamepads.appdata.xml.in \
	gnome-gamepads.desktop.in \
	gnome-gamepads.gresource.xml \
  org.gnome.Gamepads.gschema.xml \
	$(NULL)

CLEANFILES = \
	gnome-gamepads.gresource \
	gnome-gamepads.appdata.xml \
	$(apps_DATA) \
	*.valid \
	gschemas.compiled \
	$(NULL)

all-local: gschemas.compiled

-include $(top_srcdir)/git.mk
