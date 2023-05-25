import os
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter


def generate_final_report(directory_path):
    template_file = "template.xlsx"

    # Create a dictionary to map the sheet names
    sheet_mapping = {
        "Unassociated Elastic IPs": "Unattached Elastic IPs",
        "Old AMIs": "EC2 Old Image",
        "Old EBS Snapshots": "EC2 Old Snapshots",
        "Unattached Volumes": "Unattached EBS Volumes",
        "Unused AMIs": "EC2 Image Not Associated",
        "Old RDS Snapshots": "RDS Old Snapshots",
        # Add more mappings as needed
    }

    # Create a dictionary to map the columns to remove from specific sheets
    column_removal = {
        "Old AMIs": ["Storage Size (GB)", "Snapshot Count"],
        "Unused AMIs": ["Storage Size (GB)", "Snapshot Count"],
        # Add more mappings as needed
    }

    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if "Validated" in filename and filename.endswith(".xlsx"):
            # Get the full file path
            file_path = os.path.join(directory_path, filename)

            # Load the validated Excel file
            validated_wb = load_workbook(file_path)

            # Create a new workbook based on the template
            final_wb = load_workbook(template_file)

            # Iterate over the sheets in the validated workbook
            for validated_sheet in validated_wb.sheetnames:
                if validated_sheet in sheet_mapping and sheet_mapping[validated_sheet] in final_wb.sheetnames:
                    # Get the corresponding sheet in the final workbook
                    final_sheet = final_wb[sheet_mapping[validated_sheet]]

                    # Get the corresponding sheet in the validated workbook
                    validated_sheet = validated_wb[validated_sheet]

                    # Copy the data from the validated sheet to the final sheet
                    for i, row in enumerate(validated_sheet.iter_rows(values_only=True), start=1):
                        if i > 1:  # Exclude the first row (header)
                            final_sheet.append(row)

            # Remove specified columns from the final sheet
            for sheet_name, columns_to_remove in column_removal.items():
                if sheet_name in final_wb.sheetnames:
                    final_sheet = final_wb[sheet_name]
                    for column_name in columns_to_remove:
                        column_letter = get_column_letter(final_sheet[column_name].column)
                        final_sheet.delete_cols(final_sheet[column_name].column)

            # Generate the new filename by replacing "Validated" with "Final"
            new_filename = filename.replace("Validated", "Final")

            # Save the final workbook with the new filename
            final_wb.save(os.path.join(directory_path, new_filename))

            # Close the workbooks
            validated_wb.close()
            final_wb.close()


# Specify the directory path where your Excel files are located
directory_path = "C:\\Users\\awittung.2NDWATCH\\PycharmProjects\\CHscripts\\modules"

# Call the function
generate_final_report(directory_path)

# TODO: Overall - Script currently inputs the headers from the Validated Excel Doc. Need to remove it.
#  All Sheets - Need to grab regions per sheet and provide a list in each sheet of each region and the total items.
#  All Sheets - If no info, remove sheet or update Overview Formula to say 'N/A'
#  Overview - Formulas need to be automatically fixed with the new values.
#  EC2 Old Snapshots - Source excel needs 'Image Id' Column replaced with 'Snapshot Age' calculation.
#  Unattached Elastic IPs - Need 'Unattached At' Column after 'Public IP' Column
#  RDS Old Snapshots - Need 'Instance Id' Column after 'Snapshot Id'
#  RDS Old Snapshots - Need calculated 'Snapshot Age' column after 'Create Date'
