export $(cat .env | xargs) && env
python -m pipenv run python main.py
