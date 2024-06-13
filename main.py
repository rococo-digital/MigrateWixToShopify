import csv

# Read the Wix CSV file
with open('catalog_products.csv', mode='r', encoding='utf-8-sig') as wix_file:
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
    with open('shopify_products_final.csv', mode='w', newline='', encoding='utf-8') as shopify_file:
        shopify_writer = csv.DictWriter(shopify_file, fieldnames=shopify_headers)
        shopify_writer.writeheader()

        Handle, Title, Body, Collection, Vendor, VariantSKU, VariantPrice, VariantInventoryQty, VariantGrams, \
            CostPerItem, ImageSrc, productOptionName1, productOptionName2, \
            productOptionName3 = ("", "", "", "", "", "", "", "", "", "", "", "", "", "")

        index = 0
        prod = 0
        for row in wix_reader:
            shopify_row = {header: '' for header in shopify_headers}

            if row.get("fieldType", '') == "Product":
                #     Take some note
                Handle = row.get("handleId", '')
                Title = row.get("name", '')
                Body = row.get("description", '')
                Collection = row.get("collection", '')
                Vendor = row.get("brand", '')
                VariantSKU = row.get("sku", '')
                VariantPrice = row.get("price", '')
                VariantInventoryQty = row.get("inventory", '')
                VariantGrams = row.get("weight", '')
                CostPerItem = row.get("cost", '')
                ImageSrc = row.get("productImageUrl", '')
                productOptionName1 = row.get("productOptionName1", '')
                productOptionName2 = row.get("productOptionName2", '')
                productOptionName3 = row.get("productOptionName3", '')
                index = 0
                prod = prod + 1
            else:

                images = ImageSrc.split(';')

                # Directly mapping Wix fields to Shopify fields
                if index == 0:
                    shopify_row["Title"] = Title
                    shopify_row["Body (HTML)"] = Body
                    shopify_row["Vendor"] = Vendor
                    shopify_row["Collection"] = Collection
                    # shopify_row["Product Category"] = Collection
                    shopify_row["Published"] = "True"
                    shopify_row["Variant SKU"] = VariantSKU
                    shopify_row["Variant Grams"] = 0  # VariantGrams
                    shopify_row["Variant Inventory Tracker"] = "shopify"
                    shopify_row["Cost per item"] = CostPerItem
                    shopify_row["Option1 Name"] = productOptionName1
                    shopify_row["Option2 Name"] = productOptionName2
                    shopify_row["Option3 Name"] = productOptionName3
                    shopify_row["Status"] = "active"
                    shopify_row["Included / International"] = "True"
                    shopify_row["Included / Bangladesh"] = "True"
                    shopify_row["Gift Card"] = "False"
                    shopify_row["Variant Taxable"] = "True"
                    shopify_row["Variant Requires Shipping"] = "True"

                shopify_row["Handle"] = Handle.replace('_', '-')
                shopify_row["Variant Inventory Qty"] = 100  # VariantInventoryQty
                shopify_row["Variant Weight Unit"] = "kg"
                shopify_row["Variant Fulfillment Service"] = "manual"
                shopify_row["Variant Inventory Policy"] = "deny"
                shopify_row["Variant Price"] = row.get("surcharge", '')
                shopify_row["Image Src"] = f"https://static.wixstatic.com/media/{images[index]}" if len(
                    images) > index else ''
                shopify_row["Image Position"] = index + 1 if len(images) > index else ''
                shopify_row["Option1 Value"] = row.get("productOptionDescription1", '')
                shopify_row["Option2 Value"] = row.get("productOptionDescription2", '')
                shopify_row["Option3 Value"] = row.get("productOptionDescription3", '')

                shopify_writer.writerow(shopify_row)
                index = index + 1

print("Data transfer from Wix to Shopify CSV completed.")
