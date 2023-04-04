import spec_parser
import spec_parser_t2
import sys
from PyQt5.QtWidgets import *
from gui_v3 import Ui_MainWindow
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import resolve1
import os
import csv
import os
import traceback
import time
import multiprocessing
from multiprocessing import Manager, Process
import json

header = ['Document Name', 'Search Word Text', 'Secondary Search', 'Element Identifier ', 'Element Text']
import re
"""
Application class (some main class to manage the app)
"""


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class AppWindow(QMainWindow):

    # this method called when class object is created
    def __init__(self):
        print('__init__')
        super().__init__()
        # add GUI code to app (from gui.py file)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # folder to save results
        self.folder = ''
        # all PDF files to parse
        self.files = []
        self.patterns = []
        # events
        """
        The event object (event) encapsulates the state changes in the event source.
         The event target is the object that wants to be notified. 
         Event source object delegates the task of handling an event to the event target. 
         PyQt5 has a unique signal and slot mechanism to deal with events.

         So, self.ui.selectPDF - is a button
            (self.select_pdf - is a method called when the button pressed
        """
        self.ui.selectPDF.clicked.connect(self.select_pdf)
        # self.ui.text_edit.clicked.connect(self.select_txt)
        self.text_files = []
        self.ui.selectSaveFolder.clicked.connect(self.select_save_folder)
        self.ui.runButton.clicked.connect(self.parse_run)
        self.ui.closeButton.clicked.connect(self.shutprocess)
        self.ui.selectPS.clicked.connect(self.selectPS)
        self.ui.selectSS.clicked.connect(self.selectSS)
        # self.ui.saveButton.clicked.connect(self.save_pattern)
        #self.ui.loadButton.clicked.connect(self.load_pattern)

        with open('primary.json', 'r') as f:
            data = json.load(f)
        i = 0
        for x in self.ui.text_edits_primary:
            x.setPlainText('\n'.join(list(data.values())[i]))
            i += 1

        with open('secondary.json', 'r') as f:
            data = json.load(f)
        i = 0
        for x in self.ui.text_edits_secondary:
            x.setPlainText('\n'.join(list(data.values())[i]))
            i += 1

        with open('regex.json', 'r') as f:
            data = json.load(f)
        i = 0
        for x in self.ui.buttons_primary:
            x.setText("browse..")
            x.clicked.connect(self.select_txt)
            i += 1

        for x in self.ui.buttons_secondary:

            x.setText("browse..")
            x.clicked.connect(self.select_txt)
            i += 1

        self.patterns = [x["regex"] for x in list(data.values())]
        print("Patterns")
        print(self.patterns)

        # show gui
        self.show()




    def selectPS(self):
        try:
            print('selectPS')
            print('selectSS')
            '''get pdf`s file names'''
            caption = 'Open txt file file with seach words line by line'
            # use current/working directory
            directory = './'
            # allows to select TXT files only
            filter_mask = "*.json"
            # returns all PDF files selected
            self.text_files, _ = QFileDialog.getOpenFileName(None,
                                                             caption, directory, filter_mask)
            print(self.text_files)
            with open('primary.json', 'r') as f:
                data = json.load(f)
            i = 0
            for x in self.ui.text_edits_primary:
                x.setPlainText('\n'.join(list(data.values())[i]))
                i += 1
        except Exception:
            pass

    def selectSS(self):
        try:
            print('selectSS')
            '''get pdf`s file names'''
            caption = 'Open txt file file with seach words line by line'
            # use current/working directory
            directory = './'
            # allows to select TXT files only
            filter_mask = "*.json"
            # returns all PDF files selected
            self.text_files, _ = QFileDialog.getOpenFileName(None,
                                                             caption, directory, filter_mask)
            print(self.text_files)
            with open(self.text_files, 'r') as f:
                data = json.load(f)
            i = 0
            for x in self.ui.text_edits_secondary:
                x.setPlainText('\n'.join(list(data.values())[i]))
                i += 1
        except Exception:
            pass

    def save_pattern(self):
        print('save_pattern')

    def load_pattern(self):
        '''get pdf`s file names'''
        caption = 'Open txt file file with seach words line by line'
        # use current/working directory
        directory = './'
        # allows to select TXT files only
        filter_mask = "*.json"
        # returns all PDF files selected
        self.text_files, _ = QFileDialog.getOpenFileName(None,
                                                         caption, directory, filter_mask)
        with open(self.text_files, 'r') as f:
            data = json.load(f)
        i = 0
        for x in self.ui.text_edits_primary:
            x.setText(list(data.values())[i]["comment"])
            i += 1
        self.patterns = [x["regex"] for x in list(data.values())]
        print(self.patterns)

    def shutprocess(self):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            print('Window closed')
        else:
            pass

    # simple method that allows to select multiple PDF`s from filesystem
    def select_txt(self):
        try:
            '''get pdf`s file names'''
            caption = 'Open txt file file with seach words line by line'
            # use current/working directory
            directory = './'
            # allows to select TXT files only
            filter_mask = "*.txt"
            # returns all PDF files selected
            self.text_files, _ = QFileDialog.getOpenFileName(None,
                                                             caption, directory, filter_mask)
            with open(self.text_files, 'r', encoding='utf-8') as f:
                data = [x.strip() for x in f.read().split('\n') if x.strip()]
                print(data)
            name = self.sender().objectName()
            if 'primary' in name:
                self.ui.text_edits_primary[int(name[-1])].setPlainText('\n'.join(data))
            else:
                self.ui.text_edits_secondary[int(name[-1])].setPlainText('\n'.join(data))
        except Exception as e:
            pass

    # simple method that allows to select multiple PDF`s from filesystem
    def select_pdf(self):
        '''get pdf`s file names'''
        caption = 'Open PDF files'
        # use current/working directory
        directory = './'
        # allows to select PDF files only
        filter_mask = "*.pdf"
        # returns all PDF files selected
        self.files, _ = QFileDialog.getOpenFileNames(None,
                                                     caption, directory, filter_mask)

    # simple method that allows to select folder to save csv result

    def select_save_folder(self):
        '''get save folder'''
        # allows to delect folders only
        self.folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        # change text of the label (with current save path)

    # this method invokes when user press 'RUN'
    def parse_run(self):
        # if no files selected - nothing to parse - return
        if self.files == []:
            QMessageBox.information(self, "QMessageBox.information()",
                                    "Please select PDF  file first!")
            return

        patterns = self.patterns

        if True:
            files = self.files
            if self.folder != '':
                folder = self.folder
            else:
                folder = os.path.dirname(files[0])

                # Manger is Thread Manager.
                # pool of threads. We can run code blocks in same time to speed up our parser
                processes = []
            data = {}
            for i in range(7):
                temp = []
                data[i + 1] = [self.ui.text_edits_primary[i].toPlainText().split('\n'),
                               self.ui.text_edits_secondary[i].toPlainText().split('\n'), patterns[i]]
            data[8] =  [[''], [''], '[a-z]+.']
            data[9] = [[''], [''], '[a-z]+.']
            print('data')
            print(data)
            if self.ui.checkbox_type.isChecked():
                try:
                    print('Parsed as a new type')
                    csv_path = os.path.join(folder, 'result.csv')
                    chunks_file = list(chunks(files, 16))
                    with Manager() as manager:
                        L = manager.list()

                        # pool of threads. We can run code blocks in same time to speed up our parser
                        processes = []
                        # creates 1 thread for each file selected
                        for chunk in chunks_file:
                            for filename in chunk:
                                try:
                                    # method to call in multithread mode - prepare_to_parsing
                                    # arguments of prepare_to_parsing - filename and folder
                                    p = Process(target=spec_parser_t2.prepare_to_parsing, args=(filename, folder, L, data))
                                    # start processes
                                    p.start()
                                    processes.append(p)
                                except Exception:
                                    pass
                            for p in processes:
                                p.join()
                        print('!!!!!!!!!')

                        L = [x for x in L]
                        print(L)
                        L.sort(key=lambda x: x[0])
                        L.insert(0, header)

                        json_path = os.path.join(folder, 'result.json')
                        result_json = []
                        for x in L[1:]:
                            temp = {
                                "Specification Section Name": x[0],
                                "Specification Section Number": x[0].split()[0],
                                "Section Name": x[1],
                                "Item Type": x[2],
                                "SubSection Number": x[3],
                                "SubSection Text": x[4]
                            }
                            result_json.append(temp)

                        with open(json_path, 'w') as f:
                            json.dump(result_json, f, indent=4)

                        with open(csv_path, "w",
                                  newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerows(L)
                        QMessageBox.information(self, "QMessageBox.information()",
                                                "Done and saved!")
                except Exception as e:
                    print(traceback.format_exc())

            else:
                try:
                    print('Parsed as an old type')
                    csv_path = os.path.join(folder, 'result.csv')
                    chunks_file = list(chunks(files, 16))
                    with Manager() as manager:
                        L = manager.list()

                        # pool of threads. We can run code blocks in same time to speed up our parser
                        processes = []
                        # creates 1 thread for each file selected
                        for chunk in chunks_file:
                            for filename in chunk:
                                try:
                                    # method to call in multithread mode - prepare_to_parsing
                                    # arguments of prepare_to_parsing - filename and folder
                                    p = Process(target=spec_parser.prepare_to_parsing, args=(filename, folder, L, data))
                                    # start processes
                                    p.start()
                                    processes.append(p)
                                except Exception:
                                    pass
                            for p in processes:
                                p.join()

                        L = [x for x in L]
                        print(L)
                        L.sort(key=lambda x: x[0])
                        L.insert(0, header)
                        json_path = os.path.join(folder, 'result.json')
                        result_json = []
                        for x in L[1:]:
                            temp = {
                                "Specification Section Name": x[0],
                                "Specification Section Number": x[0].split()[0],
                                "Section Name": x[1],
                                "Item Type": x[2],
                                "SubSection Number": x[3],
                                "SubSection Text": x[4]
                            }
                            result_json.append(temp)

                        with open(json_path, 'w') as f:
                            json.dump(result_json, f, indent=4)

                        with open(csv_path, "w",
                                  newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerows(L)
                        QMessageBox.information(self, "QMessageBox.information()",
                                                "Done and saved!")
                except Exception as e:
                    print(traceback.format_exc())


# start point of the script

# we should check if the method is main to call it from other scripts and threds
if __name__ == '__main__':
    # freeze support allows to use multiprocessing on Windows    # Create application object. It`s core and heart of out app
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    w = AppWindow()
    # set backgroundcolour
    w.setStyleSheet("QMainWindow {background: '#a2a3a4';}");
    # show app
    w.show()
    # detroy app when closed
    sys.exit(app.exec_())
