
dist-clean:
	rm -fr dist

dist-build:
	poetry build 

dist-publish:
	poetry publish
