# Required modules
import PyPDF2
import os
import re
import pandas as pd

# User input for search word or words. Use serial commas for multiple words.
words = ["enter word", "enter second word"]
results = []  # Initialize an empty list to store the results in the csv.

for foldername, subfolders, files in os.walk("enter directory name here"):  # Walk through directory to read the files
    for file in files:  # Loop to walk through each file for os.walk().
        print('\n')  # Adds a line break.
        print('file:', file)  # Prints the file name with the file prefix.

        pdfReader = PyPDF2.PdfReader(os.path.join(foldername, file))  # Opens the pdf file.

        numPages = len(pdfReader.pages)  # Gets the number of pages using latest PyPDF2 documentation.

        for i in range(numPages):  # Loops for reading all the pages in the directory
            PageObj = pdfReader.pages[i]  # Creates a page object
            pdfdata = PageObj.extract_text()  # Extracts text to the console.
            print('\n')  # Adds a line break.
            print("Page No:", i+1)  # Prints the page number.

            text = pdfdata  # Sets text object and splits the extracted text into lines.

            # Splits the extracted text into sentences.
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s', pdfdata)

            found = False  # Flag to check if the search term(s) is/are found.
            for lineNum, line in enumerate(sentences):  # A loop to run through all pdfs.
                # Checks for exact word match in the if condition. The \b is a boundary around the word.
                if any(re.search(r'\b' + re.escape(word) + r'\b', line) for word in words):  # Checks for search terms.
                    for word in words:
                        # Function to find and replace exact word matches with leading/ending lines for readability.
                        line = re.sub(r'\b' + re.escape(word) + r'\b', f'_{word}_', line)
                    # print('\n')  # Adds a line break.
                    print('Line Number:', lineNum + 1)  # Prints line number for found text (1-based index)
                    print('Sentence:', line)  # Prints the sentence with the found text.
                    print('\n')  # Adds a line break.
                    found = True  # Sets the flag to True if it finds text in the sentence.

                    results.append([file, i + 1, line])  # The loop index of the page that appends to the results list.

            if not found:  # A check flag for empty search outside the loop.
                print(f"I did not find any search terms on Page {i+1}.")  # Message for null.

df = pd.DataFrame(results, columns=['File', 'Page Number', 'Sentences'])  # Creates a dataframe with headers.
df.to_csv('results.csv', index=False)  # Saves the df to a csv file.
