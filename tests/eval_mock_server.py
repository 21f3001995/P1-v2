# eval_mock_server.py
from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI(title="Mock Evaluation Server")

@app.post("/notify")
async def receive_evaluation(request: Request):
    data = await request.json()
    print("\n🧪 Evaluation mock received:")
    print(json.dumps(data, indent=2))
    return {"status": "ok", "message": "Received"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
