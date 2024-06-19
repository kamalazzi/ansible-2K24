#!/usr/bin/env bash

# Get the current working directory
NEW_HOME=$HOME

# Define the paths to the files that need to be modified
FILES=(
    "$HOME/automation/bin/flask"
    "$HOME/automation/bin/gunicorn"
    "$HOME/automation/bin/pip"
)

# Loop through each file and modify the shebang line
for FILE_PATH in "${FILES[@]}"; do
    # Check if the file exists
    if [[ -f "$FILE_PATH" ]]; then
        # Extract the script name from the file path (e.g., flask, gunicorn, pip)
        SCRIPT_NAME=$(basename "$FILE_PATH")

        # Check if the script name is 'flask', 'gunicorn', or 'pip'
        if [[ "$SCRIPT_NAME" == "flask" || "$SCRIPT_NAME" == "gunicorn" || "$SCRIPT_NAME" == "pip" ]]; then
            # Define the new shebang line with /python3 for flask, gunicorn, and pip
            NEW_SHEBANG="#!${NEW_HOME}/automation/bin/python3"
        else
            # Define the new shebang line for other scripts
            NEW_SHEBANG="#!${NEW_HOME}/automation/bin/${SCRIPT_NAME}"
        fi

        # Read the first line of the file
        FIRST_LINE=$(head -n 1 "$FILE_PATH")

        # Check if the first line starts with '#!'
        if [[ "$FIRST_LINE" == \#!* ]]; then
            # Replace the shebang line
            sed -i "1s|.*|$NEW_SHEBANG|" "$FILE_PATH"
            echo "Shebang line in $FILE_PATH modified successfully."
        else
            echo "The first line of $FILE_PATH does not appear to be a shebang line."
        fi
    else
        echo "File $FILE_PATH does not exist."
    fi
done
