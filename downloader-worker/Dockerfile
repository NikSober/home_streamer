FROM python:3.9-slim
USER root
RUN dnf -y install \
    epel-release && \
    dnf -y install \
    python3-devel \
    boost-devel \
    openssl-devel \
    libtorrent-rasterbar \
    libtorrent-rasterbar-devel \
    gcc \
    && dnf clean all

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000
EXPOSE 6881

CMD ["python", "app.py"]