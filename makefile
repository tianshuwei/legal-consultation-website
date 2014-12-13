FIXTURES_PATH = ./fixtures

all: fixtures
	@true

fixtures: clean
	@echo "Dumping accounts..."
	python manage.py dumpdata auth.User accounts --indent=2 > "$(FIXTURES_PATH)/accounts.json"
	@echo "Dumping blogs..."
	python manage.py dumpdata blogs --indent=2 > "$(FIXTURES_PATH)/blogs.json"
	@echo "Dumping products & orders..."
	python manage.py dumpdata products --indent=2 > "$(FIXTURES_PATH)/products.json"

clean:
	@echo "Cleaning..."
	rm -f $(FIXTURES_PATH)/*.json
