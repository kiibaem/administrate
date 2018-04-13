import pickle as pi
import pandas as pd


pd.set_option('display.max_rows', 1000)

def add(dict,content):
    # Appends new rows to the database by taking dictionaries and turning them in to DataFrames.
    new_row = pd.DataFrame.from_dict(dict, orient = 'columns')
    content = content.append(new_row, ignore_index = True)
    return content
    
def get(content):
    # Returns all rows which contain the selected value - will do partial matches.
    col = input("Which column would you like to search? ")
    stri = input("What are you looking for? ")
    selection = content.loc[content[col].str.contains(stri)]
    return selection

def delete(col, val, content):
    # Deletes rows based on the content in a specified column.
    index_to_delete = content.index[content[col] == val].tolist()
    content = content.drop(index = index_to_delete)
    return content

def run():
    i = 1
    while i > 0: # Wanted the program to keep running, so I put it in an infinite while loop, this is broken if you enter the 'exit' command.
        command = input("What would you like to do? (Enter 'new' to create a new database - this will overwrite the existing database, 'exit' to leave the program, 'add' to create a new entry, 'get' to view specific entries, 'view' to see the whole database, or 'delete' to remove entries.) ")
        # Checks to see what command you entered and then runs the correct code snippet.
        if command == 'new':
            content = pd.DataFrame(columns = ['Organisation', 'Name','Position','Email','Phone number', 'Address']) # Basic empty dataframe - the contacts database will live here.
            data = open('./data.pkl', 'wb')
            pi.dump(content, data)
            data.close()
            print("New database initialised!")
        elif command == 'add':
            add_more = 'yes'
            while add_more == 'yes':
                # Data is loaded before any 'add', 'get' or 'delete' operation and saved immediately after. This is so that if the program crashes, the data still persists.
                with open('data.pkl', 'rb') as data:
                    content = pi.load(data, fix_imports=True) # Pickle is used to save the data as this keeps it in an easily python-readable format.
                print("To add a new contact, simply fill in the information when prompted. If you wish to leave a field blank, just enter a '-'.")
                data = {'Organisation':[input("Name of organisation: ")], 'Name':[input("Name of contact: ")], 'Email':[input("Email address of contact: ")], 'Phone number':[input("Phone number of contact: ")], 'Address': [input("Address of organisation/contact: ")], 'Position':[input("Job title of contact: ")]}
                content = add(data, content)
                print(content)
                with open('data.pkl', 'wb') as data:
                    pi.dump(content, data)
                add_more = input("Add another contact? (yes/no): ")
            print(content)
        elif command == 'get':
            with open('data.pkl', 'rb') as data:
                content = pi.load(data, fix_imports=True)
            selection = get(content)
            print(selection)
        elif command == 'view':
            with open('data.pkl', 'rb') as data:
                content = pi.load(data, fix_imports=True)
                print(content)
        elif command == 'delete':
            print("Please enter first which column you would like to look for the record to delete in, followed by the expected text for the row to delete.")
            col = input("Enter the column you want to search: ")
            val = input("Enter the data you want to delete: ")
            with open('data.pkl', 'rb') as data:
                content = pi.load(data, fix_imports=True)
            content = delete(col, val, content)
            print(content)
            with open('data.pkl', 'wb') as data:
                    pi.dump(content, data)
        elif command == 'exit':
            exit() # Breaks the infinite while loop. 
        else:
            print("Please enter a valid command.")
        i += 1 # Keeps the loop going after the if/elif/else exits (unless previous command was 'exit'.)


run()