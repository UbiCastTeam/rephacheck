.PHONY: all install build publish clean

all: build

install:
	poetry install

build:
	poetry build

publish:
	poetry publish

clean:
	rm -rfv .venv/ dist/ *.egg-info rephacheck/*.pyc rephacheck/__pycache__
