import csv


# Function to read the CSV file and return the data
def read_csv(file_name):
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        data = list(reader)
    return headers, data


# Function to write the sorted data to a new CSV file
def write_csv(file_name, headers, data):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


# Function to sort the data by 'Handle' and 'Option1 Value'
def sort_data(data):
    # Group data by 'Handle'
    grouped_data = {}
    for row in data:
        handle = row["Handle"]
        if handle not in grouped_data:
            grouped_data[handle] = []
        grouped_data[handle].append(row)

    # Sort each group
    sorted_data = []
    for handle in sorted(grouped_data):
        products = grouped_data[handle]
        # Extract the title row
        title_row = [product for product in products if product["Title"] != ""]
        other_rows = [product for product in products if product["Title"] == ""]

        if title_row:
            title_option1_value = title_row[0]["Option1 Value"]

            # Separate rows with the same Option1 Value as the title row
            same_option1_value_rows = [row for row in other_rows if row["Option1 Value"] == title_option1_value]
            different_option1_value_rows = [row for row in other_rows if row["Option1 Value"] != title_option1_value]

            option1_groups = {}

            # Iterate through each row in the dataset
            for row in different_option1_value_rows:
                option1_value = row["Option1 Value"]

                if option1_value not in option1_groups:
                    option1_groups[option1_value] = []

                option1_groups[option1_value].append(row)

            for option1_value, rows in option1_groups.items():
                sorted_rows = sorted(
                    rows,
                    key=lambda x: (int(x["Option2 Value"]) if x["Option2 Value"].isdigit() else x["Option2 Value"])
                )

                # Replace the unsorted rows with the sorted rows in the original dataset
                option1_groups[option1_value] = sorted_rows

            # Sort the rows with the same Option1 Value by Option2 Value, Option3 Value
            sorted_same_option1_value_rows = sorted(
                same_option1_value_rows,
                key=lambda x: (int(x["Option2 Value"]) if x["Option2 Value"].isdigit() else x["Option2 Value"])
            )

            sorted_data2 = []
            for option1_value in sorted(option1_groups.keys()):
                sorted_data2.extend(option1_groups[option1_value])

            # Combine the title row, same Option1 Value rows, and other sorted rows
            sorted_data.extend(title_row + sorted_same_option1_value_rows + sorted_data2)
        else:
            # If there is no title row, just sort normally
            print('')

    return sorted_data


# Main execution
headers, data = read_csv('shopify_products_final.csv')
sorted_data = sort_data(data)
write_csv('shopify_products_sorted.csv', headers, sorted_data)

print("Data sorting by Option1 Value, Option2 Value, and Option3 Value completed.")
