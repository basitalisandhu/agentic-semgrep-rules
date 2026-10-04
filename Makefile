# agentic-semgrep-rules
#
# make test      run the fixture suite (every rule has ruleid / ok annotations)
# make validate  check rule syntax and metadata
# make smoke     scan the fixtures and any extra paths in SMOKE_PATHS and report counts
# make sarif     produce results.sarif for the current directory
# make bundle    regenerate the single-file agentic-semgrep-rules.yaml

SEMGREP ?= semgrep
SEMGREP_FLAGS ?= --metrics=off --disable-version-check
SMOKE_PATHS ?=

.PHONY: test validate smoke sarif audit-fixtures lint-metadata bundle bundle-check help

help:
	@grep -E '^# make' Makefile | sed 's/^# //'

test:
	$(SEMGREP) --test --config rules tests $(SEMGREP_FLAGS)
	python3 scripts/check_fixtures.py

validate: lint-metadata bundle-check
	$(SEMGREP) --validate --config rules $(SEMGREP_FLAGS)

lint-metadata:
	python3 scripts/check_metadata.py rules

audit-fixtures:
	python3 scripts/check_fixtures.py
	python3 scripts/check_fixtures.py --config agentic-semgrep-rules.yaml

bundle:
	python3 scripts/bundle.py

bundle-check:
	python3 scripts/bundle.py --check

smoke:
	python3 scripts/check_fixtures.py --report
ifneq ($(strip $(SMOKE_PATHS)),)
	$(SEMGREP) --config rules $(SEMGREP_FLAGS) --error $(SMOKE_PATHS)
endif

sarif:
	$(SEMGREP) --config rules $(SEMGREP_FLAGS) --sarif --output results.sarif .
