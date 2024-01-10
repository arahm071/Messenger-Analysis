# Standard library imports
import os              # Provides a way of using operating system dependent functionality
import re              # Allows regular expression operations
import sys             # Provides access to some variables used or maintained by the interpreter

# Third-party imports
import pandas as pd    # Data manipulation and analysis library
from fuzzywuzzy import fuzz     # String matching library
from thefuzz import process     # Another part of the string matching library, used for process-based functions

# Local application imports
import chat_processing.single_folder as single_folder  # Local module for processing single chat folder
import chat_processing.all_folders as all_folders      # Local module for processing all chat folders
import chat_processing.chat_features as chat_features  # Local module for various chat features analysis


def save_file_path(file_path):
    """
    Saves the specified file path to a text file for later retrieval.

    This function writes the provided file path to a text file named 'saved_file_path.txt'.
    It's useful for persisting a file path across sessions or for logging purposes.

    Parameters:
    file_path (str): The file path to be saved.

    Returns:
    None: The function writes to a file but does not return any value.
    """
    # Open a text file in write mode
    with open('saved_file_path.txt', 'w') as file:
        # Write the file path to the text file
        file.write(file_path)


def load_file_path():
    """
    Loads the previously saved file path from a text file.

    This function attempts to read a file path from a text file named 'saved_file_path.txt'.
    If the file exists and contains a path, it returns the path. If the file does not exist,
    the function returns None.

    Returns:
    str or None: The file path stored in 'saved_file_path.txt', or None if the file does not exist.
    """
    try:
        # Attempt to open the file and read the saved path
        with open('saved_file_path.txt', 'r') as file:
            return file.read().strip()  # Strip to remove any leading/trailing whitespace
    except FileNotFoundError:
        # Return None if the file is not found
        return None


def prompt_for_new_path():
    """
    Prompts the user to enter a new file path until a valid path is provided.

    The function repeatedly asks the user to input a file path. Once a valid path is entered 
    (i.e., the path exists), it saves the path using the 'save_file_path' function and returns it. 
    If an invalid path is entered, it prompts the user again.

    Returns:
    str: The validated file path entered by the user.
    """
    while True:
        # Prompt the user to enter a file path
        file_path = input("\nEnter new file path: ").strip()

        # Check if the entered path exists
        if os.path.exists(file_path):
            # Save the valid file path and return it
            save_file_path(file_path)
            return file_path
        else:
            # Inform the user if the path is invalid and prompt again
            print("\nInvalid file path. Please enter a valid path.\n")


def get_user_permission():
    """
    Asks the user for permission to proceed with changes.

    This function prompts the user to agree or disagree with proceeding with certain changes. 
    It continues to ask until a valid response ('yes', 'y', 'no', 'n') is provided.

    Returns:
    str: The user's response indicating consent ('yes' or 'y') or denial ('no' or 'n').
    """
    while True:
        # Ask the user for permission to proceed
        permission = input("We're planning to update the naming convention of folders for better readability. Do you agree to proceed with these changes? (yes/no): ").lower()

        # Check if the response is one of the accepted answers
        if permission in ['yes', 'y', 'no', 'n']:
            # Return the user's response
            return permission
        else:
            # Prompt the user to enter a valid response
            print("\nPlease enter 'yes' or 'no'.\n")


