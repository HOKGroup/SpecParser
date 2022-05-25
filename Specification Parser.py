import sys
from PyQt5.QtWidgets import *
from gui_v2 import Ui_MainWindow
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
Before we get started I would like to talk about the general principle of parsing PDF.
So PDF document consists of elements - text elements and some graphic elements.
We are interested in the text elements.
Each element has coordinates - X and Y. like [600, 300] 600 - X coord, and 300 is Y coord
Our task is to determine patterns of similar arrangement of elements for our set of documents


Next we will work with the text object.
it looks like this
a
el = [[X, Y] 'Sometext'] 

so 
el[0][0] is X
el[0][1] is Y
el[1] is TEXT
Please, remember about it

"""

# list to stoe text object described earlier like [[X, Y] 'Sometext']
ListOfStrings = []


def checkString(str):
    # intializing flag variable
    flag_n = False

    # given string
    for i in str:
        # if string has number
        if i.isdigit():
            flag_n = True

    # returning and of flag
    # for checking required condition
    return flag_n


class PdfPositionHandling:
    """
    The purpose of this method is to add quotation marks to values that contain commas.
    imagine that we have values 'apples, pies'
    In this case, any csv editor will interpret this as 2 columns.
    To avoid this we need to add qoutations = "apples, pies"

    (NB)

    This action can be done using the csv core library. (import csv)
    I prefer to do it manually because this module sometimes behaves unpredictably
    """

    def add_quotes_to_list(self, start_list):
        '''Add qutes to records with ',' inside '''
        for item in start_list:
            for index in range(0, len(item)):
                # add qoutation to value if comma in value
                if ',' in str(item[index]):
                    item[index] = '"' + str(item[index]).replace(',', '') + '"'
        return start_list

    """
    forms a csv-like string from a 2d array

    (NB) 

    This action can be done using the csv core library. (import csv)
    I prefer to do it manually because this module sometimes behaves unpredictably
    """

    def create_csv(self, result_list, folder, save_name, start_string):
        '''Save csv to filesystem. selected folder'''
        result_string = start_string
        for a in result_list:
            # ['A', 'B', 'C'] to 'A,B,C'
            result_string += str(','.join(a))
            result_string += '\n'
        # save csv-file itself

        cvs_result = open(folder + '/' + str(save_name),
                          'w', encoding='utf-8')
        cvs_result.write(result_string)
        cvs_result.close()

    # looking for text objects
    # self, lt_objs is a set of PDF text and graphical objects
    # we should find text only and store X and Y coords
    def parse_obj(self, lt_objs, i):
        '''parse pdf elements to python list'''

        for obj in lt_objs:
            # if object is text - add new Text pdf object (like [[X, Y] 'Sometext']  to ListOfStrings)
            if isinstance(obj, LTTextLine):
                for char in obj:
                    font = char.fontname
                    charsize = int(char.size) * 72 / 96
                    break
                if 50 < int(obj.bbox[1]) < 715:
                    if 69 < int(obj.bbox[0]) < 73:
                        if any([x for x in obj.get_text().replace('\n', ' ').strip() if
                                x.isalpha() and x.islower()]) or 'SECTION ' in obj.get_text().replace('\n',
                                                                                                      ' ').strip() or 'TIPS:' in obj.get_text().replace(
                            '\n', ' ').strip():
                            continue
                        # and not any([x for x in obj.get_text().replace('\n', ' ').strip() if x.lower()]):

                    ListOfStrings.append([[int(obj.bbox[0]), int(obj.bbox[1])],
                                          obj.get_text().replace('\n', ' ').strip()])

            # if object is not Text - looking for Text objects in non-Text objects recursive
            if isinstance(obj, LTTextBoxHorizontal):
                self.parse_obj(obj._objs, i)
            elif isinstance(obj, LTFigure):
                self.parse_obj(obj._objs, i)

    def parse_pdf(self, file_name, start_page, end_page, save_folder, L, data):
        try:
            '''parse pdf to list of lists and save to csv'''
            # create object of PDF parser (pdfminersix lib)

            print(file_name)
            fp = open(file_name, 'rb')
            parser = PDFParser(fp)
            document = PDFDocument(parser)

            # if document is blocked - return
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed

            # some pdfminersix routine, Creates interpreter object
            rsrcmgr = PDFResourceManager()
            device = PDFDevice(rsrcmgr)
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # i in number of page
            i = 0
            result = []
            for page in PDFPage.create_pages(document):
                try:
                    # start page and end page is 2 last pages
                    # if page is not in 2 lat - ignore page
                    if start_page <= i <= end_page:
                        # cretes layout. layout is a set of PDF text and graphical objects (like [[X, Y] 'Sometext'] )
                        interpreter.process_page(page)
                        layout = device.get_result()

                        # look for text objects
                        self.parse_obj(layout._objs, i)
                    i += 1
                    print("PAGE: {}".format(i))
                    ListOfStrings.sort(key=lambda x: (-x[0][1], x[0][0]))
                    temp = [''] * len(header)

                    lvls_dict = {72: 1, 86: 2, 115: 3, 144: 4}
                    index_first = False
                    if not ListOfStrings:
                        continue
                    a = ListOfStrings[0]
                    if not ((69 < a[0][0] < 73 and 'PART' in a[1]) or (69 < a[0][0] < 73) or (
                            len(a[1]) < 5 and (a[1][-1] == '.'))):
                        try:
                            value = []
                            for x in ListOfStrings:
                                if (69 < x[0][0] < 73) or (len(x[1]) < 5 and (x[1][-1] == '.')):
                                    break
                                else:
                                    value.append(x[1])
                            value = ' '.join(value)
                            print('VALUE')
                            print(result)
                            print(value)
                            result[-1][-1] = result[-1][-1] + ' ' + value
                        except Exception:
                            pass

                    for a in ListOfStrings:
                        if 69 < a[0][0] < 73 and 'PART' in a[1]:
                            result.append([0+1, a[1], a[1]])
                        elif ((69 < a[0][0] < 73) and len(a[1]) < 5) or (len(a[1]) < 4 and (a[1][-1] == '.')):
                            value = []
                            for x in ListOfStrings[ListOfStrings.index(a) + 1:]:
                                if ((69 < x[0][0] < 73) and len(x[1]) < 5) or (len(x[1]) < 4 and (x[1][-1] == '.')):
                                    break
                                else:
                                    value.append(x[1])
                            value = ' '.join(value)
                            result.append([lvls_dict[a[0][0]]+1, a[1], value])

                    ListOfStrings.clear()
                except Exception:
                    ListOfStrings.clear()


            result = [x for x in result if re.search(r"{}".format(data[x[0]][2].strip()), x[1].strip())]

            indexes = ['', '', '', '', '', '', '']
            for c in result:
                if c[0] !=1:
                    indexes[c[0]] = c[1]
                    for x in range(c[0]+1, 6):
                        indexes[x] = ''
                    result[result.index(c)][1] = '-'.join([x for x in indexes if x])

            with open(os.path.join(save_folder, os.path.basename(file_name).lower().replace('.pdf', '.csv')), "w",
                      newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(result)

            result_searches = []
            for x in result:
                    level = x[0]
                    level_primaries = [x for x in data[level][0]]
                    level_sec = [x.lower() for x in data[level][1]]
                    print('+')
                    print(level_primaries)
                    print(level_sec)
                    if not level_primaries:
                        return
                    detected_lp = ''
                    for lp in level_primaries:
                        if lp.lower() in x[2].lower():
                            detected_lp = lp

                    if detected_lp:
                        print('LP')
                        print(detected_lp)
                        print(x[1])
                        category = x[1].split('-')[0]
                        if category:
                            print("FN")
                            print(file_name)
                            print(category)
                            try:
                                category_name = [d[2] for d in result if d[1] == category][0]
                                if [os.path.basename(file_name), detected_lp, '', x[1], x[2]] not in L:
                                    L.append([os.path.basename(file_name), detected_lp, '', x[1], x[2]])
                            except Exception:
                                print(traceback.format_exc())
                                exit(0)
                            print(L)

                        else:
                            if [os.path.basename(file_name), detected_lp, '', x[1], x[2]]  not in L:
                                L.append([os.path.basename(file_name), detected_lp, '', x[1], x[2]])
                        print("CATEGORY")
                        print(category)
                        if level_sec:
                            if category:
                                childs = [d for d in result if x[1] in d[1]]
                                for c in childs:
                                    detected_sec = []
                                    for ls in level_sec:
                                        if ls.lower() in c[2].lower():
                                            detected_sec.append(ls)
                                    if [os.path.basename(file_name), detected_lp, '', c[1], c[2]] in L:
                                        L.remove([os.path.basename(file_name), detected_lp, '', c[1], c[2]])
                                    if [os.path.basename(file_name), detected_lp, ','.join(detected_sec), c[1], c[2]] not in L:
                                        L.append([os.path.basename(file_name), detected_lp, ','.join(detected_sec), c[1], c[2]])
            return result_searches
        except Exception:
            print(traceback.format_exc())

    def add_row(self, current_paragraph, current_part, current_section, current_spec, current_text, result,
                section_name):
        temp = [current_spec, current_part.lower().capitalize(), current_section, section_name.lower().capitalize(),
                current_paragraph, ' '.join(current_text), '', '',
                '']
        result.append(temp)
        temp = [''] * 9
        current_text = []
        return current_text


# it`s a first method called in multithread mode
# So if we selected 5 files, we run 5 methods in the same time
# genereal purpose of method is define page numbers to parse.
def prepare_to_parsing(file_name, folder, L, data):
    '''get`s pdf 2 last page values'''
    # create object of PdfPositionHandling of pdfminerlib - tool to parse PDF
    pdf_handler = PdfPositionHandling()
    # open PDF file
    file = open(file_name, 'rb')
    # read pdF content with parser and create document object
    parser = PDFParser(file)
    document = PDFDocument(parser)
    # get lenth of PDF in page
    len_of_pdf = resolve1(document.catalog['Pages'])['Count']
    # We need 2 last pages only, so len_of_pdf - 2, len_of_pdf - 1 is a range of pages to parse - 2 last pages
    # rin parse_pdf
    return pdf_handler.parse_pdf(file_name, 0, 10000, folder, L, data)


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
        #self.ui.text_edit.clicked.connect(self.select_txt)
        self.text_files = []
        self.ui.selectSaveFolder.clicked.connect(self.select_save_folder)
        self.ui.runButton.clicked.connect(self.parse_run)
        self.ui.closeButton.clicked.connect(self.shutprocess)
        self.ui.selectPS.clicked.connect(self.selectPS)
        self.ui.selectSS.clicked.connect(self.selectSS)
        #self.ui.saveButton.clicked.connect(self.save_pattern)
        self.ui.loadButton.clicked.connect(self.load_pattern)

        with open('primary.json', 'r') as f:
            data = json.load(f)
        i = 0
        for x in self.ui.text_edits_primary:

            x.setPlainText('\n'.join(list(data.values())[i]))
            i+=1

        with open('secondary.json', 'r') as f:
            data = json.load(f)
        i = 0
        for x in self.ui.text_edits_secondary:

            x.setPlainText('\n'.join(list(data.values())[i]))
            i+=1

        with open('regex.json', 'r') as f:
            data = json.load(f)
        i = 0
        for x in self.ui.text_edits:
            x.setText(list(data.values())[i]["comment"])
            i+=1
        self.patterns = [x["regex"] for x in list(data.values())]
        print(self.patterns)

        # show gui
        self.show()

    def selectPS(self):
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
            i+=1




    def selectSS(self):
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
            i+=1

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
        for x in self.ui.text_edits:
            x.setText(list(data.values())[i]["comment"])
            i+=1
        self.patterns = [x["regex"] for x in list(data.values())]
        print(self.patterns)

    def shutprocess(self):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            print('Window closed')
        else:
            pass

    # simple method that allows to select multiple PDF`s from filesystem
    def select_txt(self):
        '''get pdf`s file names'''
        caption = 'Open txt file file with seach words line by line'
        # use current/working directory
        directory = './'
        # allows to select TXT files only
        filter_mask = "*.txt"
        # returns all PDF files selected
        self.text_files, _ = QFileDialog.getOpenFileName(None,
                                                     caption, directory, filter_mask)
        print(self.text_files)



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
                data[i+1] = [self.ui.text_edits_primary[i].toPlainText().split('\n'),self.ui.text_edits_secondary[i].toPlainText().split('\n'), patterns[i]]
            print(data)

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
                            p = Process(target=prepare_to_parsing, args=(filename, folder, L, data))
                            # start processes
                            p.start()
                            processes.append(p)
                        except Exception:
                            pass
                    for p in processes:
                        p.join()
                L = [x for x in L]
                L.sort(key=lambda x: x[0])
                L.insert(0, header)

                with open(csv_path, "w",
                          newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(L)
                QMessageBox.information(self, "QMessageBox.information()",
                                        "Done and saved!")


# start point of the script

# we should check if the method is main to call it from other scripts and threds
if __name__ == '__main__':
    # freeze support allows to use multiprocessing on Windows    # Create application object. It`s core and heart of out app
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    w = AppWindow()
    # set backgroundcolour
    w.setStyleSheet("QMainWindow {background: '#C2efC4';}");
    # show app
    w.show()
    # detroy app when closed
    sys.exit(app.exec_())
