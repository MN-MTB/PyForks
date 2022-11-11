clean:
	rm -rf bin dist build .cookie PyForks.egg-info PyForks/__pycache__ PyForks/test PyForks/_test/__pycache__ .pytest_cache

build: clean
	pip3 install wheel twine
	python setup.py sdist bdist_wheel

publish: build
	twine upload dist/*

docs:
	pdoc --html --template-dir ./doc/templates/light_theme/ -o ./doc/ --force PyForks
	mv ./doc/PyForks/* ./doc
	rm -rf ./doc/PyForks

test: clean
	pytest