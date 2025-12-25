# pylint: disable=missing-module-docstring

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from workout_api.routers import athlete, workout


app = FastAPI(title="Workout API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(athlete.router)
app.include_router(workout.router)




@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Workout API is running"}
