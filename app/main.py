from fastapi import FastAPI
from app.database.db_config import init_db
from app.api.routes import intent_routes, response_routes

app = FastAPI(
    title="Customizable Intent Management System",
    description="API for managing intents and responses for different customers"
)

# Include routers
app.include_router(intent_routes.router, prefix="/api/v1", tags=["intents"])
app.include_router(response_routes.router, prefix="/api/v1", tags=["responses"])


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/")
async def root():
    return {"message": "Intent Management System API"}
