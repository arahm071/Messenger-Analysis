# Standard library imports
import json              # Provides methods for working with JSON data
import os                # For interacting with the operating system
import glob              # To find all the pathnames matching a specified pattern

# Third-party imports
import pandas as pd      # Popular data manipulation and analysis library for Python
import emoji             # Library to work with and process emojis in text data

# Local application imports
from . import chat_features     # Module for handling specific chat features


def chat_db(json_file):
    """
    Reads and processes a JSON file containing chat data, converting it into a pandas DataFrame.

    The function opens the specified JSON file, extracts chat messages and metadata, and 
    transforms this information into a structured DataFrame. It also adjusts the timestamp 
    to the 'America/Toronto' timezone.

    Parameters:
    json_file (str): The file path to the JSON file containing chat data.

    Returns:
    DataFrame: A pandas DataFrame containing the processed chat logs, with the chat name as the index name.
    """
    # Open and read the JSON file
    with open(json_file, "r") as read_file:
        data = json.load(read_file)

    # Extract messages and chat name from the JSON data
    messages = data.get("messages")
    chat_name = data.get("title")

    # Convert the messages list to a pandas DataFrame
    chat_logs = pd.DataFrame(messages)

    # Set the DataFrame index name to the chat name
    chat_logs.index.name = chat_name

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


def clean_messages(directory):
    """
    Processes and cleans messages from multiple folders within a directory.

    This function normalizes the path to the directory, extracts messages from all JSON files, and performs 
    various cleaning operations like dropping specific columns, converting timestamps to human-readable dates 
    and times, and renaming columns. It also sorts messages and computes additional features like word count 
    and emoji count.

    Parameters:
    directory (str): The path to the parent directory containing multiple folders.

    Returns:
    DataFrame: A pandas DataFrame containing cleaned and sorted messages from all the folders.
    """
    # Normalize the directory path for consistency
    normalized_directory = os.path.normpath(directory)

    # Extract messages from all folders in the directory
    cleaned_df = all_messages(normalized_directory)

    # Retrieve the chat name from the DataFrame's index name
    chat_name = cleaned_df.index.name

    # Retain rows where columns indicating photos, shares, etc. are all NaN.
    # This ensures we keep only rows with textual content or call duration information.
    retain_columns = ["sender_name", "timestamp_ms", "content", "call_duration"]
    purge_columns = [col for col in cleaned_df.columns if col not in retain_columns]

     # Keep rows with all NaN values in identified columns
    cleaned_df = cleaned_df[cleaned_df[purge_columns].isna().all(axis=1)]

    # Convert 'timestamp_ms' to date and time formats
    cleaned_df['Date'] = pd.to_datetime(cleaned_df['timestamp_ms']).dt.date # 'mm-dd-yyyy'
    cleaned_df['Time'] = pd.to_datetime(cleaned_df['timestamp_ms']).dt.time # 'hh:mm:ss:ffffff AM/PM'

    # Rename columns for clarity
    cleaned_df.rename(columns={"sender_name": "Sender", "content": "Message"}, inplace=True)

    # Rename and rearrange columns if 'call_duration' exists
    if "call_duration" in cleaned_df.columns:
        cleaned_df.rename(columns={"call_duration": "Call Duration (Sec)"}, inplace=True)
        column_order = ["Sender", "timestamp_ms", "Date", "Time", "Message", "Call Duration (Sec)"]
    else:
        column_order = ["Sender", "timestamp_ms", "Date", "Time", "Message"]

    cleaned_df = cleaned_df[column_order]

    # Drop rows with NaN in 'Message' and sort by 'timestamp_ms'
    cleaned_df = cleaned_df.dropna(subset=["Message"])
    cleaned_df = cleaned_df.sort_values("timestamp_ms", ascending=True)

    # Apply functions to process emojis and word count
    cleaned_df['Message'] = cleaned_df['Message'].apply(chat_features.unicode_emoji_converter)
    cleaned_df["Word Count"] = cleaned_df["Message"].map(chat_features.word_count)

    # Additional processing for 'Call Duration (Sec)' and 'Word Count'
    if "Call Duration (Sec)" in cleaned_df.columns:
        cleaned_df = cleaned_df[cleaned_df["Call Duration (Sec)"] != 0]
        mask = cleaned_df["Call Duration (Sec)"] >= 0
        cleaned_df.loc[mask, "Word Count"] = 0

    # Exclude word count for messages containing URLs
    mask_url = cleaned_df['Message'].str.contains('http')
    cleaned_df.loc[mask_url, "Word Count"] = 0

    # Add 'Emoji Count' column
    cleaned_df['Emoji Count'] = cleaned_df['Message'].apply(emoji.emoji_count)

    # Reset and adjust the DataFrame index
    cleaned_df.reset_index(drop=True, inplace=True)
    cleaned_df.index += 1
    cleaned_df.index.name = chat_name

    return cleaned_df