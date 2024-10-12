.PHONY: help clean lint build publish

.DEFAULT: help

export PYTHONPATH = $PYTHONPATH:$(shell pwd)

help:
	@echo "\nUsage:"
	@echo "make <command>"
	@echo "\nExample:"
	@echo "make run param='list'"
	@echo "\nAvailable Commands:"
	@echo "- run\t\t\t Run project"
	@echo "- clean\t\t\t Run clean project"
	@echo "- lint\t\t\t Check python code against some of the style conventions in PEP 8"
	@echo "- build\t\t\t Builds a package, as a tarball and a wheel by default."
	@echo "- publish\t\t Publishes a package to a remote repository.\n\n"

run:
	@echo "\n> Running project";\
	python beegen/ $(param);\

clean:
	@echo "\n> Cleaning project\n";\
	find . -name '*.pyc' -exec rm --force {} +;\
	find . -name '*.pyo' -exec rm --force {} +;\
	find . | grep -E "__pycache__|.pyc" | xargs rm -rf;\
	rm -rf dist/;\

lint:
	@echo "\n> Check python code PEP 8\n";\
	black beegen/ & flake8 beegen/ & bandit -r -lll beegen/;\

build:
	@echo "\nBuilds a package, as a tarball and a wheel by default.\n";\
	poetry build

publish:
	@echo "\nRun publish package in pypi\n";\
	poetry run twine upload dist/*