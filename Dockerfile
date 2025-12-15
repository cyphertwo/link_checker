# 1️⃣ Image de base Python slim
FROM python:3.11-slim

# 2️⃣ Installer dépendances système pour Chrome et Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    gnupg \
    curl \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ Installer Google Chrome stable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Définir le répertoire de travail
WORKDIR /app

# 5️⃣ Copier les fichiers du projet
COPY . .

# 6️⃣ Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# 7️⃣ Exposer le port Flask
EXPOSE 5000

# 8️⃣ Commande par défaut pour lancer Flask
CMD ["python", "app.py"]
