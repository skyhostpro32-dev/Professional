FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (Streamlit default)
EXPOSE 8501

# Start app using dynamic PORT (IMPORTANT for Render)
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
