FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libreoffice \
    gcc \
    libpq-dev \
    vim \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN echo "alias ls='ls --color=auto'" >> ~/.bashrc

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"]
