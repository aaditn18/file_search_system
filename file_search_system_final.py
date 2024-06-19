import os
import sys
import fitz
import docx2txt
from datetime import datetime
import time

# Function to retrieve files from the system based on selected file types
def retrieve_files(file_types, search_directory):
    file_list = []
    for root, dirs, files in os.walk(search_directory):
        for file in files:
            if is_text_file(file, file_types):
                file_list.append(os.path.join(root, file))
    return file_list

# Function to check if a file has a text-based extension based on selected file types
def is_text_file(file, file_types):
    if file.endswith(".sock"):
        return False
    for ext in file_types:
        if file.endswith(ext):
            return True
    return False

# Function to perform content search on files using keyword search
def search_files(files, keyword, task, os_device):
    search_results = []
    for file in files:
        try:
            if file.endswith(".docx"):
                count = search_docx_file(file, keyword)
                if task == 1 and os_device == 2 and keyword.lower() in file[1+file.rindex('/'):file.rindex('.')].lower():
                    search_results.append((file, count, get_last_modified_date(file)))
                elif task == 1 and os_device == 1 and keyword.lower() in file[1+file.rindex('\\'):file.rindex('.')].lower():
                    search_results.append((file, count, get_last_modified_date(file)))
                elif task == 2 and count > 0:
                    search_results.append((file, count, get_last_modified_date(file)))
            elif file.endswith(".pdf"):
                count = search_pdf_file(file, keyword)
                if task == 1 and os_device == 2 and keyword.lower() in file[1+file.rindex('/'):file.rindex('.')].lower():
                    search_results.append((file, count, get_last_modified_date(file)))
                elif task == 1 and os_device == 1 and keyword.lower() in file[1+file.rindex('\\'):file.rindex('.')].lower():
                    search_results.append((file, count, get_last_modified_date(file)))
                elif task == 2 and count > 0:
                    search_results.append((file, count, get_last_modified_date(file)))
            else:
                with open(file, 'r', errors='replace') as f:
                    content = f.read()
                    count = content.lower().count(keyword.lower())
                    if task == 1 and os_device == 2 and keyword.lower() in file[1+file.rindex('/'):file.rindex('.')].lower():
                        search_results.append((file, count, get_last_modified_date(file)))
                    elif task == 1 and os_device == 1 and keyword.lower() in file[1+file.rindex('\\'):file.rindex('.')].lower():
                        search_results.append((file, count, get_last_modified_date(file)))
                    elif task == 2 and count > 0:
                        search_results.append((file, count, get_last_modified_date(file)))
        except (UnicodeDecodeError, FileNotFoundError, PermissionError):
            continue
    search_results.sort(key=lambda x: (x[2], x[1]), reverse=True)
    return [file[0] for file in search_results]


# Function to get the last modified date of a file
def get_last_modified_date(file_path):
    try:
        return os.path.getmtime(file_path)
    except OSError:
        return 0


# Function to search keyword in a .docx file
def search_docx_file(file, keyword):
    if file.startswith('~$'):
        return False
    text = docx2txt.process(file)
    if keyword.lower() in text.lower():
        return True
    return False

# Function to search keyword in a .pdf file
def search_pdf_file(file, keyword):
    doc = fitz.open(file)
    for page in doc:
        text = page.get_text()
        if keyword.lower() in text.lower():
            doc.close()
            return True
    doc.close()
    return False

# Function to display search results
def display_search_results(search_results, startDateStamp, endDateStamp):
            
    if search_results:
        print("Search results:")
        j=0
        for i, file in enumerate(search_results):
            try:
                last_modified = os.path.getmtime(file)
                if startDateStamp != '' and endDateStamp != '' and last_modified >= startDateStamp and last_modified <=endDateStamp:
                    last_modified_date = datetime.fromtimestamp(last_modified)
                    formatted_date = last_modified_date.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{i+1-j}. {file} (Last Modified: {formatted_date})")
                    continue
                elif startDateStamp != '' and endDateStamp != '':
                    j=i+1
                    continue
                elif startDateStamp == '' and endDateStamp == '':
                    last_modified_date = datetime.fromtimestamp(last_modified)
                    formatted_date = last_modified_date.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{i+1}. {file} (Last Modified: {formatted_date})")
            except OSError:
                if startDateStamp != '' and endDateStamp != '':
                    continue
                else:
                    print(f"{i+1}. {file}")
                    continue
    else:
        print("No matching files found.")