def rename_folders(directory):
    """
    Renames folders within the given directory. 
    Each folder name is simplified by removing characters after an underscore. 
    If the base name (before the underscore) is the same as the previous folder's, 
    a hyphen is appended to ensure uniqueness.

    Parameters:
    directory (str): The path to the directory containing folders to be renamed.

    Returns:
    None: The function renames folders but does not return a value.
    """
    # Normalize the directory path for consistency
    normalized_directory = os.path.normpath(directory)
    
    # Change the current working directory to the specified directory
    os.chdir(normalized_directory)

    # Keep track of the last renamed folder's base name for uniqueness
    previous_name = ""

    # List all items in the directory
    all_items = os.listdir(normalized_directory)

    # Iterate over each item in the directory
    for item in all_items:
        # Split the item's name at the underscore
        split_name = re.split("\_", item)

        # Check if the name split into two parts
        if len(split_name) == 2:
            base_name = split_name[0]

            # Rename the folder with the base name if it's different from the previous one
            if previous_name != base_name:
                os.rename(item, base_name)
                previous_name = base_name
            # Append a hyphen to the base name if it's the same as the previous one
            else:
                new_name = base_name + "-"
                os.rename(item, new_name)
                previous_name = new_name


def chat_analysis(directory, entire=False):
    """
    Performs chat analysis based on user-selected features within a specified directory.

    The function allows the user to choose from a variety of analysis options, including general statistics, 
    top words, top emojis, message distribution, and more. The user can also output the data to a CSV file, 
    choose another folder for analysis, or exit the program.

    Parameters:
    directory (str): The path to the directory containing chat data.
    entire (bool): Flag to indicate whether to analyze all folders (True) or a single folder (False).
    """
    # Load and clean messages from the entire directory or a single folder
    if entire:
        df = all_folders.clean_messages(directory)
    else:
        df = single_folder.clean_messages(directory)

    # Define the analysis options available to the user
    choices = ['General Message Stats', 'Top Words Used', 'Top Emojis Used', 'Total Message Distribution',
               'Total Message Frequency', 'Output csv of df', 'Choose Another Folder', 'Exit']
    options = {count: choice for count, choice in enumerate(choices, start=1)}

    while True:
        # Display the analysis options to the user
        for key, value in options.items():
            print(f'{key}. {value}')

        # Handle user input for selecting an option
        try:
            num_input = int(input("\nPlease input the number of the chat feature you want to see: "))
            print('')

            # Process the selected option
            if num_input in options:
                if num_input == 8:
                    print('Goodbye\n')
                    sys.exit()  # Exit the program if user selects 'Exit'

                elif num_input == 7:
                    return  # Return to the previous menu

                elif num_input == 6:
                    # Output the data to a CSV file
                    output = os.path.join(directory, f'{os.path.basename(directory)}.csv')
                    df.to_csv(output)
                    print(f'\nThe csv file has been outputted within {directory} under the file name {os.path.basename(directory)}.csv\n')

                elif num_input == 5:
                    # Display total message frequency analysis
                    print('\nLook at the plot\n')
                    chat_features.total_message_frequency(df)

                elif num_input == 4:
                    # Display total message distribution analysis
                    print('\nLook at the plot\n')
                    chat_features.plot_message_distribution(df)

                elif num_input == 3:
                    # Display top emojis used in the chat
                    print('\nHere are the chat\'s top emojis:\n')
                    print(chat_features.plot_top(df, top_type='emojis'))
                    print('')

                elif num_input == 2:
                    # Display top words used in the chat
                    print('\nHere are the chat\'s top words:\n')
                    print(chat_features.plot_top(df, top_type='words'))
                    print('')

                elif num_input == 1:
                    # Display general message statistics
                    print('\nHere are the chat\'s stats:\n')
                    print(chat_features.message_stats(df))
                    print('')

                print("Please Choose Another Option:")

            else:
                print("\nPlease choose a valid number from the list.\n")

        except ValueError:
            print("\nInvalid input. Please enter a number.\n")


