# Dockerfile

# 1. Použijeme oficiální odlehčený Python image
FROM python:3.12-slim

# 2. Nastavíme pracovní adresář uvnitř kontejneru
WORKDIR /code

# 3. Zkopírujeme soubor se závislostmi
COPY ./requirements.txt .

# 4. Nainstalujeme závislosti
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Zkopírujeme zbytek aplikace do kontejneru
COPY . .

RUN chmod +x /code/entrypoint.sh