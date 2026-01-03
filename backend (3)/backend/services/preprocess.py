import pickle
import numpy as np
import pandas as pd
from pathlib import Path

# -----------------------------
# Load Models Folder
# -----------------------------
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"


# -----------------------------
# SAFE PICKLE LOADER
# -----------------------------
def safe_load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


# -----------------------------
# LOAD SAVED OBJECTS
# -----------------------------
LABEL_ENCODERS = safe_load_pickle(MODEL_DIR / "label_encoders.pkl")
SCALER = safe_load_pickle(MODEL_DIR / "scaler.pkl")


# -----------------------------
# COLUMNS MATCHING TRAINING
# -----------------------------
CATEGORICAL_COLS = [
    "category",
    "domain",
    "category_type",
    "difficulty",
    "mood",
    "recent_event",
]

NUMERIC_COLS = [
    "study_time",
    "review_count",
    "confidence",
    "stress_level",
    "sleep_hours",
    "distraction_level",
    "attention_level",
]


# -----------------------------
# FEATURE ORDER (same as training)
# -----------------------------
FEATURE_ORDER = [
    "topic_name",
    "category",
    "domain",
    "category_type",
    "study_time",
    "review_count",
    "confidence",
    "difficulty",
    "stress_level",
    "sleep_hours",
    "mood",
    "distraction_level",
    "recent_event",
    "attention_level",
]


# -----------------------------
# Safe deterministic encoders
# -----------------------------
CATEGORICAL_VALUE_MAPPINGS = {
    "category": {
        "science": 0, "mathematics": 1, "history": 2, "literature": 3,
        "language": 4, "arts": 5, "technology": 6, "business": 7, "other": 8
    },
    "domain": {
        "school": 0, "pu": 1, "college": 2, "university": 3,
        "online": 4, "self-study": 5
    },
    "category_type": {
        "concept": 0, "formula": 1, "fact": 2, "procedure": 3,
        "principle": 4, "theory": 5, "other": 6
    },
    "difficulty": {
        "easy": 0, "medium": 1, "hard": 2, "very hard": 3
    },
    "mood": {
        "calm": 0, "stressed": 1, "excited": 2, "tired": 3,
        "focused": 4, "anxious": 5, "confident": 6, "neutral": 7
    },
    "recent_event": {
        "none": 0, "exam": 1, "test": 2, "presentation": 3,
        "assignment": 4, "deadline": 5, "holiday": 6, "illness": 7, "other": 8
    }
}


def encode_string_deterministic(value: str, col_name: str, target_mean: float = 0.0, target_std: float = 1.0) -> float:
    if not value or str(value).strip() == "":
        return target_mean

    value = str(value).lower().strip()

    if col_name in CATEGORICAL_VALUE_MAPPINGS:
        if value in CATEGORICAL_VALUE_MAPPINGS[col_name]:
            mapped_val = CATEGORICAL_VALUE_MAPPINGS[col_name][value]
            max_mapped = max(CATEGORICAL_VALUE_MAPPINGS[col_name].values())
            normalized = (mapped_val / max_mapped) * 2 - 1
            return float(target_mean + normalized * target_std * 2.0)

    hash_val = 0
    prime = 31
    for char in value:
        hash_val = (hash_val * prime + ord(char)) % (2**31)

    normalized = (hash_val % 100000) / 100000.0
    return float(target_mean + (normalized - 0.5) * target_std * 4.0)


def encode_topic_name(topic_name: str) -> float:
    if not topic_name or str(topic_name).strip() == "":
        return 48.62

    topic_str = str(topic_name).strip()
    hash_val = 0
    prime = 5381
    for char in topic_str:
        hash_val = (hash_val * prime + ord(char)) % (2**31)

    normalized = (hash_val % 100000) / 100000.0
    return float(48.62 + (normalized - 0.5) * 28.31 * 2.0)


# -----------------------------
# MAIN PREPROCESS FUNCTION
# -----------------------------
def preprocess_payload(payload: dict):
    """Preprocess and return a scaled DataFrame (NO WARNING)."""

    feature_values = []

    for col in FEATURE_ORDER:
        if col not in payload:
            feature_values.append(0.0)
            continue

        val = payload[col]

        if val is None or (isinstance(val, str) and val.strip() == ""):
            if col in NUMERIC_COLS:
                feature_values.append(0.0)
            elif col == "topic_name":
                feature_values.append(encode_topic_name(""))
            else:
                feature_values.append(0.0)
            continue

        if col == "topic_name":
            feature_values.append(encode_topic_name(str(val)))

        elif col in CATEGORICAL_COLS:
            encoder = LABEL_ENCODERS.get(col)
            val_lower = str(val).lower().strip()

            if encoder and val_lower in encoder.classes_:
                feature_values.append(float(encoder.transform([val_lower])[0]))
            else:
                stats = {
                    "category": {"mean": 9.996, "std": 6.060},
                    "domain": {"mean": 5.311, "std": 2.550},
                    "category_type": {"mean": 0.364, "std": 0.481},
                    "difficulty": {"mean": 1.5, "std": 1.0},
                    "mood": {"mean": 2.0, "std": 1.5},
                    "recent_event": {"mean": 1.0, "std": 1.0},
                }.get(col, {"mean": 0.0, "std": 1.0})

                feature_values.append(
                    encode_string_deterministic(val, col, stats["mean"], stats["std"])
                )

        elif col in NUMERIC_COLS:
            try:
                feature_values.append(float(val))
            except:
                feature_values.append(0.0)

        else:
            feature_values.append(0.0)

    # -----------------------------
    # FIX: Create DataFrame with column names
    # -----------------------------
    df = pd.DataFrame([dict(zip(FEATURE_ORDER, feature_values))])

    # -----------------------------
    # Scale using fitted scaler (NO MORE WARNINGS)
    # -----------------------------
    df_scaled = SCALER.transform(df)

    return df_scaled
