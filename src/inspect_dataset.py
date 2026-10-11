
import argparse
from pathlib import Path

import pandas as pd


NORMAL_LABEL = "000 - Normal"


def inspect_dataset(csv_path: Path, sample_rows: int = 5) -> None:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}\n"
            "Place the SR-BH CSV at the specified path and try again."
        )

    print(f"Reading dataset: {csv_path}")
    df = pd.read_csv(csv_path, low_memory=False)

    print("\n" + "=" * 70)
    print("DATASET OVERVIEW")
    print("=" * 70)
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB")

    print("\n" + "=" * 70)
    print("COLUMN NAMES AND DATA TYPES")
    print("=" * 70)
    for column, dtype in df.dtypes.items():
        print(f"{column}: {dtype}")

    print("\n" + "=" * 70)
    print("MISSING VALUES")
    print("=" * 70)
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("No pandas-recognized missing values found.")
    else:
        for column, count in missing.items():
            print(f"{column}: {count:,} ({count / len(df):.2%})")

    # SR-BH attack labels are generally represented by binary columns.
    # We identify likely label columns by their known naming convention,
    # then report their values without assuming every dataset is identical.
    label_columns = [
        column
        for column in df.columns
        if column == NORMAL_LABEL
        or (
            " - " in column
            and column.split(" - ", maxsplit=1)[0].strip().isdigit()
        )
    ]

    print("\n" + "=" * 70)
    print("POTENTIAL LABEL COLUMNS")
    print("=" * 70)

    if not label_columns:
        print("No label columns matched the expected CAPEC naming convention.")
        print("Review the column list above and update the label detection rule.")
    else:
        print(f"Found {len(label_columns)} potential label columns.")

        for column in label_columns:
            values = df[column].value_counts(dropna=False).to_dict()
            print(f"\n{column}: {values}")

        # Check whether records have more than one positive label.
        numeric_labels = df[label_columns].apply(
            pd.to_numeric, errors="coerce"
        ).fillna(0)

        positive_counts = numeric_labels.gt(0).sum(axis=1)
        multi_label_rows = int((positive_counts > 1).sum())
        unlabeled_rows = int((positive_counts == 0).sum())

        print("\nLabel overlap summary:")
        print(f"Rows with multiple positive labels: {multi_label_rows:,}")
        print(f"Rows with no positive label: {unlabeled_rows:,}")

    request_columns = [
        "request_http_method",
        "request_http_request",
        "request_http_protocol",
        "request_content_type",
        "request_user_agent",
        "request_body",
    ]

    print("\n" + "=" * 70)
    print("REQUEST-TIME FEATURE AVAILABILITY")
    print("=" * 70)

    for column in request_columns:
        if column in df.columns:
            print(f"[FOUND] {column}")
        else:
            print(f"[MISSING] {column}")

    response_columns = [
        column
        for column in df.columns
        if column.startswith("response_")
    ]

    print("\nResponse-side columns detected (do not use as request-time inputs):")
    if response_columns:
        for column in response_columns:
            print(f"- {column}")
    else:
        print("None found using the response_ prefix.")

    print("\n" + "=" * 70)
    print(f"FIRST {sample_rows} ROWS")
    print("=" * 70)

    # Limit displayed text so long cookies and request bodies do not flood
    # the terminal.
    with pd.option_context(
        "display.max_columns", 12,
        "display.max_colwidth", 100,
        "display.width", 180,
    ):
        print(df.head(sample_rows).to_string(index=False))

    print("\nInspection completed. No files were modified.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect the SR-BH 2020 HTTP request dataset."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("data/raw/data_capec_multilabel.csv"),
        help="Path to the dataset CSV.",
    )
    parser.add_argument(
        "--sample-rows",
        type=int,
        default=5,
        help="Number of sample rows to display.",
    )
    args = parser.parse_args()

    if args.sample_rows < 1:
        parser.error("--sample-rows must be at least 1")

    inspect_dataset(args.csv, args.sample_rows)


if __name__ == "__main__":
    main()
