.PHONY: clean

run: clean
	src/driver.py

clean:
	black $$(find -name *.py)