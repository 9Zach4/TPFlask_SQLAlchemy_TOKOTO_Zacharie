FROM python:3.9

# Installation des dépendances
# COPY <Hote_chemin> <conteneur_chemin>
COPY requirements.txt  /app/requirements.txt
RUN pip install -r /app/requirements.txt
WORKDIR /app

COPY src /app
ENV FLASK_APP=/app/src/critique_film

# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]