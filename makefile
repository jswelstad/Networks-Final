PROGRAM = python3
MAIN = client.py

run:
	$(PROGRAM) $(MAIN)

.PHONY: clean
clean:
	@rm -rf __pycache__
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@echo "All Clean"
