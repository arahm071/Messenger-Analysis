# Standard library imports
import string              # For common string operations
import re                  # Allows regular expression operations
from collections import Counter  # Provides a container to store elements as dictionary keys and their counts as dictionary values

# Third-party imports
import pandas as pd        # Data manipulation and analysis library, particularly useful for working with structured data
import numpy as np         # Library for numerical computing
import matplotlib.pyplot as plt  # Plotting library for creating static, animated, and interactive visualizations
import seaborn as sns      # Data visualization library based on matplotlib, provides a high-level interface for drawing attractive and informative statistical graphics
import emoji               # Library to work with and process emojis in text data


def unicode_emoji_converter(unicode_str):
    """
    Convert a Unicode string to a UTF-8 encoded string.

    This function encodes a given Unicode string using 'latin1' encoding
    and then decodes it back using 'utf8' encoding. This can be useful
    for handling certain types of emoji or character encoding issues.

    Parameters:
    unicode_str (str): The Unicode string to be converted.

    Returns:
    str: The converted string in UTF-8 encoding.
    """
    # Convert the string from 'latin1' encoding to 'utf8' encoding
    converted_str = unicode_str.encode('latin1').decode('utf8')

    return converted_str


def get_emoji_regexp():
    """
    Compile and return a regular expression to match emojis.

    The function sorts the emojis by length in descending order to ensure
    that multi-character emojis are matched before single-character ones.
    This is important for accurate pattern matching in strings containing
    emojis.

    Returns:
    re.Pattern: A compiled regular expression for matching emojis.
    """
    # Sort emojis by length to ensure multi-character emojis are matched first
    emojis = sorted(emoji.EMOJI_DATA, key=len, reverse=True)

    # Create a regular expression pattern by joining sorted emojis
    pattern = '(' + '|'.join(re.escape(u) for u in emojis) + ')'

    # Compile and return the regular expression pattern
    return re.compile(pattern)


def keep_only_emojis(text):
    """
    Extract and return only the emojis from a given text string.

    This function uses a regular expression to find all emojis in the
    provided text. Non-emoji characters are ignored, and only emoji
    characters are included in the returned list.

    Parameters:
    text (str): The text from which emojis are to be extracted.

    Returns:
    list: A list of all emojis found in the input text.
    """
    # Obtain the emoji regular expression pattern
    exp = get_emoji_regexp()

    # Find and return all emojis in the text
    return exp.findall(string=text)


''' # ! def double_check_emoji(row):
    """
    Check if the emoji in the given row is a valid emoji.

    This function checks whether the 'Emoji' field of the input row
    is present in the emoji.EMOJI_DATA, which is assumed to be a collection
    of valid emojis.

    Parameters:
    row (dict): A dictionary or similar data structure that contains
                an 'Emoji' key.

    Returns:
    bool: True if the 'Emoji' is in emoji.EMOJI_DATA, False otherwise.
    """
    # Check if the Emoji in the row is in the list of valid emojis
    return row['Emoji'] in emoji.EMOJI_DATA
'''


def words_without_punctuation(text):
    """
    Remove punctuation from the given text and return the modified text.

    This function creates a translation table that maps each punctuation
    character to None (effectively removing it). It then uses this table
    to translate the provided text, removing all punctuation.

    Parameters:
    text (str): The input text from which punctuation is to be removed.

    Returns:
    str: The text with punctuation removed.
    """
    # Create a translation table for removing punctuation
    translation_table = str.maketrans('', '', string.punctuation)
    
    # Remove punctuation from the text using the translation table
    text_without_punctuation = text.translate(translation_table)

    return text_without_punctuation


def prep_text(s, cap=True):
    """
    Prepare the text by capitalizing and removing non-alphanumeric characters.

    This function first capitalizes the first letter of each word if 'cap' is True.
    It then removes all non-alphanumeric characters, including emojis, from the text.
    The processed text is split into words and returned as a list.

    Parameters:
    s (str): The input string to be processed.
    cap (bool): If True, capitalizes each word in the string. Default is True.

    Returns:
    list: A list of processed words from the input string.
    """
    if cap:
        # Capitalize each word
        s = re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                   lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(), s)

    # Remove non-alphanumeric characters, including emojis
    s = re.sub(r'[^\w\d\s\']+', '', s)

    # Split into words and return the list
    return s.split()


