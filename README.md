# Markinator

Term 1's Software Engineering assignment.

View the full project at https://github.com/jridz/Markinator

## Description

A simple command line application for recording, viewing, and managing results for assignments and tests.

## Requirements

1. Data entry
    - Allow users to enter results into the application.
2. Viewing results
    - Results can be viewed in a readable way.
3. Managing results
    - Allow users to delete results which may be incorrect or no longer needed.
4. File saving
    - Allow marks to be saved in a file that can be backed up or sent by the user.
5. Readable notices
    - Make errors, warnings, notices, and other important messages obvious and readable to the user.

## Inputs, Processes & Outputs

### Inputs

- Selected action
- Confirmations
- Subject name
- Selected subject
- Result name
- Score achieved
- Maximum possible score

### Processes

- Open/Close File
- Parse JSON from file
- Handle selected action
- Handle user confirmation
- Create warnings, errors, and notices
- Alter data to reflect changes (creations, additions, or deletions)
- Write changes
- Make lists of subjects and results
- Handle incorrect selections and data entries

### Outputs

- Welcome message
- Warnings, errors, and notices
- Lists of subjects and results
- Thank You message

## Data Types

### Data types used

1. Integers (int)
2. Floating point nubers (float)
3. Strings (str)
4. Boolean (bool)
5. List/Array (list)
6. None (None)
7. JSON/Dictionary

## Debugging Tools

### Breakpoints

I used breakpoints to investingate the values of the program mid-execution. I used breakpoints to do the following:

- Fix incorrect starting iteration values in for loops.
- Find where data was in lists and how to parse the data.
- Stop before errors so I could diagnose.

### Single Line Stepping

I used single line stepping to figure out what order functions were running in. I used single line stepping to do the
following:

- Find why loops were/weren't looping infinitely.
- Look at how data was changing after each step taken.
- Go line by line to check for incorrect iteration or variable types.

### Error Messages
I used Python's error messages to find many things _(mostly spelling mistakes)_. It was a useful tool as it showed me when I was:
- Inputting the incorrect data into function arguments.
- Referencing variables that didnt't exist within the current function.
- Using the incorrect data types.

### Special Print Messages
I made my own function `print_special()` which I use to notify the user when certain things happen. I also used them a fair amount as a way to debug.
The function is often triggered when I enter incorrect data into the program. I used them to check if incorrect data was being handled correctly.

An example of where I used them was when you are entering in a result's score. Since errors wouldn't be triggered if the data is correct,
I checked for data the should be errored by using the fact that the errors wouldn't trigger.

## Errors
### Function stopping unexpectedly
In the `view_result()` function there was the following code:
```python
# For each subject
for subject_index, subject in enumerate(data, start=1):
    # Print subject name
    print_special("underline", f"\n{subject['name']}")
    # Check if subject marks are empty
    if len(subject['marks']) == 0:
        print("(N/A) No marks for this subject.")
        # Skip current and move to next subject
        break
    # If not empty
    for mark_index, mark in enumerate(subject['marks'], start=1):
        # Print each result in this format: (1) Math Test: 10/100 [10.00%]
        print(f"({mark_index}) {mark['result_name']}: {mark['score']}/{mark['max_score']} "
              f"[{calculate_percentage(mark['score'], mark['max_score'])}]")
```
I was confused because if it was an empty it showed an error which was correct, but it wouldn't display the other following subjects which were correct.
I threw in a breakpoint on the for loop and went step-by-step to see exactly why the function would quit before finishing.
I eventually got to the line that has `break`, then immediatley after the for loop stopped and function ended.
After looking into what `break` does I realised that I shouldn't have been using `break`.
Instead I should have been using `continue` so it stops the current iteration in the loop then continues onto the next instead of breaking the loop.

After fixing the mistake I ended up with the following fixed code:
```python
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
```
