from fastapi import FastAPI
from .app.database import engine, Base
from .app.routes import router

app = FastAPI(
    title="API de Automação de Pesquisas Jurídicas",
    description="Backend para gerenciamento de lotes e automação de pesquisas em tribunais."
)

Base.metadata.create_all(bind=engine)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)