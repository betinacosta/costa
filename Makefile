setup:
	pipenv --three
	pipenv install --dev
	pipenv shell

test:
	pytest -v --disable-warnings
	pytest --cov=app tests/