# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = /usr/bin/env python3 -msphinx
SPHINXPROJ    = remake
SOURCEDIR     = .
BUILDDIR      = _build

all: html

# Put it first so that "make" without argument is like "make help".
#: Show help on useful targets
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

#: Make docs used in readthedocs.io
readthedocs:
	$(MAKE) html

html:
	$(MAKE) -C .. $@

%: html
	$(MAKE) -C .. $@

.PHONY: help Makefile all

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
