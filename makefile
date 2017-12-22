.PHONY: all build sdist wheel push clean

all: build

build:
	@make sdist
	@make wheel

sdist:
	@python3 setup.py sdist

wheel:
	@python3 setup.py bdist_wheel

push:
	@twine upload dist/*

clean:
	@rm -rfv build/ dist/ src/*.egg-info src/rephacheck/*.pyc src/rephacheck/__pycache__
