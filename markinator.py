# Import neccessary libraries
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
        # Check if file is empty
        if os.path.getsize("marks.json") == 0:
            # If is empty, write an empty array to the file to prevent errors
            with open("marks.json", "w") as file:
                file.write(json.dumps([]))
                file.close()
        # File does exist
        return True
    # If file doesn't exist
    else:
        # Warn the user that the file doesnt exist
        print_special("warn", "Marksfile does not exist.")
        # Ask to make file
        ask_make_file = input("Would you like to make marks.json? (yes/no)\n").lower()
        # If user agrees
        if ask_make_file == "yes" or ask_make_file == "y":
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
    # Open file so it will close when function completes
    with open("marks.json", "r+") as file:
        # Parse JSON into python data
        data = json.load(file)
        # Ask for subject name
        subject_name = input("New subject name: ")
        # Ask for confirmation
        confirmation = input(f"Are you sure you want to create subject \"{subject_name}\"? (yes/no) ").lower()
        # Handle confirmation
        if confirmation == "y" or confirmation == "yes":
            pass
        # If confirmation failed
        else:
            print_special("warn", "Subject creation cancelled.")
            return
        # When confirmed add subject to marks
        data.append({"name": subject_name, "marks": []})
        # Write changes to file
        file.seek(0)
        json.dump(data, file)
        file.truncate()
        # Inform that subject was created
        print_special("inform", f"Created subject {subject_name}!")


# Deletes a subject from marks.json
def delete_subject():
    # Open file so it will close when function completes
    with open("marks.json", "r+") as file:
        # Parse JSON into python data
        data = json.load(file)
        # Address possibly empty file
        if len(data) == 0:
            print_special("error", "Empty file. Nothing to delete.")
            return
        # Print out each subject"s name
        for subject_index, subject in enumerate(data, start=1):
            print(f"({subject_index}) {subject['name']}")
        # Address case where user wants to cancel
        print_special("inform", "Enter \"0\" to cancel.")
        # Get item to delete
        try:
            subject_to_delete = int(input("Enter the number of the subject you want to delete: "))
        # Handle invalid inputs
        except ValueError:
            print_special("error", "Invalid input. Please pick from the list")
            return
        # Handle cancellation
        if subject_to_delete == 0:
            print_special("warn", "Deletion cancelled.")
            return
        # Ask for confirmation
        confirmation = input(f"Are you sure you want to delete subject {subject_to_delete}? (yes/no) ").lower()
        # Handle confirmation
        if confirmation == "y" or confirmation == "yes":
            pass
        # If confirmation failed
        else:
            print_special("warn", "Deletion cancelled.")
            return
        # Adjust for array beginning at 0
        subject_to_delete -= 1
        # Check if item_to_delete is within the list range
        if 0 <= subject_to_delete <= len(data):
            # Delete subject from list
            data.pop(subject_to_delete)
            print_special("inform", "The selected subject has been deleted.")
        # If not in range
        else:
            print_special("error", "Invalid selection.")
        # Write changes to file
        file.seek(0)
        json.dump(data, file)
        file.truncate()


# Adds a result to a subject in marks.json
def new_result():
    # Open file so it will close when function completes
    with open("marks.json", "r+") as file:
        # Parse JSON into python data
        data = json.load(file)
        # Check if there are no subjects
        subject_counter = 0
        for _, subject in enumerate(data, start=1):
            subject_counter += 1
        # If there are no subjects
        if subject_counter == 0:
            print_special("error", "No Subjects. To add a mark you must have a subject to add it to.")
            return
        # Print out each subject's name
        for subject_index, subject in enumerate(data, start=1):
            print(f"({subject_index}) {subject['name']}")
        # Address case where user wants to cancel
        print_special("inform", "Enter \"0\" to cancel.")
        # Get subject to add to
        try:
            selected_subject = int(input("Enter the number of the subject you want to add a mark to: "))
        # Handle invalid inputs
        except ValueError:
            print_special("error", "Invalid input. Please pick from the list")
            return
        if selected_subject == 0:
            print_special("warn", "Creation cancelled.")
            return
        # Adjust for array beginning at 0
        selected_subject -= 1
        # Check if selected_subject is within the list range
        if 0 <= selected_subject <= len(data):
            pass
        # Handle invalid selection
        else:
            print_special("error", "Invalid selection.")
            return
        # Loop over data to find selected_subject
        for subject_index, subject in enumerate(data):
            # Once selected_subject is found
            if subject_index == selected_subject:
                result_name = input(f"Name for new result in {subject['name']} (e.g. \"Math Final\"): ")
                # Get achieved score
                try:
                    score = float(input("Score achieved (e.g. " "\033[92m" "81" "\033[0m" "/100): "))
                # Handle invalid inputs
                except ValueError:
                    print_special("error", "Invalid input. Must be a number.")
                    return
                # Disallow negative scores
                if score < 0:
                    print_special("error", "Invalid input. Score must be 0 or higher.")
                    return
                # Get max score
                try:
                    max_score = float(input("Max score achievable (e.g. " "81/" "\033[92m" "100" "\033[0m" "): "))
                # Handle invalid inputs
                except ValueError:
                    print_special("error", "Invalid input. Must be a number.")
                    return
                # Disallow invalid score ratios
                if max_score < score:
                    print_special("error", "Invalid input. Max achieveable score must be higher than score.")
                    return
                # Add new result to marks
                subject["marks"].append({"result_name": result_name, "score": score, "max_score": max_score})
                # Write changes to file
                file.seek(0)
                json.dump(data, file)
                file.truncate()
                print_special("inform", f"{result_name} has successfully been added to {subject['name']}.")


