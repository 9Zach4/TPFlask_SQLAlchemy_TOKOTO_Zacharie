# liste des endpoint
* http://localhost:5000
  - utilisez postman pour tester les requêtes

* ### 1. Recherche de Chambres Disponibles

**Endpoint :** `/api/chambres/disponibles`
- il faut mettre un argument correspondant a vos date d'arrivée et de départ dans l'endpoint par example  ` api/rooms/available?arrival_date=2024-02-11&departure_date=2024-02-15 `
* ### 2. Création de Réservation
**Endpoint :** `/api/reservations`
- exemple de requête *POST* sur postman  `{
    "id_client": 1,
    "id_chambre": 1,
    "date_arrivee": "2024-06-15",
    "date_depart": "2024-08-27"
} `
