.PHONY: install html check weekly-html intake-html vacc-html dict weekly-dict intake-dict vacc-dict

DEF_DIR=surveys

WEEKLY_DIR=$(DEF_DIR)/weekly
INTAKE_DIR=$(DEF_DIR)/intake
WEEKLY_DEF=$(WEEKLY_DIR)/survey.json
INTAKE_DEF=$(INTAKE_DIR)/survey.json
VACC_DIR=$(DEF_DIR)/vaccination
VACC_DEF=$(VACC_DIR)/survey.json

help:
	@echo "Managing survey standards"
	@echo "   install: install tools (needs python3)"
	@echo "   html:    build html files from survey description json (weekly-html,intake-html,vacc-html) "
	@echo "   dict:    build json dictionary file (weekly-dict,intake-dict,vacc-dict)
	@echo "   check:   check json validity against json schema"

install:
	python3 -m venv venv

vacc-html:
	tools/build-html.sh $(VACC_DEF) $(VACC_DIR)/survey.html

weekly-html:
	tools/build-html.sh $(WEEKLY_DEF) $(WEEKLY_DIR)/survey.html
	
intake-html:
	tools/build-html.sh $(INTAKE_DEF) $(INTAKE_DIR)/survey.html

html: weekly-html intake-html vacc-html

intake-dict:
	./cli survey:dictionary intake --output=$(INTAKE_DIR)/dictionary.json

weekly-dict:
	./cli survey:dictionary weekly --output=$(WEEKLY_DIR)/dictionary.json

vacc-dict:
	./cli survey:dictionary vaccination --output=$(VACC_DIR)/dictionary.json

dict: intake-dict weekly-dict vacc-dict

docx:
	./cli survey:show --template="survey_clean.html" $(WEEKLY_DEF) --output="weekly_clean.html"
	pandoc --from="html" --to="docx" -o "weekly.docx" weekly_clean.html

check:
	./cli survey:validate $(WEEKLY_DEF)
	./cli survey:check weekly
	./cli survey:validate $(INTAKE_DEF)
	./cli survey:check intake
	./cli survey:validate $(VACC_DEF)
	./cli survey:check vaccination
	
