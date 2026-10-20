from fastapi import FastAPI

app = FastAPI(title="Safe Checkout Spike")


@app.get("/health")
def health():
    return {"status": "ok"}
    