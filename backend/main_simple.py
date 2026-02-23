from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI(
    title="Water-Borne Disease Prediction API",
    description="API for predicting water-borne diseases based on water quality and symptoms",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Water-Borne Disease Prediction API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)