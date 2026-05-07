.PHONY: all
all: activate generate_cprd make_cprd_db generate_hes make_hes_db

activate:
	@if ! [ -d env ]; then \
		python -m venv env; \
		source env/bin/activate; \
		pip install -r requirements.txt; \
	else \
		source env/bin/activate; \
	fi

generate_cprd: activate
	time python scripts/cprd/gen_data.py

make_cprd_db: activate generate_cprd
	time python scripts/cprd/make_db.py

generate_hes: activate data/cprd/raw/Patient.csv
	time python scripts/hes/gen_data.py

make_hes_db: activate generate_hes
	time python scripts/hes/make_db.py
