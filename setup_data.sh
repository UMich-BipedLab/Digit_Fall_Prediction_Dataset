#!/bin/bash

DATASET_REPO="https://huggingface.co/datasets/Gokul97/digit_fall_prediction_dataset"
DATASET_DIR="hf_dataset_tmp"

SIM_TARGET_DIR="digit_data/feature_data/sim"
REAL_TARGET_DIR="digit_data/feature_data/real"

git clone "$DATASET_REPO" "$DATASET_DIR"

mkdir -p "$SIM_TARGET_DIR"
mkdir -p "$REAL_TARGET_DIR"

for zipfile in "$DATASET_DIR/sim"/*.zip; do
    [ -f "$zipfile" ] && unzip -o "$zipfile" -d "$SIM_TARGET_DIR"
done

for zipfile in "$DATASET_DIR/real"/*.zip; do
    [ -f "$zipfile" ] && unzip -o "$zipfile" -d "$REAL_TARGET_DIR"
done

rm -rf "$DATASET_DIR"
