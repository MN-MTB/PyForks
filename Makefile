ifeq ($(OS), Windows_NT)
	RM = rmdir /s /q
	MV = powershell -c move -Force
else
	ifeq ($(shell uname), Linux)
		RM = rm -rf
		MV = mv
	endif
endif

clean:
	$(RM) ".cookie" "build" "dist" "PyForks.egg-info" "PyForks/__pycache__" "PyForks/test" "PyForks/_test/__pycache__" ".pytest_cache"

build:
	pip3 install wheel twine
	python setup.py sdist bdist_wheel

publish: build
	twine upload dist/*

docs:
	pdoc --html --template-dir ./doc/templates/light_theme/ -o ./doc/ --force PyForks
	$(MV) ./doc/PyForks/* ./doc/
	$(RM) "./doc/PyForks"

test: clean
	flake8 --extend-ignore E501 --exclude "PyForks/_test" PyForks
	pytest