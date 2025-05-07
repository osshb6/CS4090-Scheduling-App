.PHONY: clean

run: clean
	src/driver.py

debug: clean
	python3 src/debug.py
clean:
	black $$(find -name *.py)