#!/bin/bash

DATASET_REPO="https://huggingface.co/datasets/<username>/<dataset_repo>"
DATASET_DIR="hf_dataset_tmp"
TARGET_DIR="digit_data/feature_data/sim"

git clone "$DATASET_REPO" "$DATASET_DIR"

mkdir -p "$TARGET_DIR"

for zipfile in "$DATASET_DIR"/*.zip; do
    unzip -o "$zipfile" -d "$TARGET_DIR"
done

rm -rf "$DATASET_DIR"
