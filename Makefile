.PHONY: help clean lint

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
	@echo "- lint\t\t\t Check python code against some of the style conventions in PEP 8\n\n"

run:
	@echo "\n> Running project";\
	python beegen/ $(param);\

clean:
	@echo "\n> Cleaning project\n";\
	find . -name '*.pyc' -exec rm --force {} +;\
	find . -name '*.pyo' -exec rm --force {} +;\
	find . | grep -E "__pycache__|.pyc" | xargs rm -rf;\
	rm -f logs/grace_service.log;\

lint:
	@echo "\n> Check python code PEP 8\n";\
	black beegen/ & flake8 beegen/ & bandit -r -lll beegen/;\