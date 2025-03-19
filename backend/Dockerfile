# Use Python Image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the contents of the backend folder into /app
COPY . /app/

# Install dependencies from requirements.txt (recommended)
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask Port
EXPOSE 5001

# Set environment variables (Optional but good practice)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
ENV FLASK_DEBUG=1

# Run Flask using flask run
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001", "--debug"]