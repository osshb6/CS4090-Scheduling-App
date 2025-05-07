.PHONY: clean

run: clean
	src/driver.py

debug: clean
	python3 src/debug.py
clean:
	black $$(find -name *.py)

mock: 
	python3 src/driver.py --db_path=database/mock_company.db