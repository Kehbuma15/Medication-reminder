import json
import os
import time
from datetime import datetime, timedelta

import time




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

def start_reminder_loop():
    medications = load_medications()
    if not medications:
        print("No medications to remind. Please add some first.")
        return

    # Track next dose times
    next_doses = []

    for med in medications:
        try:
            # Convert first_dose string to datetime object for today
            dose_time = datetime.strptime(med["first_dose"], "%H:%M")
            now = datetime.now()
            # Adjust dose_time to today's date
            dose_time = dose_time.replace(year=now.year, month=now.month, day=now.day)
            # If dose_time is in the past, keep adding frequency until it's in the future
            while dose_time < now:
                dose_time += timedelta(hours=med["frequency"])
            next_doses.append((med, dose_time))
        except Exception as e:
            print(f"Error in medication {med['name']}: {e}")

    print("\n⏰ Starting reminder loop (Press Ctrl+C to stop)...")

    try:
        while True:
            now = datetime.now()
            for i in range(len(next_doses)):
                med, dose_time = next_doses[i]
                if now >= dose_time:
                    print(f"\n🔔 Time to take your medication: {med['name']} (scheduled for {dose_time.strftime('%H:%M')})")
                    # Schedule the next dose
                    dose_time += timedelta(hours=med["frequency"])
                    next_doses[i] = (med, dose_time)
            time.sleep(60)  # Wait for 60 seconds
    except KeyboardInterrupt:
        print("\nReminder loop stopped.")

def main():
    while True:
        print("\n--- Medication Reminder ---")
        print("1. Add Medication")
        print("2. View Medications")
        print("3. Start Reminder")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_medication()
        elif choice == "2":
            view_medications()
        elif choice == "3":
            start_reminder_loop()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
