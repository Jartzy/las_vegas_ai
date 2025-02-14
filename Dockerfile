# Use Python Image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the entire backend folder into /app
COPY backend /app/

# Install dependencies (added flask-migrate)
RUN pip install --no-cache-dir flask flask_sqlalchemy flask-login flask-bcrypt psycopg2 pyotp qrcode[pil] requests python-dotenv flask-cors flask-migrate

# Expose Flask Port
EXPOSE 5000

# Set environment variables (Optional but good practice)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=1

# Run Flask using flask run
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]