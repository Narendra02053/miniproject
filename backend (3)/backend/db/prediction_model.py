from datetime import datetime
from typing import List, Optional

from .connection import get_prediction_col


def _collection():
    return get_prediction_col()


def save_prediction(email: Optional[str], payload: dict, prediction: float) -> None:
    pred_col = _collection()
    if pred_col is None:
        return

    doc = {
        "email": email.lower() if email else None,
        "payload": payload,
        "prediction": prediction,
        "created_at": datetime.utcnow(),
    }
    pred_col.insert_one(doc)


def get_predictions(email: str, limit: int = 10) -> List[dict]:
    pred_col = _collection()
    if pred_col is None:
        return []

    cursor = (
        pred_col.find({"email": email.lower()})
        .sort("_id", -1)
        .limit(limit)
    )

    history = []
    for doc in cursor:
        history.append(
            {
                "id": str(doc.get("_id", "")),
                "prediction": doc.get("prediction"),
                "payload": doc.get("payload", {}),
                "created_at": doc.get("created_at"),
            }
        )
    return history