def call_folder(directory):
    """
    Interactively prompts the user to select a chat folder for analysis within a given directory.

    This function lists all folders in the specified directory and allows the user to choose a folder by name,
    analyze all folders, or exit the program. If a specific folder name is provided, it uses fuzzy matching 
    to suggest the closest folder names. The user can then select a folder for further analysis.

    Parameters:
    directory (str): The path to the directory containing chat folders.
    """
    # Normalize the directory path for uniformity across different OS
    normalized_directory = os.path.normpath(directory)

    while True:  # Start of the user interaction loop
        # Retrieve the list of folder names in the directory
        folder_names = os.listdir(normalized_directory)

        # Request user input for a chat name or option
        name_input = input("Whose chat do you want to analyze (type 'exit' to quit): ").lower().replace(" ", "")

        # Handle the 'exit' input to terminate the function
        if name_input == 'exit':
            print('\nGoodbye\n')
            sys.exit()  # Exit the program

        # Handle the 'all' input to analyze all chats
        if name_input == 'all':
            chat_analysis(normalized_directory, entire=True)
        else:
            # Use fuzzy matching for the folder names based on user input
            guesses = process.extract(name_input, folder_names, scorer=fuzz.ratio, limit=10)
            # Create a dictionary of potential matches with a score of 50 or above
            guesses = {count: guess[0] for count, guess in enumerate(guesses, start=1)}

            # Add an option for the user to exit the selection
            guesses[len(guesses) + 1] = 'Exit'
            # Display the list of matching folders for user selection
            for key, value in guesses.items():
                print(f'{key}. {value}')

            # Loop to handle the user's selection of a folder
            while True:
                try:
                    num_input = int(input("\nPlease input the number of the chat you want to analyze: "))
                    print('')
                    # Process the user's selection
                    if num_input in guesses:
                        if num_input == len(guesses):
                            print('Goodbye\n')
                            sys.exit()  # Exit the program if the user selects 'Exit'
                        else:
                            # Conduct chat analysis on the selected folder
                            selected_folder = guesses.get(num_input)
                            path = os.path.join(normalized_directory, selected_folder)
                            chat_analysis(path)
                            break  # Exit the loop once a valid selection is made
                    else:
                        print("\nPlease choose a valid number from the list.\n")
                except ValueError:
                    print("\nInvalid input. Please enter a number.\n")

        print("\nReturning to folder selection...\n")


def main():
    """
    Main function to handle file path input, user permissions, and subsequent actions.

    This function performs several steps:
    1. Loads a previously saved file path (if available).
    2. Prompts the user to use the saved path or enter a new one.
    3. Asks the user for permission to proceed with renaming folders.
    4. Based on user input, either proceeds with renaming folders and calling the folder analysis function, or exits.

    Note: The function utilizes other functions like load_file_path, prompt_for_new_path, get_user_permission, rename_folders, and call_folder.
    """
    # Load the previously saved file path, if it exists
    saved_file_path = load_file_path()

    # Determine whether to use a saved file path or to prompt for a new one
    if saved_file_path:
        # Interact with the user to confirm using the saved file path
        use_saved = input(f"Found a saved file path: {saved_file_path}. Do you want to use this path? (yes/no): ").lower()
        while use_saved not in ['yes', 'y', 'no', 'n']:
            print("\nPlease enter 'yes' or 'no'.\n")
            use_saved = input("Do you want to use this path? (yes/no): ").lower()

        # Choose the file path based on the user's decision
        file_path = saved_file_path if use_saved in ['yes', 'y'] else prompt_for_new_path()
    else:
        # Prompt for a new path if no saved path is found
        file_path = prompt_for_new_path()

    # Confirm the file path being used
    print(f"\nUsing file path: {file_path}\n")

    # Request user permission to proceed with folder renaming
    permission = get_user_permission()

    # Execute actions based on the user's permission
    if permission in ['no', 'n']:
        print("\nNo changes will be made to your folder names.\n")
    elif permission in ['yes', 'y']:
        print("\nYou agreed to proceed with the changes.\n")
        # Rename folders and then call the folder analysis function
        rename_folders(file_path)
        print("Folder names have been updated.\n")
        # Initiate chat folder analysis process
        call_folder(file_path)


# Ensure the main function is executed when the script runs
if __name__ == "__main__":
    main()






















        






