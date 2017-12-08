.PHONY: all sdist wheel push clean

all:

sdist:
	@python setup.py sdist

wheel:
	@python setup.py bdist_wheel

push:
	@twine upload dist/*

clean:
	@rm -rfv build/ dist/ src/*.egg-info src/rephacheck/*.pyc src/rephacheck/__pycache__
