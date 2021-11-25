
dist-clean:
	rm -fr dist

dist-build:
	python3 -m build

dist-deploy:
	python3 -m twine upload --repository pypi dist/*