def word_count(s):
    """
    Count the number of words in a given string, excluding emojis.

    This function processes the input string using the 'prep_text' function
    to remove non-alphanumeric characters (including emojis) and then splits
    the processed string into words. The function counts and returns the number
    of words in the processed string.

    Parameters:
    s (str): The input string to be analyzed.

    Returns:
    int: The total number of words in the processed input string.
    """
    # Process the string to remove non-alphanumeric characters (including emojis)
    # and split it into words
    words_split = prep_text(s, cap=False)

    # Count and return the number of words in the processed string
    return len(words_split)


def message_stats(df_m_s):
    """
    Calculate message statistics for each sender in a DataFrame.

    The function preprocesses the messages to exclude those containing URLs
    and to remove non-alphanumeric characters (including emojis). It then
    calculates the count of messages and the sum of word counts for each sender.
    If present, it also calculates the sum of call durations.

    Parameters:
    df_m_s (DataFrame): DataFrame containing messages and sender information.

    Returns:
    DataFrame: A DataFrame containing message statistics grouped by sender. 
    """
    # Exclude messages containing URLs
    df_m_s = df_m_s[~df_m_s['Message'].str.contains('http')].copy()

    # Preprocess messages: remove non-alphanumeric characters (including emojis) and split into words 
    df_m_s['Message'] = df_m_s['Message'].apply(prep_text, cap=False)

    # Join the list of words back into a string
    df_m_s['Message'] = df_m_s['Message'].apply(lambda x: ' '.join(x))

    if "Call Duration (Sec)" in df_m_s.columns:
        # Calculate call duration sum for each sender
        call_sum = df_m_s.groupby("Sender").agg({"Call Duration (Sec)": "sum"})

        # Exclude rows where call duration is greater than 0 to prevent phrases like
        # 'You called _____' from being counted as messages in the word count and message count
        df_m_s = df_m_s[~(df_m_s['Call Duration (Sec)'] > 0)].copy()

        # Calculate message count and word count sum for each sender
        rest_agg = df_m_s.groupby("Sender").agg({"Message": "count", "Word Count": "sum"})

        # Combine message and call duration statistics
        stats_df = rest_agg.copy()
        stats_df["Call Duration (Sec)"] = call_sum["Call Duration (Sec)"]

    else:
        # Calculate statistics without "Call Duration (Sec)" column
        stats_df = df_m_s.groupby("Sender").agg({"Message": "count", "Word Count": "sum"})

    # Create a total row and concatenate it to the DataFrame
    total_row = pd.DataFrame(stats_df.agg(["sum"])).rename(index={"sum": "Total"})
    stats_df = pd.concat([stats_df, total_row])

    return stats_df


