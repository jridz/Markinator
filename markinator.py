import json
import os


# Special formatting for errors, warnings and notices. Also does underlines.
def print_special(action, text):
    if action == "underline":
        print("\033[4m" + text + "\033[0m")
    elif action == "error":
        print("\033[91m" + "Error: " + text + "\033[0m")
    elif action == "warn":
        print("\033[93m" + "Warning: " + text + "\033[0m")
    elif action == "inform":
        print("\033[94m" + "Note: " + text + "\033[0m")
    # If action not found
    else:
        print(f"Internal Error: Action in print_special({action}, {text}) not found.")


# Calculate percentage from score and max_score
def calculate_percentage(score, max_score):
    percentage = (score / max_score) * 100
    # Round to 2 decimal places for sensibility
    percentage = "{:.2f}%".format(percentage)
    return percentage


# Used to check if marks.json exists
def marksfile_exists():
    # If file does exist
    if os.path.isfile("marks.json"):
        # If file is empty
        if os.path.getsize("marks.json") == 0:
            # Write an empty list to prevent errors
            with open("marks.json", "w") as file:
                file.write(json.dumps([]))
                file.close()
        return True
    # If file doesn't exist
    else:
        print_special("warn", "Marksfile does not exist.")
        # Get confirmation
        confirmation = input("Would you like to make marks.json? (yes/no)\n").lower()
        if confirmation == "yes" or confirmation == "y":
            os.open("marks.json", os.O_CREAT | os.O_WRONLY)
            # Make new file
            with open("marks.json", "w") as new_file:
                new_file.write(json.dumps([], indent=4))
            print_special("inform", "Successfully created marks.json!")
            return True
        # If confirmation failed
        else:
            print_special("warn", "File not created.")
            return False


# Creates a new subject in marks.json
def new_subject():
    with open("marks.json", "r+") as file:
        data = json.load(file)
        subject_name = input("New subject name: ")
        # Get confirmation
        confirmation = input(f"Are you sure you want to create subject \"{subject_name}\"? (yes/no) ").lower()
        if confirmation == "y" or confirmation == "yes":
            pass
        # If confirmation failed
        else:
            print_special("warn", "Subject creation cancelled.")
            return
        # If confirmation succeeds add subject to marks
        data.append({"name": subject_name, "marks": []})
        # Write changes to file
        file.seek(0)
        json.dump(data, file)
        file.truncate()
        # Inform that subject was created
        print_special("inform", f"Created subject {subject_name}!")
        return


# Deletes a subject from marks.json
def delete_subject():
    with open("marks.json", "r+") as file:
        data = json.load(file)
        # Address possibly empty file
        if len(data) == 0:
            print_special("error", "Empty file. Nothing to delete.")
            return
        # List subjects
        for subject_index, subject in enumerate(data, start=1):
            print(f"({subject_index}) {subject['name']}")
        print_special("inform", "Enter \"0\" to cancel.")
        # Get subject to delete
        try:
            subject_to_delete = int(input("Enter the number of the subject you want to delete: "))
        except ValueError:
            print_special("error", "Invalid input. Please pick from the list")
            return
        # Handle cancellation
        if subject_to_delete == 0:
            print_special("warn", "Deletion cancelled.")
            return
        # Get confirmation
        confirmation = input(f"Are you sure you want to delete subject {subject_to_delete}? (yes/no) ").lower()
        if confirmation == "y" or confirmation == "yes":
            pass
        else:
            print_special("warn", "Deletion cancelled.")
            return
        # Find selected_subject in file
        if 0 <= subject_to_delete <= len(data):
            pass
        else:
            print_special("error", "Invalid input. Please pick from the list.")
            return
        # Adjust for list beginning at 0
        subject_to_delete -= 1
        # Delete subject from file
        data.pop(subject_to_delete)
        # Write changes to file
        file.seek(0)
        json.dump(data, file)
        file.truncate()
        # Inform that subject was deleted
        print_special("inform", "The selected subject has been deleted.")
        return


