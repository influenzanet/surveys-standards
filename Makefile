.PHONY: install html check weekly-html

DEF_DIR=surveys

WEEKLY_DIR=$(DEF_DIR)/weekly
INTAKE_DIR=$(DEF_DIR)/intake

install:
	python3 -m venv venv

weekly-html:
	./cli survey:show $(WEEKLY_DIR)/survey.json --output=$(WEEKLY_DIR)/survey.html
	
intake-html:
	./cli survey:show $(INTAKE_DIR)/survey.json --output=$(INTAKE_DIR)/survey.html

html: weekly-html intake-html
    
	
check:
	./cli survey:validate $(WEEKLY_DIR)/survey.json
	./cli survey:validate $(INTAKE_DIR)/survey.json