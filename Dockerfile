FROM python:3.12-slim

# Set environment variables
ENV PYTHONBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE="false"

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set the working directory
WORKDIR /app

# Copy the dependencies file to the working directory
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry install --no-interaction --no-ansi --without dev

# Copy the project files to the working directory
COPY . /app/

# Make the entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Run the application
ENTRYPOINT [ "./docker-entrypoint.sh" ]
