# Standard library imports
import json              # Provides methods for working with JSON data
import os                # For interacting with the operating system
import glob              # To find all the pathnames matching a specified pattern

# Third-party imports
import pandas as pd      # Popular data manipulation and analysis library for Python
import emoji             # Module for working with and processing emojis

# Local application imports
import chat_features     # Module for handling specific chat features


def chat_db(json_file):
    """
    Reads and processes a JSON file containing chat data, converting it into a pandas DataFrame.

    This function opens the specified JSON file, extracts chat messages and metadata, and 
    transforms this information into a structured DataFrame. It also adjusts the timestamp 
    to the 'America/Toronto' timezone.

    Parameters:
    json_file (str): The file path to the JSON file containing chat data.

    Returns:
    DataFrame: A pandas DataFrame containing the processed chat logs, with the chat name as an additional column.
    """
    # Open and read the JSON file
    with open(json_file, "r") as read_file:
        data = json.load(read_file)

    # Extract messages and chat name from the JSON data
    messages = data.get("messages")
    chat_name = data.get("title")

    # Convert the messages list to a pandas DataFrame
    chat_logs = pd.DataFrame(messages)

    # Add a column for the chat name
    chat_logs["Title"] = chat_name

    # Convert 'timestamp_ms' to datetime and adjust for 'America/Toronto' timezone
    chat_logs['timestamp_ms'] = (
        pd.to_datetime(chat_logs['timestamp_ms'], unit='ms', utc=True)
        .map(lambda x: x.tz_convert('America/Toronto'))
    )

    return chat_logs


def all_messages(directory):
    """
    Loads and combines messages from multiple JSON files within a given directory.

    This function iterates through all JSON files in the specified directory, extracting 
    chat data from each file using the chat_db function. It then consolidates this data 
    into a single pandas DataFrame.

    Parameters:
    directory (str): The path to the directory containing the JSON files.

    Returns:
    DataFrame: A pandas DataFrame containing the combined messages from all JSON files in the directory.
    """
    # Normalize the directory path for consistency
    normalized_directory = os.path.normpath(directory)

    # Define the file pattern for JSON files in the directory
    json_pattern = os.path.join(normalized_directory, '*.json')

    # Gather a list of all JSON files in the directory
    file_list = glob.glob(json_pattern)

    # Initialize an empty list to hold DataFrames from each JSON file
    dfs = []

    # Loop through each JSON file and process the chat data
    for file in file_list:
        chat_data = chat_db(file)
        dfs.append(chat_data)

    # Combine all individual DataFrames into one
    combined_messages = pd.concat(dfs)

    return combined_messages


def all_folder(directory):
    """
    Processes and combines messages from multiple folders within a directory.

    This function iterates through each folder in the specified directory, using the 
    all_messages function to extract and combine chat data from JSON files in each folder. 
    The resulting data from all folders is then merged into a single pandas DataFrame.

    Parameters:
    directory (str): The path to the parent directory containing multiple folders.

    Returns:
    DataFrame: A pandas DataFrame containing the combined and sorted messages from all the folders.
    """
    # Normalize the directory path for consistency
    normalized_directory = os.path.normpath(directory)

    # Initialize an empty list to hold DataFrames from each folder
    df_list = []

    # Loop through each folder in the normalized directory
    for folder_name in os.listdir(normalized_directory):
        folder_path = os.path.join(directory, folder_name)
        
        # Check if the current path is a directory
        if os.path.isdir(folder_path):
            # Extract messages from the folder and append to the DataFrame list
            folder_data = all_messages(folder_path)
            df_list.append(folder_data)

    # Combine all DataFrames from different folders into one
    total_messages = pd.concat(df_list)

    return total_messages


def clean_messages(directory):
    """
    Cleans and processes messages from multiple folders within a directory.

    This function compiles chat data from multiple folders, then cleans and processes the data. 
    It includes operations like dropping specific rows, converting timestamps to human-readable dates 
    and times, renaming columns, sorting the messages, and computing word and emoji counts.

    Parameters:
        directory (str): The path to the parent directory containing multiple folders.

    Returns:
        DataFrame: A pandas DataFrame containing the cleaned and sorted messages from all the folders.
    """
    # Normalize the directory path
    normalized_directory = os.path.normpath(directory)

    # Combine messages from all folders into a single DataFrame
    cleaned_df = all_folder(normalized_directory)

    # Retain rows where columns indicating photos, shares, etc. are all NaN.
    # This ensures we keep only rows with textual content or call duration information.
    retain_columns = ["sender_name", "timestamp_ms", "content", "call_duration", 'Title']
    purge_columns = [col for col in cleaned_df.columns if col not in retain_columns]

     # Keep rows with all NaN values in identified columns
    cleaned_df = cleaned_df[cleaned_df[purge_columns].isna().all(axis=1)]

    # Convert 'timestamp_ms' to date and time formats
    cleaned_df['Date'] = pd.to_datetime(cleaned_df['timestamp_ms']).dt.date #'mm-dd-yyyy'
    cleaned_df['Time'] = pd.to_datetime(cleaned_df['timestamp_ms']).dt.time #'hh:mm:ss:ffffff AM/PM'

    # Rename columns for clarity
    cleaned_df.rename(columns={"sender_name": "Sender", "content": "Message", "call_duration": "Call Duration (Sec)"}, inplace=True)

    # Rearrange columns in the specified order
    column_order = ["Sender", "Title", "timestamp_ms", "Date", "Time", "Message", "Call Duration (Sec)"]
    cleaned_df = cleaned_df[column_order]

    # Drop rows with NaN in 'Message' and sort by 'Date' and 'Time'
    cleaned_df.dropna(subset=["Message"], inplace=True)
    cleaned_df.sort_values(by=["Date", "Time"], ascending=[True, True], inplace=True)

    # Process message content and compute word and emoji counts
    cleaned_df['Message'] = cleaned_df['Message'].apply(chat_features.unicode_emoji_converter)
    cleaned_df["Word Count"] = cleaned_df["Message"].map(chat_features.word_count)

    # Filter out rows with zero call duration
    cleaned_df = cleaned_df[cleaned_df["Call Duration (Sec)"] != 0]

    # Reset word count for messages with non-zero call duration or containing URLs
    mask_call_duration = cleaned_df["Call Duration (Sec)"] >= 0
    mask_url = cleaned_df['Message'].str.contains('http')
    cleaned_df.loc[mask_call_duration, "Word Count"] = 0
    cleaned_df.loc[mask_url, "Word Count"] = 0

    # Compute emoji count
    cleaned_df['Emoji Count'] = cleaned_df['Message'].apply(emoji.emoji_count)

    # Reset and adjust the DataFrame index
    cleaned_df.reset_index(drop=True, inplace=True)
    cleaned_df.index += 1

    return cleaned_df