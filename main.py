from fastapi import FastAPI, HTTPException
from letterboxdpy.user import User

# Crear la aplicación FastAPI con metadatos básicos
app = FastAPI(
    title="Letterboxd API",
    description="API para obtener películas de usuarios de Letterboxd",
    version="1.0.0"
)

# Lista de usuarios de Letterboxd que se consultarán por defecto
USUARIOS = [
    "elceto",
    "marcosdra",
    "emanueljurado",
    "difi109",
    "rafacarp"
]


@app.get("/")
def root():
    # Ruta raíz de la API para verificar el estado del servicio
    return {"status": "ok"}


@app.get("/films")
def get_films():
    # Devuelve las películas de todos los usuarios configurados
    rows = []

    try:
        for username in USUARIOS:
            # Consultar películas para cada usuario de la lista
            user = User(username)
            data = user.get_films()

            for _, film in data["movies"].items():
                rows.append({
                    "usuario": username,
                    "id": film.get("id"),
                    "titulo": film.get("name"),
                    "anio": film.get("year"),
                    "rating": film.get("rating"),
                })

        # Retornar total de resultados y lista de películas
        return {
            "total": len(rows),
            "films": rows
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/films/{username}")
def get_user_films(username: str):
    # Devuelve las películas de un usuario específico por nombre de usuario
    try:
        user = User(username)
        data = user.get_films()

        films = []

        for _, film in data["movies"].items():
            films.append({
                "id": film.get("id"),
                "titulo": film.get("name"),
                "anio": film.get("year"),
                "rating": film.get("rating"),
            })

        # Responder con el usuario consultado, total de películas y detalles
        return {
            "usuario": username,
            "total": len(films),
            "films": films
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )