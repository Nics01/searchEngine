import os
import pickle
import PySimpleGUI as sg
#sg.ChangeLookAndFeel('Dark') remove "#" to change to dark mode
 
class Gui:
    def __init__(self):
        self.layout = [
            #First row of GUI
            [sg.Text('Search Term', size=(10, 1)), 
            sg.Input(size=(40, 1), focus=True, key="TERM"),
            sg.Radio('Contains', group_id='choice', default=True, size=(6, 1), key="CONTAINS"),
            sg.Radio('Starts With', group_id='choice', size=(8, 1), key="STARTSWITH"),
            sg.Radio('Ends With', group_id='choice', size=(8, 1), key="ENDSWITH")],
            #Second row of GUI
            [sg.Text('Root Path', size=(10, 1)),
            sg.Input('C:/',size=(40, 1), key="PATH"),
            sg.FolderBrowse('Browse', size=(6, 1)),
            sg.Button('Re-index', size=(6, 1), key="INDEX"),
            sg.Button('Search', size=(6, 1), bind_return_key=True, key="SEARCH")],
            #Output window
            [sg.Output(size=(100,30))]
        ]
        self.window = sg.Window('File Search Engine').Layout(self.layout)

class SearchEngine:
    def __init__(self):
        self.file_index = []    #List that will store the directory index the os.walk() function returns
        self.results = []   #List that will store the reults of each search
        self.matches = 0    #Counter to count each matching file
        self.records = 0    #Counter to count each records searched

    def create_new_index(self, values):
        #Create a new index and save to pkl file
        root_path = values['PATH']
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        #Save to file
        with open('file_index.pkl', 'wb') as f:
            pickle.dump(self.file_index, f)

    def load_existing_file(self):
        #Load existing index if it exist
        try:
            with open('file_index.pkl', 'rb') as f: #rb -> Read Binary
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, values):
        #Search for term based on search type
        
        #Reset variables
        self.results.clear()
        self.matches = 0
        self.records = 0
        term = values['TERM']

        #Perform search
        for path, files in self.file_index:
            for file in files:
                self.records +=1 #Increment value for every record searched
                #Search options: Contains, Starts with, and Ends with
                if( values['CONTAINS'] and term.lower() in file.lower() or
                    values['STARTSWITH'] and file.lower().startswith(term.lower()) or
                    values['ENDSWITH'] and file.lower().endswith(term.lower())):

                    result = path.replace('\\','/') + '/' + file #Replace back slash with forward slashes
                    self.results.append(result)
                    self.matches +=1 #Increment match value
                else:
                    continue

        #Save search results
        with open('search_results.txt','w') as f:
            for row in self.results:
                f.write(row +'\n')

def main():
    g = Gui()
    s = SearchEngine()
    s.load_existing_file() #Load existing file, if available, upon starting program

    while True:
        event, values = g.window.Read()

        if event is None:
            break
        if event == 'INDEX': #If Re-Index button is clicked
            s.create_new_index(values)
            print()
            print('>> New Index has been created')
            print()
        if event == 'SEARCH': #If Search button is clicked
            s.search(values)
            print()
            for result in s.results:
                print(result)
            print()
            print('>> There were {:,d} matches out of {:,d} records searched.'.format(s.matches, s.records))
            print()
            print('>> This query produced the following matches: \n')
            print('This file is saved.')

main()