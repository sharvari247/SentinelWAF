
import re
from urllib.parse import unquote

import pandas as pd


REQUEST_COLUMNS = [
    "request_http_method",
    "request_http_request",
    "request_http_protocol",
    "request_content_type",
    "request_user_agent",
    "request_body",
]


def safe_text(value) -> str:
    """Convert missing or non-string values into safe text."""
    if pd.isna(value):
        return ""
    return str(value)


def build_request_text(row: pd.Series) -> str:
    """Combine request-time fields into a single text representation."""
    parts = []

    for column in REQUEST_COLUMNS:
        value = safe_text(row.get(column, ""))
        if value:
            parts.append(f"{column}={value}")

    return " ".join(parts)


def extract_engineered_features(text: str) -> dict:
    """Extract lightweight numeric features from an HTTP request."""
    text = safe_text(text)
    lower_text = text.lower()

    decoded_text = unquote(text, errors="replace")

    length = len(text)
    unique_chars = len(set(text))

    return {
        "request_length": length,
        "unique_character_ratio": unique_chars / max(length, 1),
        "digit_ratio": sum(char.isdigit() for char in text) / max(length, 1),
        "special_character_ratio": sum(
            not char.isalnum() and not char.isspace()
            for char in text
        ) / max(length, 1),
        "single_quote_count": text.count("'"),
        "double_quote_count": text.count('"'),
        "semicolon_count": text.count(";"),
        "equals_count": text.count("="),
        "parenthesis_count": text.count("(") + text.count(")"),
        "url_encoded_percent_count": text.lower().count("%"),
        "url_decode_length_delta": len(decoded_text) - length,
        "sql_keyword_select": len(re.findall(r"\bselect\b", lower_text)),
        "sql_keyword_union": len(re.findall(r"\bunion\b", lower_text)),
        "sql_keyword_or": len(re.findall(r"\bor\b", lower_text)),
        "sql_keyword_insert": len(re.findall(r"\binsert\b", lower_text)),
        "sql_keyword_drop": len(re.findall(r"\bdrop\b", lower_text)),
        "shell_separator_count": text.count("|") + text.count("&&"),
        "path_traversal_marker_count": lower_text.count("../")
        + lower_text.count("..\\"),
        "control_character_count": sum(
            ord(char) < 32 and char not in "\t\n\r"
            for char in text
        ),
    }


def build_feature_frame(requests: pd.Series) -> pd.DataFrame:
    """Build the numeric feature matrix for a collection of request texts."""
    features = [
        extract_engineered_features(text)
        for text in requests
    ]

    return pd.DataFrame(features, index=requests.index)


def prepare_request_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return request text and engineered features from a raw dataset."""
    missing_columns = [
        column for column in REQUEST_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing expected request columns: "
            + ", ".join(missing_columns)
        )

    request_text = df.apply(build_request_text, axis=1)

    result = pd.DataFrame(index=df.index)
    result["request_text"] = request_text

    engineered = build_feature_frame(request_text)
    result = pd.concat([result, engineered], axis=1)

    return result
