import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)

# Test de logging dans votre application
@app.get("/")
def read_root():
    logging.info("Requête reçue sur l'endpoint racine")
    return {"Hello": "World"}
