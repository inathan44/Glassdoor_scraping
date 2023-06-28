from openpyxl import Workbook, load_workbook


def write_to_excel(file_name, data):
    try:
        # Load existing workbook if it exists, or create a new one
        try:
            workbook = load_workbook(file_name)
        except FileNotFoundError:
            workbook = Workbook()

        # Select the active sheet
        sheet = workbook.active

        # Add column headers if not already present
        if sheet.max_row == 1:
            column_headers = ("company", "title", "url", "keyword_snippets")
            sheet.append(column_headers)

        # Append data to the end of the columns
        sheet.append(data)

        # Save the workbook
        workbook.save(file_name)
        print("Data written to Excel successfully.")

    except Exception as e:
        print("An error occurred while writing to Excel:", str(e))
