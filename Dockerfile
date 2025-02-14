# Use Python Image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the entire app folder
COPY app /app/

# Install dependencies
RUN pip install --no-cache-dir flask flask-login flask-bcrypt psycopg2 pyotp qrcode[pil]

# Expose Flask Port
EXPOSE 5000

# Set environment variables (Optional but good practice)
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=1

# Run Flask using flask run instead of python
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]