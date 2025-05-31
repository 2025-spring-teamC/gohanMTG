FROM python:3.12

ARG UID=1000
ARG GID=1000

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ../requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Node.jsとnpmのインストールと必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
  gcc \
  curl \
  && curl -sL https://deb.nodesource.com/setup_20.x | bash - \
  && apt-get install -y nodejs \
  && rm -rf /var/lib/apt/lists/*

# Tailwind CSSの依存関係をインストール
COPY ../package.json ../package-lock.json /code/
RUN npm install

COPY . /code

RUN groupadd -g $GID mygroup && useradd -m -u $UID -g $GID myuser
USER myuser