# Main function to run the file search system
def main():

    print("1. Start")
    os_device= int(input("Enter 1 for Windows and 2 for macOS Operating System: "))
    search_platform = input("Enter 'local' to search in the local system or 'network' to search in a network: ")
    while search_platform != "local" and search_platform != "network":
        print("Invalid input, try again...")
        search_platform = input("Enter 'local' to search in the local system or 'network' to search in a network: ")

    if search_platform == "network":
        search_directory = input("Enter the directory path in the network to search: ")
        if not os.path.exists(search_directory):
            print("Invalid directory path or directory does not exist.")
            return
    else:
        search_directory = '.'

    task = int(input("Enter 1 for searching based on file name, 2 for searching based on content: "))

    while task != 1 and task != 2:
        print("Invalid input, try again...")
        task = int(input("Enter 1 for searching based on file name, 2 for searching based on content: "))

    print("2. Enter search query (keyword(s))")
    keyword = input("Enter keyword(s): ")

    print("3. Select file types to filter:")
    print("   1. .txt")
    print("   2. .csv")
    print("   3. .py")
    print("   4. .java")
    print("   5. .pdf")
    print("   6. .docx")
    selected_file_types = input("Enter file type numbers (comma-separated): ").split(",")
    file_types = get_file_types(selected_file_types)
    startDateStamp=''
    endDateStamp=''

    while True:
        filterdate=int(input("Enter 1 to filter by specified date range of last modified , 2 to not filter: "))
        if filterdate==1:
            startDate = input("Enter Earliest Date in format: 'YYYY-MM-DD': ")+" 00:00:00"
            endDate= input("Enter Last Date in format: 'YYYY-MM-DD': ")+" 00:00:00"
        elif filterdate==2:
            break
        try:
            startDateStamp=datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S").timestamp()
            endDateStamp=datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S").timestamp()
            break
        except:
            print("Incorrect Date input")
        

    print("4. Retrieving files from the system...")
    files = retrieve_files(file_types, search_directory)

    print("5. Performing content search on files...")
    search_results = search_files(files, keyword, task, os_device)

    display_search_results(search_results, startDateStamp, endDateStamp)

    if search_results:
        file_index = input("Select a file to open (enter the corresponding number, '0' to exit): ")
        if file_index.isdigit():
            file_index = int(file_index)
            if file_index > 0 and file_index <= len(search_results):
                selected_file = search_results[file_index - 1]
                absolute_file_path = os.path.abspath(selected_file)
                open_file(absolute_file_path)
            elif file_index == 0:
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid file selection.")

    print("6. End")

# Function to map selected file type numbers to file extensions
def get_file_types(selected_file_types):
    file_types = []
    for selected_type in selected_file_types:
        if selected_type == "1":
            file_types.append(".txt")
        elif selected_type == "2":
            file_types.append(".csv")
        elif selected_type == "3":
            file_types.append(".py")
        elif selected_type == "4":
            file_types.append(".java")
        elif selected_type == "5":
            file_types.append(".pdf")
        elif selected_type == "6":
            file_types.append(".docx")
    return file_types

# Function to open a file using the default application
def open_file(file_path):
    if sys.platform == 'darwin':
        os.system(f"open '{file_path}'")
    elif sys.platform == 'win32':
        os.startfile(file_path)
    elif sys.platform == 'linux':
        os.system(f"xdg-open '{file_path}'")

if __name__ == '__main__':
    main()
