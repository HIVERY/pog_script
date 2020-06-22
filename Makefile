VENV_NAME?=env
PIP=${VENV_NAME}/bin/pip3
UNAME := $(shell uname -s)

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: requirements.txt
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PIP} install -e . 