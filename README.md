# MigrateWixToShopify

A tool to help migrate your Wix store products to Shopify.

## Overview

This project provides a solution for migrating your product catalog from Wix to Shopify. It processes the exported Wix product data and prepares it for import into Shopify.

## Usage

### 1. Export Products from Wix

1. Go to your Wix store dashboard
2. Navigate to the Products tab
3. Click on "More Actions"
4. Select "Export"
5. Save the exported file as `catalogue_products_real.csv` in the project root directory

For detailed instructions on exporting products from Wix, visit: [Wix Stores: Exporting Your Product List](https://support.wix.com/en/article/wix-stores-exporting-your-product-list)

### 2. Process the Data

Run the scripts in the following order:

1. First, run the main migration script:
```bash
python main.py
```
This will create `shopify_products_final.csv`

2. Then, run the sorting script:
```bash
python sort_sheet.py
```
This will create the final `shopify_products_sorted.csv` file that you can import into Shopify.

### 3. Import to Shopify

The final `shopify_products_sorted.csv` file is ready to be imported into your Shopify store.

## File Structure

- `catalogue_products_real.csv` - Your exported Wix products data
- `main.py` - The main migration script that converts Wix data to Shopify format
- `sort_sheet.py` - Script that sorts the products for proper Shopify import
- `shopify_products_final.csv` - Intermediate file created by main.py
- `shopify_products_sorted.csv` - Final file ready for Shopify import
- `requirements.txt` - Python dependencies