def top_words(df_t_w):
    """
    Identifies and returns a DataFrame of the most frequent words used by each sender in the 
    provided DataFrame, excluding predefined stop words.

    The function preprocesses the messages by removing URLs, call log entries, 
    non-alphanumeric characters (including emojis), and then analyzes the frequency 
    of each word used by the senders, excluding common stop words.

    Parameters:
    df_t_w (DataFrame): DataFrame containing 'Message' and 'Sender' columns.

    Returns:
    DataFrame: A DataFrame containing the top words used by each sender, 
               along with their counts.
    """
    # Define a list of stop words
    stop_words = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
    'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
    'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 
    'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 
    'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 
    'wasn', 'weren', 'won', 'wouldn', 'ur', 'u', 'r', 'c', 'k', 'b', 'n', 'ppl', 'btw', 'cuz', 
    'bc', 'dm', 'kk', 'wat', 'ok', 'yeah', 'im', 'like'
    ]


    # Capitalize stop words for consistency in comparison
    stop_words = [word.title() for word in stop_words]

    # Preprocess messages: remove URLs and call logs
    df_t_w = df_t_w[~df_t_w['Message'].str.contains('http')].copy()  # Remove messages containing URLs
    df_t_w = df_t_w[~(df_t_w['Call Duration (Sec)'] > 0)].copy()     # Exclude call logs

    # Apply text processing functions to clean 'Message' column
    df_t_w['Message'] = df_t_w['Message'].apply(words_without_punctuation)  # Remove punctuation
    df_t_w['Message'] = df_t_w['Message'].apply(prep_text)       # Process text and remove emojis

    # Initialize a Counter for each unique sender
    most_words = {s: Counter() for s in df_t_w["Sender"].unique()}

    # Count word occurrences for each sender
    for x in df_t_w.index:
        most_words[df_t_w["Sender"][x]].update(df_t_w["Message"][x])

    # Remove stop words from the Counters
    for k, v in most_words.items():
        for stop in stop_words:
            v.pop(stop, None)

    # Convert the Counters into a DataFrame
    top_words_df = pd.DataFrame(most_words).reset_index()
    top_words_df = pd.melt(top_words_df, id_vars=['index'], value_vars=df_t_w["Sender"].unique())
    top_words_df = top_words_df.rename(columns={"index": "Word", "variable": "Sender", "value": "Count"})

    # Clean up the DataFrame: drop NaNs, sort, and reset index
    top_words_df = top_words_df.dropna(subset=["Count"])
    top_words_df = top_words_df.sort_values(by="Count", ascending=False)
    top_words_df = top_words_df.reset_index(drop=True)
    top_words_df.index += 1

    return top_words_df


def top_emojis(df_t_e):
    """
    Identify and count the most frequently used emojis for each sender in a DataFrame.

    The function filters messages to include only those with emojis. 
    It then processes each message to keep only emoji characters and aggregates these emojis for each sender. 
    The resulting DataFrame lists each emoji, the sender, and the count of times the emoji was used.

    Parameters:
    df_t_e (DataFrame): DataFrame containing messages with their respective senders and emoji counts.

    Returns:
    DataFrame: A DataFrame with each row representing an emoji, the sender, and the count of the emoji's usage.
    """
    # Filter out messages without emojis
    df_t_e = df_t_e[df_t_e["Emoji Count"] > 0].copy()

    # Process messages to keep only emojis
    df_t_e["Message"] = df_t_e["Message"].apply(keep_only_emojis)

    # Initialize a counter for each sender's emojis
    most_emojis = {s: Counter() for s in df_t_e["Sender"].unique()}

    # Count emojis for each sender
    for index in df_t_e.index:
        most_emojis[df_t_e["Sender"][index]].update(df_t_e["Message"][index])

    # Convert the emoji counters into a DataFrame
    top_emojis_df = pd.DataFrame(most_emojis).reset_index()
    top_emojis_df = pd.melt(top_emojis_df, id_vars=['index'], value_vars=df_t_e["Sender"].unique())
    top_emojis_df = top_emojis_df.rename(columns={"index": "Emoji", "variable": "Sender", "value": "Count"})

    # Optional: Uncomment the following line to double-check each emoji
    # top_emojis_df = top_emojis_df[top_emojis_df.apply(double_check_emoji, axis=1)]

   # Clean up the DataFrame: drop NaNs, sort, and reset index
    top_emojis_df = top_emojis_df.dropna(subset=["Count"])
    top_emojis_df = top_emojis_df.sort_values(by="Count", ascending=False).reset_index(drop=True)
    top_emojis_df.index += 1

    return top_emojis_df