# Display all marks across all subjects
def view_all_marks():
    # Open file so it will close when function completes
    with open("marks.json", "r") as file:
        # Parse JSON into python data
        data = json.load(file)
        # For each subject
        for subject_index, subject in enumerate(data, start=1):
            # Print subject name
            print_special("underline", f"\n{subject['name']}")
            # Check if subject marks are empty
            if len(subject['marks']) == 0:
                print("(N/A) No marks for this subject.")
                continue
            # If not empty
            for mark_index, mark in enumerate(subject['marks'], start=1):
                # Print each result in this format: (1) Math Test: 10/100 [10.00%]
                print(f"({mark_index}) {mark['result_name']}: {mark['score']}/{mark['max_score']} "
                      f"[{calculate_percentage(mark['score'], mark['max_score'])}]")
        # Print empty line for better formatting
        print("\n")


def view_subject_marks():
    # Open file so it will close when function completes
    with open("marks.json", "r") as file:
        # Parse JSON into python data
        data = json.load(file)
        # Address possibly empty file
        if len(data) == 0:
            print_special("error", "Empty file. Nothing to list.")
            return
        # Print out each subject"s name
        for subject_index, subject in enumerate(data, start=1):
            print(f"({subject_index}) {subject['name']}")
        # Address case where user wants to cancel
        print_special("inform", "Enter \"0\" to cancel.")
        # Get selected_subject
        try:
            selected_subject = int(input("Enter the number of the subject you want to list marks from: "))
        # Handle invalid inputs
        except ValueError:
            print_special("error", "Invalid input. Please pick from the list")
            return
        if selected_subject == 0:
            print_special("warn", "Mark viewing cancelled.")
            return
        # Adjust for array beginning at 0
        selected_subject -= 1
        # Print subject name
        print_special("underline", f"\n{subject['name']}")
        # Loop over subjects to find correct one
        for subject_index, subject in enumerate(data):
            # If current subject is correct
            if subject_index == selected_subject:
                # Check if subject marks are empty
                if len(subject['marks']) == 0:
                    print("(N/A) No marks for this subject.")
                    # Skip current and move to next subject
                    continue
                # If not empty
                for mark_index, mark in enumerate(subject['marks'], start=1):
                    # Print each result in this format: (1) Math Test: 10/100 [10.00%]
                    print(f"({mark_index}) {mark['result_name']}: {mark['score']}/{mark['max_score']} "
                          f"[{calculate_percentage(mark['score'], mark['max_score'])}]")
        # Print empty line for better formatting
        print("\n")


def get_action():
    # List actions
    print("(0) Exit Markinator\n"
          "(1) Make a new subject\n"
          "(2) Delete a subject\n"
          "(3) Add new result\n"
          "(4) Delete a result\n"
          "(5) View all marks\n"
          "(6) View subject marks\n"
          )
    try:
        # Get selected action
        action = int(input("Select an action: "))
    # Handle invalid inputs
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
        new_result()
    elif action == 5:
        view_all_marks()
    elif action == 6:
        view_subject_marks()
    # Handle invalid actions
    else:
        print_special("error", "Invalid input. Please pick from the list")
        return
    return


# Main application loop
def main():
    # Welcome text!
    print_special("underline", "Welcome to Markinator!\n")
    # If marksfile cannot be loaded
    if not marksfile_exists():
        print_special("error", "Cannot load marks.json. File does not exist.")
        exit()
    # Loop action selection until program exited
    while True:
        get_action()


# Run the program
main()
