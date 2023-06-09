# Langchain LLM Sample

Langchain LLM Sample is a sample application that demonstrates the usage of the Langchain library to generate realistic and engaging dialogues with non-player characters (NPCs) in role-playing games. This project is powered by OpenAI's GPT API and uses a custom implementation to generate the conversations.

## Explanatory Video (youtube)
(Japanese)
https://youtu.be/GR7Nx7eanis

(English)
https://youtu.be/9UOHGBnotiM

## Installation

1. Clone this repository:

git clone https://github.com/MayaEnomoto/LangchainLLMSample.git
<br>
<br>

2. Install the required dependencies:

pip install -r requirements.txt

## Usage (test program : app_async.py)

0. Set Open AI API:

Set your Open AI API-key in config.py.
<br>
<br>

1. Run the application:

python app_async.py

![Example GUI](assets/main.png)

(1)Enter the path to the folder with text files:
Specify various settings in text files and store them in FAISS.

(2)Dict:
Enter topics and additional settings as needed.

(3)Name:
Enter the character for the conversation or action. The conversation and action can be left blank if necessary.

(4)Talk:
Enter the conversation.

(5)Behavior:
Enter the action.

(6)Emotion:
Enter the emotion of the conversation or action.

(7)Request:
Enter the content you want to request from GPT.

(8)Use multiple responses:
Change the response check from GPT from retries to multiple responses.

(9)Generate conversation:
The response from GPT will be displayed.
<br>
<br>

## Usage (NPC Chat generation : app_chat_creator.py)

0. Set Open AI API:

Set your Open AI API-key in config.py.
<br>
<br>

1. Run the application:

python app_chat_creator.py

![Example GUI](assets/generate.png)

(1)Select FAISS Index Folder:
The faiss_index generated by the test application is available.<br>
As much as possible, it is better to prepare separate indices for each story, town or dungeon.

(2)Select Input CSV:
An npc conversation file is generated for the defined number of lines.
<br>
Please refer to sample_input.csv.
<br>
sample2\sample_input.csv
<br>
Progress/Location/etc, Actor, Emotion of the conversation (bright topic, sad topic, etc.)

(3)Select Output Txt:
Choose a folder to save the results and enter a file name.
<br>
The file name will look like this
<br>
Name_entered_0000.json<br>
Name_entered_0001.json<br>
Name_entered_0002.json<br>
...

(4)Generate conversation:
Starts the actual generation of the conversation.
Please be patient, as this will take quite some time depending on the amount of keywords and FAISS inxex.
It is a good idea to start with a csv of one or two lines to see if the output is what you expect.
<br>
<br>

## License

This project is licensed under the [MIT License](LICENSE).

