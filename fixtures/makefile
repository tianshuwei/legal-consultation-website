DUMP = python ../manage.py dumpdata
OPTIONS = --indent=2

all: clean
	@echo "Dumping accounts..."
	# warning: dumping auth directly will cause conflictions with content type
	$(DUMP) auth.User accounts $(OPTIONS) > "./accounts.json"
	@echo "Dumping blogs..."
	$(DUMP) blogs $(OPTIONS) > "./blogs.json"
	@echo "Dumping products & orders..."
	$(DUMP) products $(OPTIONS) > "./products.json"
	@echo "Dumping questions..."
	$(DUMP) questions $(OPTIONS) > "./questions.json"
	@echo "Dumping smartcontract..."
	$(DUMP) smartcontract $(OPTIONS) > "./smartcontract.json"
	@echo "Done."

clean:
	@echo "Cleaning..."
	rm -f ./*.json
