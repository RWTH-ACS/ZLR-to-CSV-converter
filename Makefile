SHELL := /bin/bash

init:
	python3 ./createEnv.py
	source vEnv/bin/activate && \
	pip3 install wheel && \
	pip3 install setuptools && \
	pip install --upgrade pip && \
	pip install --upgrade packaging==21.3 && \
	pip install -r requirements.txt
update:
	source vEnv/bin/activate && \
	pip install -r requirements.txt
clean:
	rm -R -f vEnv
	rm -R -f __pycache__
	rm -R -f *.egg-info
devel: init
	source vEnv/bin/activate && \
	pip install --no-deps -e ../dmu && \
	pip install --no-deps -e ../FiLiP