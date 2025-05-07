.PHONY: clean

run:
	src/driver.py

debug:
	python3 src/debug.py
	
clean:
	black $$(find -name *.py)

mock: 
	python3 src/driver.py --db_path=database/mock_company.db

test:
	python3 src/unit_tests.py