from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import os

BIN_ID = os.getenv("JSONBIN_BIN_ID")
SUMMARY_BIN_ID = os.getenv("JSONBIN_SUMMARY_ID")
MASTER_KEY = os.getenv("JSONBIN_MASTER_KEY")

JSONBIN_HEADERS = {
    "X-Master-Key": MASTER_KEY,
    "Content-Type": "application/json"
}

fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@fastapi_app.get("/stats")
def get_stats():
    try:
        group_resp = requests.get(
            f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest",
            headers={"X-Master-Key": MASTER_KEY}
        )
        group_data_count = group_resp.json()
        record = group_data_count.get("record", {}).get("data", {})

        valid_groups = {
            k: v for k, v in record.items()
            if isinstance(v, dict) and "wallets" in v
        }

        groups_api = len(valid_groups)
        wallets_api = sum(len(g.get("wallets", {})) for g in valid_groups.values())

        summary_resp = requests.get(
            f"https://api.jsonbin.io/v3/b/{SUMMARY_BIN_ID}/latest",
            headers={"X-Master-Key": MASTER_KEY}
        )
        summary_data = summary_resp.json()
        transfer_record = summary_data.get("record", {}).get("data", {})

        transfers_api = sum(
            1
            for group in transfer_record.values()
            if isinstance(group, dict)
            for event in group.get("events", [])
            if isinstance(event.get("timestamp"), (int, float))
        )

        return {
            "groups_count": groups_api,
            "wallets_count": wallets_api,
            "transfers_count": transfers_api
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"error": "Internal Server Error"}


def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run_fastapi()
