SHELL := /bin/bash

init:
	python3 ./createEnv.py
	source vEnv/bin/activate && \
	pip3 install wheel && \
	pip3 install setuptools && \
	pip install --upgrade pip && \
	pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ . 
update:
	source vEnv/bin/activate && \
	pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --upgrade .
clean:
	rm -R -f vEnv
	rm -R -f __pycache__
	rm -R -f *.egg-info