FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install UV: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

# Copy the dependency files to the working directory
COPY pyproject.toml uv.lock ./

# Install any needed packages specified in uv.lock
RUN uv export --locked --group crawler --group storage --group api --no-install-project -o /usr/src/app/requirements.txt \
    && uv pip sync --system /usr/src/app/requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 8000 for the API
EXPOSE 8000
