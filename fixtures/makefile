DUMP = python ../manage.py dumpdata
OPTIONS = --indent=2

all: clean
	@echo "Dumping accounts..."
	$(DUMP) auth.User accounts $(OPTIONS) > "./accounts.json"
	@echo "Dumping blogs..."
	$(DUMP) blogs $(OPTIONS) > "./blogs.json"
	@echo "Dumping products & orders..."
	$(DUMP) products $(OPTIONS) > "./products.json"

clean:
	@echo "Cleaning..."
	rm -f ./*.json
