File Search System
Overview
This script searches for specific keywords within text-based files on your system. It supports .txt, .csv, .py, .java, .pdf, and .docx file types, allowing you to specify which file types to search and enter a keyword to find within the content of those files.

Features
File Retrieval: Scans directories to find files of specified types.
Content Search: Searches for a keyword within the content of found files.
File Support: Handles .txt, .csv, .py, .java, .pdf, and .docx files.
Result Display: Shows search results and lets you open selected files.
Requirements
Python 3.x
Libraries: PyPDF2, python-docx
Installation
Install the required libraries with:

bash
Copy code
pip install PyPDF2 python-docx
Usage
Run the Script

bash
Copy code
python file_search.py
Enter Search Query
Provide the keyword(s) you want to search for.

Select File Types
Choose file types to search by entering the corresponding numbers:

markdown
Copy code
1. .txt
2. .csv
3. .py
4. .java
5. .pdf
File Retrieval
The script scans the current directory and subdirectories for the specified file types.

Content Search
The script searches for the provided keyword(s) within the retrieved files.

Display Results
The script displays the files where the keyword(s) were found. You can choose to open any of these files.

Functions
retrieve_files(file_types): Scans directories to find files with specified extensions.
is_text_file(file, file_types): Checks if a file matches the specified types.
search_files(files, keyword): Searches for a keyword within the content of files.
search_docx_file(file, keyword): Searches for a keyword in .docx files.
search_pdf_file(file, keyword): Searches for a keyword in .pdf files.
display_search_results(search_results): Displays the search results.
get_file_types(selected_file_types): Maps input numbers to file extensions.
open_file(file_path): Opens the selected file with the default application.
Example Workflow
Run the script.
Enter the keyword "example".
Select file types, e.g., 1,5 for .txt and .pdf.
View search results and choose a file to open.
Notes
Skips certain file types like .sock and temporary files starting with ~$.
Ensure proper permissions to access and read files.
Author
Your Name
