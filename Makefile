.PHONY: all
all: generate_cprd make_cprd_db generate_hes_apc make_hes_apc_db generate_hes_ae make_hes_ae_db generate_hes_op make_hes_op_db generate_small_area make_small_area_db make_unified_db

PYTHON = env/bin/python3

env:
	python3 -m venv env
	env/bin/pip install -r requirements.txt

generate_cprd: env
	$(PYTHON) scripts/cprd/gen_data.py

make_cprd_db: env generate_cprd
	$(PYTHON) scripts/cprd/make_db.py

generate_hes_apc: env data/cprd/raw/Patient.csv
	$(PYTHON) scripts/hes_apc/gen_data.py

make_hes_apc_db: env generate_hes_apc
	$(PYTHON) scripts/hes_apc/make_db.py

generate_hes_ae: env data/cprd/raw/Patient.csv
	$(PYTHON) scripts/hes_ae/gen_data.py

make_hes_ae_db: env generate_hes_ae
	$(PYTHON) scripts/hes_ae/make_db.py

generate_hes_op: env data/cprd/raw/Patient.csv
	$(PYTHON) scripts/hes_op/gen_data.py

make_hes_op_db: env generate_hes_op
	$(PYTHON) scripts/hes_op/make_db.py

generate_small_area: env data/cprd/raw/Patient.csv
	$(PYTHON) scripts/small_area/gen_data.py

make_small_area_db: env generate_small_area
	$(PYTHON) scripts/small_area/make_db.py

make_unified_db: env make_cprd_db make_hes_apc_db make_hes_ae_db make_hes_op_db make_small_area_db
	$(PYTHON) scripts/make_unified_db.py
