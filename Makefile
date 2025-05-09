.PHONY: clean, run, mock, new

run:
	src/driver.py

mock:
	src/init_demo.py
	src/driver.py --db_path=database/mock_company.db

new:
	src/init_blank_with_admin.py
	src/driver.py

test:
	python3 src/unit_tests.py

clean:
	rm database/*.db
	rm storage/schedule.JSON
	black $$(find -name *.py)