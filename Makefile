.PHONY: clean

run: clean
	src/driver.py

clean:
	black $$(find -name *.py)

mock: 
	python src/driver.py --db_path=database/mock_company.db