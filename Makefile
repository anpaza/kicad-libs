.PHONY: all install showrules

# A newline
define NL


endef

LIBS=Capacitors_Alu_SMD Connectors_JST Inductors_SMD Crystals
KICAD.LIBS=/usr/share/kicad
CWD=$(shell pwd)

all:
	@echo "Run 'sudo make install' to make symlinks in $(KICAD.LIBS)"
	@echo "to libraries in this directory"

install: \
	$(addprefix $(KICAD.LIBS)/modules/,$(addsuffix .pretty,$(LIBS))) \
	$(addprefix $(KICAD.LIBS)/modules/packages3d/,$(addsuffix .3dshapes,$(LIBS)))

define MKLINKRULES
$(KICAD.LIBS)/modules/$1.pretty: $(CWD)/$1/$1.pretty
	@if [ -d "$$@" ] ; then \
		echo "$$@ is a dir! Making individual links"; \
		for x in $$</*.kicad_mod ; do \
			test -f "$$$$x" || continue ; \
			y=`basename "$$$$x"` ; \
			test -L "$$@/$$$$y" && continue ; \
			echo "  Creating link $$@/$$$$y" ; \
			ln -s "$$$$x" "$$@/$$$$y" ; \
		done ; \
	else \
		echo "Creating link $$@" ; \
		ln -s $$< $$@ ; \
	fi

$(KICAD.LIBS)/modules/packages3d/$1.3dshapes: $(CWD)/$1/$1.3dshapes
	@if [ -d "$$@" ] ; then \
		echo "$$@ is a dir! Making individual links"; \
		for x in $$</*.wrl ; do \
			test -f "$$$$x" || continue ; \
			y=`basename "$$$$x"` ; \
			test -L "$$@/$$$$y" && continue ; \
			echo "  Creating link $$@/$$$$y" ; \
			ln -s "$$$$x" "$$@/$$$$y" ; \
		done ; \
	else \
		echo "Creating link $$@" ; \
		ln -s $$< $$@ ; \
	fi

endef

$(eval $(foreach _,$(LIBS),$(call MKLINKRULES,$_)))

showrules:
	@echo -e '$(subst $(NL),\n,$(foreach _,$(LIBS),$(call MKLINKRULES,$_)))'
