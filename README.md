# ComfyUI-CustomCSVLoader

## Description

This node retrieves values from CSV files using an input CSV file, row name, and column name.

## How to Use

1. Download the zip file from the main branch and unzip it into your ComfyUI directory at `your-ComfyUI-path/custom_nodes/Custom-CSV-Loader-Node`.
2. Copy the CSV files you want to retrieve data from into the folder `your-ComfyUI-path/custom_nodes/Custom-CSV-Loader-Node/CSV` (e.g., `example.csv`).
3. Restart your ComfyUI.

## Features

1. This node allows you to choose the CSV files in the folder. The supported CSV delimiter is `;`. Please use CSV files with the `;` delimiter; if your CSV file uses a comma (`,`), convert it to the supported format.
2. This node lets you select files, rows, and columns from dropdown lists in the UI, so you can see the exact row and column when setting up the input.
3. To avoid duplicate row or column names in the CSV, the dropdown lists will display entries like `rowName1_1`, `rowName2_2` and `columnName1_1`, `columnName2_2`, ensuring that your selection is unique.