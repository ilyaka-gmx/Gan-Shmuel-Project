FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    docker.io \
    docker-compose \
    git \
    curl \
    htop \
    util-linux \ 
    && rm -rf /var/lib/apt/lists/*

# Install ttyd for web terminal
RUN curl -L https://github.com/tsl0922/ttyd/releases/download/1.7.3/ttyd.x86_64 -o /usr/local/bin/ttyd && \
    chmod +x /usr/local/bin/ttyd

# Install LazyDocker and check its version
# RUN curl -L https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | sh && lazydocker --version

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY webhook_server.py .
COPY ci_script.sh .

# Create necessary directories
RUN mkdir -p /app/logs /app/data

# Make script executable
RUN chmod +x ci_script.sh

# Add monitoring module files
COPY monitoring/ /app/monitoring/

CMD ["python3", "webhook_server.py"]

