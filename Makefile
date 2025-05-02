.PHONY: clean

run: clean
	src/ui/UI.py

clean:
	black $$(find -name *.py)