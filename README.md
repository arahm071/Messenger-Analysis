![DALL·E 2024-03-20 19 06 56 - Integrate the uploaded Messenger logo into a rectangular title card design  The title card should have a sleek, high-tech background that resonates wi](https://github.com/arahm071/Messenger-Unwrapped/assets/84313155/390e7908-2739-494d-835b-83453429801b)


# Messenger Unwrapped

**Analyze your Facebook Messenger chats and discover hidden patterns.**

Messenger Unwrapped is a Python application designed to help you understand your messaging habits. It works by:

* **Extracting and cleaning chat data** from Facebook JSON files.
* **Analyzing key metrics:**  
    * Most used words and emojis
    * Message distribution across participants
    * Message frequency over time (heatmaps)
* **Exporting insights:** Save cleaned data as a CSV for further exploration.

**Why use Messenger Unwrapped?**

* **Understand your communication patterns:** See who you message most, your favorite words, and when you're most active.
* **Dive into group dynamics:** Analyze word usage and message distribution within group chats.
* **Personalize your data journey:**  Use the exported CSV for custom analysis or create your own visualizations.

## Features
### Data Handling and Preparation
This application includes a robust process for preparing Facebook Messenger chat data, which involves data extraction and cleaning:

### Data Extraction
- **Data Aggregation:** The application employs scripts (`single_folder.py` for individual chats and `all_folders.py` for all chats) to handle the extraction process. These scripts read JSON files from the specified directory, converting the contained JSON dictionaries into a list.
- **DataFrame Creation:** The listed dictionaries are then transformed into a unified DataFrame. This process is identical whether analyzing a single chat or combining multiple chats.

### Data Cleaning and Transformation
- **Initial Processing:** The `clean_messages` function takes the unified DataFrame and begins the cleaning process.
- **Enhancing Data Readability:** Timestamps are converted into separate date and time columns for better readability. Columns are renamed for easier navigation, and rows with irrelevant data are filtered out.
- **Data Enrichment:** Each message row is enriched with word and emoji counts, providing detailed insights for analysis.
- **Finalized DataFrame:** The result is a well-organized DataFrame, where all necessary information is cleanly presented and extraneous data is removed.

### Analytical Features
Once the data is prepared, the application offers a range of features to analyze and visualize the chat data:

1. **Message Stats:** This feature aggregates messaging statistics into a table showing each participant's message count, word count, and call duration. Notably, the call duration reflects the time for calls initiated by each user, meaning it only increases for the person who started the call, not for other participants in the call.

![readme_ex_general_messsage_stats](https://github.com/arahm071/Messenger-Unwrapped/assets/84313155/17931fbb-4bfd-4099-83be-52c08560a5e9)

2. **Top Words:** Analyzes and ranks the top 10 words used by the user and the chat partner(s). In group chats, it aggregates this data across all participants, providing a comparative word usage analysis.

![readme_ex_chats_top_words](https://github.com/arahm071/Messenger-Unwrapped/assets/84313155/51ffc67d-f98a-4102-a20e-a5f1903e431a)

3. **Emoji Analysis:** Similar to the Top Words feature, but focuses on emoji usage. It identifies and ranks the top 10 emojis used by each participant in the chat.

![readme_ex_chats_top_emojis](https://github.com/arahm071/Messenger-Unwrapped/assets/84313155/1e4a5477-e164-4192-b1be-f1a528c8793c)

4. **Message Distribution:** Visualized through a donut chart, this feature shows the distribution of total messages sent by each participant in a chat. It includes the total message count in the center, with individual contributions and their percentage of the total displayed in segments.

![readme_ex_messegae_distribution](https://github.com/arahm071/Messenger-Unwrapped/assets/84313155/22ab9929-dfa6-48e4-a6ab-1492c9728da8)

5. **Total Message Frequency:** Generates a heat map to visualize the frequency of messages sent on different days and times. This feature provides insights into the most active periods in the chat history, offering a temporal dimension to the analysis.

![readme_ex_message_frequency](https://github.com/arahm071/Messenger-Unwrapped/assets/84313155/a60d1914-9b84-4064-8105-5b1c1433ecf3)

6. **Export Cleaned Data to CSV:** This feature allows you to export the cleaned data from the currently selected chat into a CSV file. The CSV file will be saved in a designated folder, making it easily accessible for any additional processing or review.


## Technologies
### Language
- **Python:** The core programming language used for the entire project.

### Libraries
- **Pandas:** For data manipulation and analysis, particularly useful for working with structured data like DataFrames.
- **NumPy:** Employed for numerical computing, aiding in efficient processing of numerical data.
- **Matplotlib:** Used for creating static, interactive, and exploratory visualizations, essential in data analysis.
- **JSON:** For handling JSON data files, fundamental in data extraction and processing.
- **Emoji:** A specialized library for processing emojis within text data.
- **FuzzyWuzzy:** For string matching, useful in tasks like chat participant identification.
- **Thefuzz:** Another string matching library used in conjunction with FuzzyWuzzy.

## Getting Started

### Installation of Required Libraries
Before you can use this project, you'll need to install some Python third-party libraries:

- Pandas
- Emoji
- FuzzyWuzzy
- Fuzz
- Matplotlib
- Seaborn
- NumPy

Users can easily look up how to install these libraries using pip on their own.
___

### Requesting Your Facebook Data
To use this application, you first need to obtain your chat data from Facebook. Follow these steps:

1. **Log into Facebook**: Visit the Facebook homepage and log into your account.

2. **Access Settings and Privacy**:
   - In the top-right corner of the Facebook homepage, click on your profile picture or your account name.
   - Select "Settings and Privacy."

3. **Navigate to Settings**:
   - After clicking on "Settings and Privacy," choose "Settings."

4. **Access "Download Your Information"**:
   - On the left side of the Settings page, scroll down until you find "Your Information."
   - Click on "Download Your Information."

5. **Start Download**:
   - Inside the "Download Your Information" box, click "Continue."

6. **Choose Facebook Profile**:
   - You will be redirected to the "Download Your Information" page within the Account Center.
   - In this box, click "Request a Download."
   - You will see your connected accounts and profiles. Select only your Facebook profile (even if you have Instagram connected).

7. **Select Types of Information**:
   - Click "Next" to proceed.
   - Under "Your Facebook Activity," select "Messages" only.

8. **Choose Date Range and Preferences**:
   - Configure your date range and notification preferences according to your requirements.

9. **Select Format**:
   - For "Format," choose "JSON" (not HTML).

10. **Media Quality**:
    - Depending on your preference, choose the desired media quality settings.

11. **Submit Your Request**:
    - Click "Create File."

12. **Wait for Data**:
    - Depending on the amount of data, it may take some time for Facebook to prepare your information. Be patient.

13. **Download and Extract**:
    - Once your data is ready, it will be provided in multiple zip files.
    - Download all the zip files and extract them to the same folder or location.

14. **Access Your Messages**:
    - Inside the extracted data, navigate to the "messages" folder.
    - Look for the "inbox" folder; this contains your chat messages.

Now you have the necessary data to analyze your Facebook Messenger chats using this application.
___

### Setting Up the Project
After obtaining your Facebook data, you can set up and run the application:

1. **Download the Project:** Clone the repository or download it as a ZIP file.
2. **Unzip and Navigate:** If you downloaded it as a ZIP, unzip it. Navigate to the project directory in your terminal.
3. **Install Dependencies:** Ensure you have Python installed and install the necessary libraries.
4. **Prepare the Data:** Unzip your Facebook data and place it in the designated project directory.
5. **Run the Application:** Execute the `chat_analysis.py` script to start the analysis.
___

### Usage
1. **Run the Application:**
   - Launch the `chat_analysis` script.
   - The application will prompt you for a file path.

2. **Provide the Data Path:**
   - Enter the path to the 'inbox' folder where you have unpacked your Facebook chat data zip files.
   - Submit the path by pasting it into the terminal and pressing 'Enter'.

3. **Folder Name Adjustment:**
   - A prompt will appear asking to change folder names in the 'inbox' folder for convenience.
   - Type 'y' or 'yes' and press 'Enter' to confirm.
   - This step renames folders to make them more accessible for the application.

4. **Select the Chat for Analysis:**
   - The application will ask which chat you want to analyze.
   - You can choose to analyze 'all' chats combined or a specific chat.
   - For a specific chat, enter the name of the person or the group chat name or for all chat just type 'all' and press enter.
   - A list of the top 10 matching names will be displayed.
   - Select the desired chat by entering the corresponding number.

5. **Data Processing:**
   - After selection, the application will process and load the data into data frames.
   - This may take a moment depending on the size of the chat data.

6. **Choose Analysis Features:**
   - Various features (labeled from 1 to 6) will be available for analysis.
   - Select the feature number you wish to use.
   - Option 7 allows you to return to the chat selection step.
   - Option 8 exits the program.

## Future Plans

My aim is to continually improve this project with a focus on increasing its interactivity and user engagement:

- **Interactive Features:** Enhancements such as allowing users to select specific date ranges for chat analysis are in the pipeline. This will offer a more personalized and detailed exploration of chat data.

- **Enhanced Displays:** I plan to introduce a variety of new data visualization types. These will make the presentation of chat insights more dynamic and visually interesting.

- **Long-Term Goal - Interactive Dashboard:** Eventually, I hope to develop an interactive dashboard, potentially as a web application or GUI. This is contingent on my learning and comfort with the necessary web or GUI development technologies, marking it as a future goal.

These updates are aimed at making the tool more versatile and enjoyable to use. As I learn and adapt to new programming techniques, I'll work towards incorporating these features into the project.


## Acknowledgements

- **Quang-Vinh:** Shout-out to Quang-Vinh for introducing me to a WhatsApp chat analysis project, which was the initial spark for this project. Thier motivation and guidance at the start of this project was crucial in making this idea a reality.

- **bijx:** Thanks to bijx for the help in setting up the GitHub repository for this project. Their assistance was invaluable in sharing this work with others.

- **Inspiration Source:** The concept for this project was initially inspired by a WhatsApp chat analysis project. Seeing that analysis made me realize the potential of doing something similar for Facebook Messenger. https://www.reddit.com/r/datascience/comments/x0o1nt/whatsapp_chat_analysis_between_me_and_a_friend/
