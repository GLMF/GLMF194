PACKAGE=cb-login
VERSION=1.0
COPYRIGHT=IUT de Beziers
EMAIL=cb@iutbeziers.fr

CC:=gcc
BASENAME:=$(shell basename $(PWD))
CFLAGS_GTK:=$(shell pkg-config --cflags gtk+-3.0)
LDFLAGS_GTK:=$(shell pkg-config --libs gtk+-3.0)

CSRCS:=$(wildcard *.c)
CEXES:=$(CSRCS:.c=)

CFLAGS:=-g -O2 -Wall $(CFLAGS_GTK)
LDFLAGS:=$(LIB) $(LDFLAGS_GTK)

all: $(CEXES)
po: $(PACKAGE).pot
	@make -C po
$(PACKAGE).pot: gtk3-06-internationalisation.c
	xgettext --sort-output --no-wrap --escape --keyword=_ \
		--copyright-holder="$(COPYRIGHT)" \
		--msgid-bugs-address="$(EMAIL)" \
		--package-name="$(PACKAGE)" \
		--package-version="$(VERSION)" \
		-o $@ $<
tar: clean
	@cd ..;tar cvJf $(BASENAME).tar.xz --exclude=.directory --exclude=*.odt --exclude=*.png $(BASENAME)

.c:
	$(CC) $< $(CFLAGS) -o $@ $(LDFLAGS)

clean_bak:
	@rm -vf *~ *.bak *.org
clean_data: clean_bak
	@rm -vf *.dat *.stackdump core
clean: clean_data
	@rm -vf $(CEXES) $(PACKAGE).pot
	@make -C po clean
