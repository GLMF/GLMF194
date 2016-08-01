PACKAGE=cb-login
DESTDIR=/usr/share/locale

PO:=$(wildcard *.po)
MO:=$(PO:.po=.mo)
LANG:=$(PO:.po=)

all: $(MO)
install: all
	@for f in $(LANG); do \
		if [ ! -f $(DESTDIR)/$$f/LC_MESSAGES/$(PACKAGE).mo ]; then \
		 echo cp -v $$f.mo $(DESTDIR)/$$f/LC_MESSAGES/$(PACKAGE).mo; \
		fi \
	done
uninstall:
	@for f in $(LANG); do \
		if [ -f $(DESTDIR)/$$f/LC_MESSAGES/$(PACKAGE).mo ]; then \
		 echo rm -vf $(DESTDIR)/$$f/LC_MESSAGES/$(PACKAGE).mo; \
		fi \
	done

%.mo: %.po
	msgfmt $< -o $@

clean:
	@rm -vf $(MO)
