
dist-clean:
	rm -fr dist

dist-build:
	python3 setup.py sdist bdist_wheel 

dist-deploy:
	python3 -m twine upload --repository pypi dist/*