# Adds a mark to a subject in marks.json
def new_mark():
    with open("marks.json", "r+") as file:
        data = json.load(file)
        # Address possibly empty file
        if len(data) == 0:
            print_special("error", "Empty file. No subjects to add to.")
            return
        # List subjects
        for subject_index, subject in enumerate(data, start=1):
            print(f"({subject_index}) {subject['name']}")
        print_special("inform", "Enter \"0\" to cancel.")
        # Get subject to add to
        try:
            selected_subject = int(input("Enter the number of the subject you want to add a mark to: "))
        except ValueError:
            print_special("error", "Invalid input. Please pick from the list")
            return
        if selected_subject == 0:
            print_special("warn", "Creation cancelled.")
            return
        # Adjust for list beginning at 0
        selected_subject -= 1
        # Make sure selected_subject is within the list range
        if 0 <= selected_subject <= len(data):
            pass
        else:
            print_special("error", "Invalid input. Please pick from the list.")
            return
        # Find selected_subject in file
        for subject_index, subject in enumerate(data):
            if subject_index != selected_subject:
                continue
            mark_name = input(f"Name for new mark in {subject['name']} (e.g. \"Math Final\"): ")
            # Get achieved score
            try:
                score = float(input("Score achieved (e.g. " "\033[92m" "81" "\033[0m" "/100): "))
            except ValueError:
                print_special("error", "Invalid input. Must be a number.")
                return
            if score < 0:
                print_special("error", "Invalid input. Score must be 0 or higher.")
                return
            # Get max score
            try:
                max_score = float(input("Max score achievable (e.g. " "81/" "\033[92m" "100" "\033[0m" "): "))
            except ValueError:
                print_special("error", "Invalid input. Must be a number.")
                return
            # Reject invalid score ratios
            if max_score < score:
                print_special("error", "Invalid input. Max achieveable score must be higher than score.")
                return
            # Add new mark to selected_subject
            subject["marks"].append({"mark_name": mark_name, "score": score, "max_score": max_score})
            # Write changes to file
            file.seek(0)
            json.dump(data, file)
            file.truncate()
            print_special("inform", f"{mark_name} has successfully been added to {subject['name']}.")
            return


# Display all marks across all subjects
def view_all_marks():
    with open("marks.json", "r") as file:
        data = json.load(file)
        # For each subject
        for subject_index, subject in enumerate(data, start=1):
            # Print subject name
            print_special("underline", f"\n{subject['name']}")
            # If subject marks are empty
            if len(subject['marks']) == 0:
                print("(N/A) No marks for this subject.")
                continue
            # If not empty
            for mark_index, mark in enumerate(subject['marks'], start=1):
                # Print each mark in this format: (1) Math Test: 10/100 [10.00%]
                print(f"({mark_index}) {mark['mark_name']}: {mark['score']}/{mark['max_score']} "
                      f"[{calculate_percentage(mark['score'], mark['max_score'])}]")
        print("\n")
        return


def view_subject_marks():
    with open("marks.json", "r") as file:
        data = json.load(file)
        # Address possibly empty file
        if len(data) == 0:
            print_special("error", "Empty file. Nothing to list.")
            return
        # List subjects
        for subject_index, subject in enumerate(data, start=1):
            print(f"({subject_index}) {subject['name']}")
        print_special("inform", "Enter \"0\" to cancel.")
        # Get selected_subject
        try:
            selected_subject = int(input("Enter the number of the subject you want to list marks from: "))
        except ValueError:
            print_special("error", "Invalid input. Please pick from the list")
            return
        if selected_subject == 0:
            print_special("warn", "Mark viewing cancelled.")
            return
        # Make sure selected_subject is within the list range
        if 0 <= selected_subject <= len(data):
            pass
        else:
            print_special("error", "Invalid input. Please pick from the list.")
            return
        # Adjust for list beginning at 0
        selected_subject -= 1
        # Find selected_subject in file
        for subject_index, subject in enumerate(data):
            if subject_index != selected_subject:
                continue
            print_special("underline", f"\n{subject['name']}")
            # If subject marks are empty
            if len(subject['marks']) == 0:
                print_special("error", "Subject marks empty. Nothing to list.")
                continue
            # If not empty
            for mark_index, mark in enumerate(subject['marks'], start=1):
                # Print each mark in this format: (1) Math Test: 10/100 [10.00%]
                print(f"({mark_index}) {mark['mark_name']}: {mark['score']}/{mark['max_score']} "
                      f"[{calculate_percentage(mark['score'], mark['max_score'])}]")
        # Print empty line for better formatting
        print("\n")
        return


