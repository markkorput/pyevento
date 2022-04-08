RUN = poetry run
PATHS = evento tests examples

# Code style
.PHONY: format
format:
	${RUN} isort ${PATHS}
	${RUN} black ${PATHS}

.PHONY: format-check
format-check:
	${RUN} isort --check-only ${PATHS}
	${RUN} black --check ${PATHS}

.PHONY: lint
lint:
	${RUN} flake8 ${PATHS}

.PHONY: tc # alias for typecheck
tc: typecheck

.PHONY: typecheck
typecheck:
	${RUN} mypy ${PATHS}

.PHONY: stale
stale:
	${RUN} vulture --min-confidence 100 ${PATHS}

.PHONY w:
w: watch

# Testing
.PHONY: watch
watch: clean/tests
	${RUN} ptw -n --runner "pytest --testmon ${scope}"

.PHONY: watch/focus
watch/focus:
	${RUN} ptw -n --runner "pytest --testmon -m focus ${scope}"

.PHONY: f # alias for watch/focus
f: watch/focus

.PHONY: t # alias for test
t: test

.PHONY: test
test:
	${RUN} pytest ${scope}

.PHONY: test/focus
test/focus:
	${RUN} pytest -m focus ${scope}

.PHONY: v # alias for validate
v: validate

.PHONY: vv
vv: format lint typecheck stale

.PHONY: validate
validate: vv test


# Maintenance
.PHONY: clean
clean: clean/builds clean/cache clean/tests clean/files

.PHONY: clean/files
clean/files:
	rm -fr tmp/files
	rm -fr tmp/emails

.PHONY: clean/cache
clean/cache:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean/builds
clean/builds:
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean/tests
clean/tests:
	rm -fr coverage/
	rm -fr .testmondata
	rm -fr .pytest_cache
	rm -fr .mypy_cache
