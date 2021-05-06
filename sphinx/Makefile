# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -E
SPHINXBUILD   = ../.venv/bin/sphinx-build
SPHINXAPIDOC   = ../.venv/bin/sphinx-apidoc
SOURCEDIR     = source
BUILDDIR      = ./_build/
APIDOCDIR     = "$(SOURCEDIR)/_apidoc"
PACKAGESDIR   = ../packages/akit
PUBLISHDIR = ../docs/html

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

apidoc:
	@$(SPHINXAPIDOC) --output-dir "$(APIDOCDIR)" "$(PACKAGESDIR)" 

apidoc-full:
	@$(SPHINXAPIDOC) -f --output-dir "$(APIDOCDIR)" "$(PACKAGESDIR)" 

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -d "$(SOURCEDIR)/_doctrees"
	@cp -a "$(BUILDDIR)/html/." "$(PUBLISHDIR)/"