def delete_mark():
    with open("marks.json", "r+") as file:
        data = json.load(file)
        # Address possibly empty file
        if len(data) == 0:
            print_special("error", "Empty file. Nothing to list.")
            return
        # List subjects
        for subject_index, subject in enumerate(data, start=1):
            print(f"({subject_index}) {subject['name']}")
        print_special("inform", "Enter \"0\" to cancel.")
        # Get subject to delete from
        try:
            selected_subject = int(input("Enter the number of the subject you want to delete from: "))
        except ValueError:
            print_special("error", "Invalid input. Please pick from the list")
            return
        if selected_subject == 0:
            print_special("warn", "Deletion cancelled.")
            return
        # Make sure selected_subject is within the list range
        if 0 <= selected_subject <= len(data):
            pass
        else:
            print_special("error", "Invalid input. Please pick from the list.")
            return
        # Adjust for list beginning at 0
        selected_subject -= 1
        # Loop over data to find selected_subject
        for subject_index, subject in enumerate(data):
            if subject_index != selected_subject:
                continue
            else:
                pass
            # When correct subjected is selected
            if len(subject['marks']) == 0:
                print_special("error", "Subject marks empty. Nothing to list.")
                return
            # List marks
            for mark_index, mark in enumerate(subject['marks'], start=1):
                print(f"({mark_index}) {mark['mark_name']}: {mark['score']}/{mark['max_score']} "
                      f"[{calculate_percentage(mark['score'], mark['max_score'])}]")
            print_special("inform", "Enter \"0\" to cancel.")
            # Get mark_to_delete
            try:
                mark_to_delete = int(input("Enter the number of the mark you want to delete: "))
            except ValueError:
                print_special("error", "Invalid input. Please pick from the list")
                return
            if mark_to_delete == 0:
                print_special("warn", "Deletion cancelled.")
                return
            # Make sure mark_to_delete is within the list range
            if 0 <= mark_to_delete <= len(subject['marks']):
                pass
            else:
                print_special("error", "Invalid input. Please pick from the list.")
                return
            # Adjust for list beginning at 0
            mark_to_delete -= 1
            # Delete subject from list
            subject['marks'].pop(mark_to_delete)
            print_special("inform", "The selected mark has been deleted.")
            # Write changes to file
            file.seek(0)
            json.dump(data, file)
            file.truncate()
            # When complete exit function
            return


# Gets action to complete from user, runs all other functions
def get_action():
    # List actions
    print("(0) Exit Markinator\n"
          "(1) Make a new subject\n"
          "(2) Delete a subject\n"
          "(3) Add new mark\n"
          "(4) Delete a mark\n"
          "(5) View all marks\n"
          "(6) View subject marks\n"
          )
    # Get selected action
    try:
        action = int(input("Select an action: "))
    except ValueError:
        print_special("error", "Invalid action. Please pick from the list")
        return
    # Execute corresponding action
    if action == 0:
        print_special("inform", "Thanks for using Markinator!")
        print("Exiting...")
        exit()
    elif action == 1:
        new_subject()
    elif action == 2:
        delete_subject()
    elif action == 3:
        new_mark()
    elif action == 4:
        delete_mark()
    elif action == 5:
        view_all_marks()
    elif action == 6:
        view_subject_marks()
    # Handle invalid actions
    else:
        print_special("error", "Invalid input. Please pick from the list")
        return
    return


# Main application
def main():
    # Welcome text!
    print_special("underline", "Welcome to Markinator!\n")
    # If marksfile cannot be loaded
    if not marksfile_exists():
        print_special("error", "Cannot load marks.json. File does not exist.")
        exit()
    # Loop action selection until program is exited
    while True:
        get_action()


# Run the program
main()
