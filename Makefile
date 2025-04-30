.PHONY: clean

run: clean
	src/UI.py

clean:
	black src/*.py