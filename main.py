import uvicorn
from app.api import app
from prometheus_fastapi_instrumentator import Instrumentator


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

    
Instrumentator().instrument(app).expose(app)
