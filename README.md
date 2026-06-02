# Generating synthetic CPRD and linked data

The code in this repository can be used to create low-fidelity synthetic data based on the Clinical Practice Research Datalink (CPRD) ARUM [data dictionary](https://www.cprd.com/sites/default/files/2024-08/CPRD%20Aurum%20Data%20Specification%20v3.5.pdf).

It also creates synthetic linked and small area data:

-  Hospital Episode Statistics (HES) data that is in the same format as the linked HES data provided by CPRD: [HES APC](https://www.cprd.com/sites/default/files/2026-02/HES_APC_Data_Dictionary_v2.9.pdf), [HES A&E](https://www.cprd.com/sites/default/files/2026-06/HES_AE_Documentation_v1.9.pdf), [HES OP](https://www.cprd.com/sites/default/files/2026-01/HES_OP_Documentation_v2.2.pdf)
-  [Small area level data](https://www.cprd.com/sites/default/files/2026-01/SmallAreaData_Patient_documentation_v3.5.pdf)

These synthetic datasets can be used for developing code for data extraction and cleaning prior to accessing CPRD. Each dataset has an associated `config.py`. In these files parameters such as the number of patients, practices and consultations to synthesise can be adjusted.

To run the code you will need python installed. The code was developed using python 3.11.8. All other dependencies can be found in `requirements.txt`. Bash commands to run the code are listed in `Makefile`. To generate both datasets, run `make all`.