def plot_top(df_top, top_type, top_num=10):
    """
    Generate a DataFrame showing the top emojis or words used by each sender.

    The function supports two types of analyses: 'emojis' and 'words'. It calls either the 
    top_emojis or top_words function based on the 'top_type' argument, processes the data 
    to include only the top N items (where N is defined by 'top_num'), and returns a 
    consolidated DataFrame sorted by count.

    Parameters:
    df_top (DataFrame): DataFrame containing the data to be analyzed.
    top_type (str): Type of analysis to perform - 'emojis' or 'words'.
    top_num (int, optional): The number of top items to include for each sender. Defaults to 10.

    Returns:
    DataFrame: A DataFrame with the top items used by each sender, sorted by count.
    """
    holder = []

    # Process for top emojis
    if top_type == 'emojis':
        df_top = top_emojis(df_top).copy()
        for name in df_top['Sender'].unique():
            subset = df_top[df_top['Sender'] == name].iloc[:top_num]
            holder.append(subset)
    
    # Process for top words
    elif top_type == 'words':
        df_top = top_words(df_top).copy()
        for name in df_top['Sender'].unique():
            subset = df_top[df_top['Sender'] == name].iloc[:top_num]
            holder.append(subset)

    # Combine and sort results, then reset the index
    result_df = pd.concat(holder, ignore_index=True).sort_values(by="Count", ascending=False).reset_index(drop=True)

    # Adjust the index to start from 1
    result_df.index = result_df.index + 1

    return result_df


def plot_message_distribution(df_m_d):
    """
    Generate a donut chart visualizing the total number of messages sent by each sender.

    The function filters out any records associated with call durations, groups the data by sender, 
    and counts the number of messages for each. It then uses this data to create a donut chart, 
    displaying the proportion of messages sent by each sender, along with the total message count.

    Parameters:
    df_m_d (DataFrame): DataFrame containing message data with 'Call Duration (Sec)' and 'Sender' columns.

    Returns:
    None: The function directly displays the plot and does not return any value.
    """
    # Exclude call records
    df_m_d = df_m_d[~(df_m_d['Call Duration (Sec)'] > 0)].copy()

    # Count messages per sender
    message_count = df_m_d.groupby('Sender')["Message"].agg('count')

    # Prepare labels and sizes for the plot
    sizes = message_count.values
    labels = message_count.index
    total_messages = sum(sizes)

    # Create and configure the donut chart
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

    # Draw the center circle for the donut hole
    circle = plt.Circle((0, 0), 0.70, fc='white')
    ax.add_artist(circle)

    # Add message count labels to each segment
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
        x = wedge.r * 0.85 * np.cos(np.deg2rad(angle))
        y = wedge.r * 0.85 * np.sin(np.deg2rad(angle))
        ax.text(x, y, str(sizes[i]), ha='center', va='center', color='white', fontsize=12)

    # Display the total message count in the center
    ax.text(0, 0, f'Total Messages: {total_messages}', ha='center', va='center', color='black', fontsize=12)

    plt.title('Message Count per Sender')
    plt.show()

    
def total_message_frequency(df_t_m_f):
    """
    Analyzes and visualizes the total count of messages per day and hour in a heatmap.

    The function extracts the day of the week and hour from the DataFrame, groups the 
    messages by these time units, and calculates the total count of messages. It then 
    creates a heatmap to visually represent the frequency of messages throughout the week.

    Parameters:
    df_t_m_f (DataFrame): A DataFrame with columns 'Date', 'Time', and 'Message'.

    Returns:
    None: The function displays a heatmap and does not return a value.
    """
    # Exclude call records
    df_t_m_f = df_t_m_f[~(df_t_m_f['Call Duration (Sec)'] > 0)].copy()

    # Extract day name and hour from Date and Time columns
    df_t_m_f["Day"] = df_t_m_f["Date"].apply(lambda x: x.strftime('%A'))
    df_t_m_f["Hour"] = df_t_m_f["Time"].apply(lambda x: x.strftime('%H'))

    # Group data by Day and Hour and count the number of messages
    message_count_df = df_t_m_f.groupby(["Day", "Hour"])["Message"].count().reset_index()
    message_count_df.rename(columns={'Message': 'Count'}, inplace=True)

    # Define the desired order of days for the heatmap
    desired_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Create a pivot table for the heatmap
    pivot_table = message_count_df.pivot_table(values='Count', index='Day', columns='Hour', fill_value=0)
    pivot_table = pivot_table.reindex(desired_order)

    # Configure and display the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, cmap='Reds', annot=False, fmt='d', linewidth=.5)
    plt.xlabel('Hour of the Day')
    plt.ylabel('Day of the Week')
    plt.title(f"Message Count Heatmap with {df_t_m_f.index.name}")
    plt.show()
