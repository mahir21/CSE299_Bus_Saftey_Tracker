import pandas as pd

def check_plate_safety(csv_file, plate_number):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    print(df)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        if row['Number Plate'] == plate_number:
            return row['Vehicle Saftey Index']

    # Plate number not found
    return None

csv_file = r'C:\Users\USER\Desktop\CSE299Project\299Train.csv'  # Use raw string (r) to avoid escape characters

# Specify the plate number to check
plate_number = 1128

# Call the function to check the plate safety index
safety_index = check_plate_safety(csv_file, plate_number)

if safety_index is not None:
    print(f"The safety index for plate number {plate_number} is {safety_index}.")
else:
    print("No matching plate number found.")
