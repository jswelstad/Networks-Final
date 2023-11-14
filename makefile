PROGRAM = python3
CLIENT = client.py
SERVER = server.py

client:
	$(PROGRAM) $(CLIENT)

server:
	$(PROGRAM) $(SERVER)

.PHONY: clean
clean:
	@rm -rf __pycache__
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@echo "All Clean"
