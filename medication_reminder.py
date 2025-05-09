import json
import os

# File where we'll save medications
DATA_FILE = "medications.json"

def load_medications():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_medications(medications):
    with open(DATA_FILE, "w") as file:
        json.dump(medications, file, indent=4)

def add_medication():
    name = input("Enter medication name: ")
    first_dose = input("Enter first dose time (HH:MM in 24hr format): ")
    frequency = input("Enter frequency (in hours): ")

    try:
        frequency = float(frequency)
    except ValueError:
        print("Invalid frequency. Must be a number.")
        return

    medication = {
        "name": name,
        "first_dose": first_dose,
        "frequency": frequency
    }

    medications = load_medications()
    medications.append(medication)
    save_medications(medications)

    print(f"✅ Medication '{name}' added successfully!")

def view_medications():
    medications = load_medications()
    if not medications:
        print("No medications found.")
        return

    print("\n💊 Current Medications:")
    for i, med in enumerate(medications, 1):
        print(f"{i}. {med['name']} - First Dose: {med['first_dose']} - Every {med['frequency']} hours")
    print()

def main():
    while True:
        print("\n--- Medication Reminder ---")
        print("1. Add Medication")
        print("2. View Medications")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_medication()
        elif choice == "2":
            view_medications()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
