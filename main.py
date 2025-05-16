import csv
import traceback
import re

def create_seo_friendly_handle(text):
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[_\s]+', '-', text)
    # Remove special characters except hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading and trailing hyphens
    text = text.strip('-')
    return text

try:
    # Read the Wix CSV file - Change this line to use the real file
    print("Opening catalog_products_real.csv file...")
    with open('catalog_products_real.csv', mode='r', encoding='utf-8-sig') as wix_file:
        wix_reader = csv.DictReader(wix_file)

        # Prepare the Shopify CSV headers
        shopify_headers = [
            "Handle", "Title", "Body (HTML)", "Vendor", "Collection", "Type", "Tags", "Published",
            "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
            "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
            "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
            "Variant Requires Shipping", "Variant Taxable", "Variant Barcode", "Image Src", "Image Position",
            "Image Alt Text", "Gift Card", "SEO Title", "SEO Description", "Google Shopping / Google Product Category",
            "Google Shopping / Gender", "Google Shopping / Age Group", "Google Shopping / MPN",
            "Google Shopping / Condition", "Google Shopping / Custom Product", "Google Shopping / Custom Label 0",
            "Google Shopping / Custom Label 1", "Google Shopping / Custom Label 2", "Google Shopping / Custom Label 3",
            "Google Shopping / Custom Label 4", "Variant Image", "Variant Weight Unit", "Variant Tax Code",
            "Cost per item", "Included / Bangladesh", "Price / Bangladesh", "Compare At Price / Bangladesh",
            "Included / International", "Price / International", "Compare At Price / International", "Status"
        ]

        # Write to the Shopify CSV file
        print("Creating shopify_products_final.csv file...")
        with open('shopify_products_final.csv', mode='w', newline='', encoding='utf-8') as shopify_file:
            shopify_writer = csv.DictWriter(shopify_file, fieldnames=shopify_headers)
            shopify_writer.writeheader()

            row_count = 0
            product_count = 0
            
            print("Processing rows...")
            for row in wix_reader:
                try:
                    row_count += 1
                    if row_count % 100 == 0:
                        print(f"Processed {row_count} rows...")
                        
                    # Skip rows that don't have fieldType=Product
                    if row.get("fieldType", '') != "Product":
                        continue
                    
                    product_count += 1
                    # Create SEO-friendly handle from the product name
                    handle = create_seo_friendly_handle(row.get("name", ''))
                    title = row.get("name", '')
                    body = row.get("description", '')
                    collection = row.get("collection", '')
                    vendor = row.get("brand", 'Jomanda')  # Default to Jomanda if not specified
                    sku = row.get("sku", '')
                    price = row.get("price", '')
                    inventory = row.get("inventory", '')
                    weight = row.get("weight", '')
                    cost = row.get("cost", '')
                    image_urls = row.get("productImageUrl", '').split(';') if row.get("productImageUrl") else []
                    
                    option1_name = row.get("productOptionName1", '')
                    option1_value = row.get("productOptionDescription1", '')
                    option2_name = row.get("productOptionName2", '')
                    option2_value = row.get("productOptionDescription2", '')
                    option3_name = row.get("productOptionName3", '')
                    option3_value = row.get("productOptionDescription3", '')
                    
                    print(f"Found product: {title} (Handle: {handle})")
                    
                    # Create the main product record with first image
                    shopify_row = {header: '' for header in shopify_headers}
                    
                    shopify_row["Handle"] = handle
                    shopify_row["Title"] = title
                    shopify_row["Body (HTML)"] = body
                    shopify_row["Vendor"] = vendor
                    shopify_row["Collection"] = collection
                    # Use collection as Tags too since the script doesn't map Tags
                    shopify_row["Tags"] = collection
                    shopify_row["Published"] = "True"
                    shopify_row["Variant SKU"] = sku
                    shopify_row["Variant Grams"] = weight if weight else "0"
                    shopify_row["Variant Inventory Tracker"] = "shopify"
                    
                    # Convert inventory values
                    if inventory == "InStock":
                        shopify_row["Variant Inventory Qty"] = "100"
                    elif inventory == "OutOfStock":
                        shopify_row["Variant Inventory Qty"] = "0"
                    else:
                        try:
                            # Try to convert to integer if it's a number
                            inventory_qty = int(inventory)
                            shopify_row["Variant Inventory Qty"] = str(inventory_qty)
                        except (ValueError, TypeError):
                            shopify_row["Variant Inventory Qty"] = "100"  # Default value
                    
                    shopify_row["Cost per item"] = cost
                    shopify_row["Option1 Name"] = option1_name
                    shopify_row["Option1 Value"] = option1_value
                    shopify_row["Option2 Name"] = option2_name
                    shopify_row["Option2 Value"] = option2_value
                    shopify_row["Option3 Name"] = option3_name
                    shopify_row["Option3 Value"] = option3_value
                    shopify_row["Status"] = "active"
                    shopify_row["Included / International"] = "True"
                    shopify_row["Included / Bangladesh"] = "True"
                    shopify_row["Gift Card"] = "False"
                    shopify_row["Variant Taxable"] = "True"
                    shopify_row["Variant Requires Shipping"] = "True"
                    shopify_row["Variant Weight Unit"] = "kg"
                    shopify_row["Variant Fulfillment Service"] = "manual"
                    shopify_row["Variant Inventory Policy"] = "deny"
                    shopify_row["Variant Price"] = price
                    
                    # Handle the first image
                    if image_urls and len(image_urls) > 0 and image_urls[0]:
                        shopify_row["Image Src"] = f"https://static.wixstatic.com/media/{image_urls[0]}"
                        shopify_row["Image Position"] = "1"
                    
                    # Write the main product record
                    shopify_writer.writerow(shopify_row)
                    
                    # Add additional rows for extra images if any
                    for i in range(1, len(image_urls)):
                        if image_urls[i]:  # Skip empty image URLs
                            image_row = {header: '' for header in shopify_headers}
                            image_row["Handle"] = handle
                            image_row["Image Src"] = f"https://static.wixstatic.com/media/{image_urls[i]}"
                            image_row["Image Position"] = str(i + 1)
                            shopify_writer.writerow(image_row)
                    
                except Exception as e:
                    print(f"Error processing row {row_count}: {str(e)}")
                    print(f"Row data: {row}")
            
            print(f"Total products processed: {product_count}")
            print(f"Total rows read: {row_count}")

    print("Data transfer from Wix to Shopify CSV completed successfully.")
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print(traceback.format_exc())
