from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.index import router as main_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    print("Backend Server Is Up and Running")
    uvicorn.run(app, host="0.0.0.0", port=3002)