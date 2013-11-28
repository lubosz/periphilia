resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --sourcedir=$(builddir) --generate-dependencies $(srcdir)/earthquake.gresource.xml) 
earthquake.gresource: earthquake.gresource.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) $<

resourcedir = $(pkgdatadir)
resource_DATA = earthquake.gresource


EXTRA_DIST = \
	$(resource_files) \
	earthquake.gresource.xml \
	$(NULL)

CLEANFILES = \
	earthquake.gresource \
	$(NULL)

-include $(top_srcdir)/git.mk
