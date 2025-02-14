Below is a comprehensive guide that walks you through setting up, running, and managing your Flask, PostgreSQL, and data ingestion environment. This guide covers both a local and a Dockerized environment, explains common commands, and includes a shortcuts section for quick access.

Comprehensive Setup and Management Guide

This guide will help you:
	•	Set up and run your Flask app with SQLAlchemy and Flask‑Migrate.
	•	Manage your PostgreSQL database.
	•	Ingest data from an external source (using Ticketmaster’s API as an example).
	•	Understand the differences between a local environment and a Docker environment.
	•	Use key Docker commands for interacting with your containers.

1. Environment Overview

Local Environment
	•	Flask Application: Runs on your local machine, using your installed Python environment.
	•	Local PostgreSQL: Requires you to install and configure PostgreSQL on your machine.
	•	Pros: Easier for quick development and debugging.
	•	Cons: You must manually manage dependencies and configuration; differences between your local setup and production might occur.

Dockerized Environment
	•	Flask Application Container: Your Flask app runs inside a Docker container.
	•	PostgreSQL Container: Your PostgreSQL database runs in its own container.
	•	Configuration: Environment variables are managed in your docker-compose.yml file or .env file, ensuring consistency.
	•	Pros: Reproducible, isolated environment that mirrors production.
	•	Cons: Requires learning Docker commands and concepts.

2. Project Structure

A typical project structure might look like this:

las_vegas_ai/
├── backend/                     # Flask API & backend code
│   ├── app.py                   # Main Flask application with models, routes, etc.
│   ├── ingest_data.py           # Data ingestion script to fetch external data
│   ├── requirements.txt         # Python dependencies
│   ├── migrations/              # Flask-Migrate migration files (auto-generated)
│   └── .env                   # Environment variables (optional, usually at project root)
├── frontend/                    # React frontend (if applicable)
├── docker-compose.yml           # Docker Compose configuration for containers
└── README.md                    # Project documentation

3. Local Setup (Without Docker)

3.1. Install Dependencies
	1.	Set Up Virtual Environment:

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


	2.	Install Dependencies:

pip install -r backend/requirements.txt

Your requirements.txt might include:

flask
flask_sqlalchemy
flask_migrate
flask_cors
flask-login
flask-bcrypt
psycopg2
pyotp
qrcode[pil]
requests
python-dotenv



3.2. Configure Environment Variables

Create a .env file (preferably in the project root) with:

DATABASE_URL=postgresql://myuser:mypassword@localhost/las_vegas_db
TICKETMASTER_API_KEY=your_actual_api_key_here

3.3. Set Up Local PostgreSQL

Ensure PostgreSQL is installed and running locally. Then, create the necessary role and database:

psql -U postgres

At the PostgreSQL prompt, run:

CREATE ROLE myuser WITH LOGIN PASSWORD 'mypassword';
ALTER ROLE myuser CREATEDB;
CREATE DATABASE las_vegas_db OWNER myuser;
\q

3.4. Run Migrations

From the backend folder:

cd backend
export FLASK_APP=app.py
flask db init             # Only needed the first time
flask db migrate -m "Initial migration: create tables"
flask db upgrade

3.5. Run the Ingestion Script

python ingest_data.py

3.6. Inspect the Database

Use psql to connect and inspect:

psql -U myuser -d las_vegas_db

Then use commands like:
	•	\d – to list tables.
	•	\d users – to view the structure of the users table.
	•	SELECT * FROM recommendations; – to query data.

4. Dockerized Setup

4.1. docker-compose.yml Overview

Your docker-compose.yml file should define two main services: one for PostgreSQL and one for your Flask app. For example:

# docker-compose.yml
version: "3.9"

services:
  db:
    image: postgres:latest
    container_name: las_vegas_db
    restart: always
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: las_vegas_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  flask_app:
    build: .
    container_name: las_vegas_flask
    restart: always
    depends_on:
      - db
    ports:
      - "5000:5000"
    environment:
      FLASK_APP: "app.py"
      FLASK_RUN_HOST: "0.0.0.0"
      FLASK_RUN_PORT: "5000"
      FLASK_DEBUG: "1"
      DATABASE_URL: "postgresql://myuser:mypassword@db/las_vegas_db"
      TICKETMASTER_API_KEY: "your_actual_api_key_here"
    volumes:
      - ./backend:/app
    command: ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]

volumes:
  pgdata:
    external: true

4.2. Dockerfile

Your Dockerfile should install all required dependencies and copy your backend code to the container:

# Dockerfile (placed at project root)
FROM python:3.9

WORKDIR /app

COPY backend /app/

RUN pip install --no-cache-dir flask flask_sqlalchemy flask_migrate flask-login flask-bcrypt psycopg2 pyotp qrcode[pil] requests python-dotenv flask-cors

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]

4.3. Build and Run Containers

From the project root, run:

docker compose down --remove-orphans
docker compose build
docker compose up -d

4.4. Running Migrations Inside Docker
	1.	Exec into the Flask Container:

docker exec -it las_vegas_flask bash


	2.	Run Migration Commands:
Inside the container:

flask --app app.py db migrate -m "Extend Recommendation model with description, event_date, venue"
flask --app app.py db upgrade



4.5. Run the Ingestion Script Inside Docker

Inside the Flask container:

python ingest_data.py

4.6. Inspect the Database in Docker

To connect to the PostgreSQL container, run:

docker exec -it las_vegas_db psql -U myuser -d las_vegas_db

Then use:
	•	\d – to list tables.
	•	\d recommendations – to inspect the recommendations table.
	•	SELECT * FROM recommendations; – to view the data.

5. Shortcuts and Common Commands

Docker Commands
	•	Start Containers in Detached Mode:

docker compose up -d


	•	Stop and Remove Containers:

docker compose down --remove-orphans


	•	Rebuild Containers:

docker compose build


	•	View Running Containers:

docker ps


	•	Exec into a Container:
	•	Flask app:

docker exec -it las_vegas_flask bash


	•	PostgreSQL:

docker exec -it las_vegas_db psql -U myuser -d las_vegas_db



Flask & Migrate Commands (Inside backend or Container)
	•	Set FLASK_APP Environment Variable:

export FLASK_APP=app.py

Or use:

flask --app app.py <command>


	•	Initialize Migrations (first time only):

flask --app app.py db init


	•	Generate a New Migration:

flask --app app.py db migrate -m "Your migration message"


	•	Apply Migrations:

flask --app app.py db upgrade



Database Inspection via psql
	•	List All Tables:

\d


	•	View Table Schema (e.g., users):

\d users


	•	Query Data:

SELECT * FROM recommendations;

Summary
	•	Local vs Docker Environment:
	•	Local: You run commands directly on your machine. Ensure you have PostgreSQL installed and configured.
	•	Docker: Everything runs in containers. Use docker compose commands, and environment variables are set in your Docker Compose file or a .env file in the project root.
	•	Key Setup Steps:
	1.	Install dependencies and set up environment variables.
	2.	Configure PostgreSQL (locally or via Docker).
	3.	Run migrations to set up your schema.
	4.	Run the data ingestion script to populate your database.
	5.	Create and use API endpoints to serve your data.
	6.	Integrate with your frontend.
	7.	Schedule updates and add robust error handling.
	•	Shortcuts:
See the “Shortcuts and Common Commands” section for frequently used commands.

This guide should serve as a detailed roadmap for setting up and managing your environment, both locally and in Docker. If you have any more questions or need further clarification on any step, feel free to ask!