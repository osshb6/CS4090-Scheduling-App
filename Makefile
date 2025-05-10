.PHONY: clean, run, mock, new

run:
	python3 src/driver.py

mock:
	python3 src/driver.py --db_path=database/mock_company.db

new:
	python3 src/init_blank_with_admin.py
	python3 src/driver.py

test:
	python3 src/unit_tests.py

clean:
	-rm database/*.db
	-rm storage/schedule.JSON
	cd src; black $$(find -name '*.py')