setup:
	pipenv --three
	pipenv install --dev
	pipenv shell

test:
	coverage run --source tests -m py.test
	coverage report