install:
	pip install -r requirements.txt

format:
	black .
	isort .

run:
	streamlit run main_page.py

build:
	docker-compose build

up:
	echo "Running streamlit on http://localhost:8501"
	docker-compose up -d

down:
	echo "Stopping streamlit on http://localhost:8501"
	docker-compose down

remove:
	echo "Removing streamlit images and containers"
	docker-compose down
	docker-compose down --rmi all --volumes --remove-orphans
	docker-compose rm -v -s -f
