# grade_system.py

try:
    # Get input from the user
    mark = float(input("Enter your mark (0-100): "))

    # Validate range
    if mark < 0 or mark > 100:
        print("Invalid input! Please enter a mark between 0 and 100.")

    else:
        # Determine grade
        if mark >= 90:
            grade = "A"
        elif mark >= 80:
            grade = "B"
        elif mark >= 70:
            grade = "C"
        elif mark >= 60:
            grade = "D"
        else:
            grade = "E"

        # Display result
        print(f"Mark: {mark} -> Grade: {grade}")

except ValueError:
    print("Invalid input! Please enter a numeric value.")