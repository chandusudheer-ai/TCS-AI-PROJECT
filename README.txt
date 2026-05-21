STUDENT AI AGENT (INSTRUCTIONS)

Purpose
-------
This is a simple AI assistant app with two modes:
1) Document Q&A: Upload documents and ask questions based on those documents.
2) Chat: Ask general questions like a normal chatbot.

Who Is This For?
--------------
This guide is written for non-coders (for example, sales teams).


WHAT YOU NEED
-------------
1) A computer with internet access.
2) Python installed (recommended: Python 3.10+).
3) An API key + Base URL + Model name (provided by your organization).


ONE-TIME SETUP (WINDOWS)
-----------------------
1) Open Command Prompt (or PowerShell) in this folder.

2) Create a virtual environment:
   python -m venv venv

3) Activate it:
   venv\Scripts\activate

4) Install required packages:
   pip install -r requirements.txt


RUN THE APP
-----------
1) Make sure the environment is activated.

2) Start the app:
   streamlit run app.py

3) A browser tab should open automatically.
   If it does not open, copy the URL shown in the terminal.
   It is usually: http://localhost:8501

To stop the app: go to the terminal and press Ctrl + C


USING THE APP (VERY IMPORTANT)
------------------------------
On the left side (sidebar), fill these fields:
1) API key
2) Base URL
3) Model name

Note: If API key is empty, the app cannot generate answers.


MODE 1: DOCUMENT Q&A
--------------------
Use this when you want answers from your uploaded files.

Steps:
1) Go to the "Document Q&A" tab.
2) Upload one or more files.
3) Type your question.
4) Click "Get answer".

Tips:
1) Ask one clear question at a time.
2) If the answer is not present in the file, the app will say it cannot find it.
3) For tables, mention the sheet name or column name in your question.


MODE 2: CHAT
------------
Use this for general questions.

Steps:
1) Go to the "Chat" tab.
2) Type your message at the bottom.
3) Press Enter.
4) Use "Clear chat" to start a fresh conversation.


SUPPORTED FILE TYPES
--------------------
Documents:
- PDF (.pdf)
- Word (.docx)

Spreadsheets:
- Excel (.xlsx, .xls, .xlsm, .xlsb)
- OpenDocument Spreadsheet (.ods)

Text tables:
- CSV (.csv)
- TSV (.tsv)


TROUBLESHOOTING
---------------
1) "Please enter API key"
   Enter the API key in the left sidebar.

2) "Could not read this spreadsheet file"
   Try opening the file and saving it again as XLSX or CSV, then upload.

3) The app is slow
   Large files can take time to extract text.

4) The page is blank / not opening
   Ensure the command "streamlit run app.py" is running in the terminal.
   If needed, refresh the browser page.


SECURITY NOTE
-------------
Treat the API key like a password.
Do not share screenshots containing the API key.
