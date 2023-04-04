import random
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

# list to store text object described earlier like [[X, Y] 'Sometext']
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
                if 50 < int(obj.bbox[0]) and  55 < int(obj.bbox[1]):
                    """
                    if 69 < int(obj.bbox[0]) < 73:
                        if any([x for x in obj.get_text().replace('\n', ' ').strip() if
                                x.isalpha() and x.islower()]) or 'SECTION ' in obj.get_text().replace('\n',
                                                                                                      ' ').strip() or 'TIPS:' in obj.get_text().replace(
                            '\n', ' ').strip():
                            continue
                        # and not any([x for x in obj.get_text().replace('\n', ' ').strip() if x.lower()]):
                    """
                    if obj.get_text().replace('\n', ' ').strip():
                        if 'bold' in font.lower():
                            font = 'BOLD'
                        else:
                            font = 'regular'
                        ListOfStrings.append([[int(obj.bbox[0]), int(obj.bbox[1]), int(obj.bbox[2])],
                                              obj.get_text().replace('\n', ' ').strip(), font])

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

            levels = []

            for page in PDFPage.create_pages(document):

                    # start page and end page is 2 last pages
                    # if page is not in 2 lat - ignore page
                    if start_page <= i <= end_page:
                        # cretes layout. layout is a set of PDF text and graphical objects (like [[X, Y] 'Sometext'] )
                        interpreter.process_page(page)
                        layout = device.get_result()

                        # look for text objects
                        self.parse_obj(layout._objs, i)
                    i += 1
                    ListOfStrings.sort(key=lambda x: (-x[0][1], x[0][0]))
                    temp = [''] * len(header)

                    lvls_dict = {72: 1, 86: 2, 115: 3, 144: 4}
                    index_first = False
                    finals = [ListOfStrings[0]]
                    for a in ListOfStrings[1:]:
                        prev = ListOfStrings[ListOfStrings.index(a)-1]
                        if a[0][1] == prev[0][1]:
                            finals[-1][1] += ' ' + a[1]
                        elif a[0][0] != prev[0][0]:
                            finals.append(a)
                        elif prev[0][1] - a[0][1] > 15:
                            finals.append(a)
                        elif (prev[0][2] > 500 and a[1][0].islower())  or (prev[1].strip()[-1].isalpha() and prev[1].strip()[-1].islower() and  len(a[1])<18) or prev[0][2] > 540:
                            finals[-1][1] += ' ' + a[1]
                        else:
                            finals.append(a)

                    verticals = list(set([x[0][0] for x in finals]))
                    ListOfStrings.clear()
                    verticals.sort()
                    for v in verticals:
                        if v not in levels and v-1 not in levels  and v+1 not in levels:
                            levels.append(v)
            levels.sort()
            print(levels)
            i = 0
            part = 0
            section = 0
            lvl_list = [0, 0, 0, 0, 0,  0, 0, 0, 0,  0, 0]
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
                    print("PAGE: {}, {}".format(i, file_name))
                    ListOfStrings.sort(key=lambda x: (-x[0][1], x[0][0]))

                    for index in range(len(ListOfStrings)):
                        if ListOfStrings[index][0][0] -1 in levels:
                            ListOfStrings[index][0][0] = ListOfStrings[index][0][0] -1
                        if ListOfStrings[index][0][0] +1 in levels:
                            ListOfStrings[index][0][0] = ListOfStrings[index][0][0] +1
                    temp = [''] * len(header)
                    lvls_dict = {}
                    for l in levels:
                        lvls_dict[l] = levels.index(l)+1
                    index_first = False
                    finals = [ListOfStrings[0]]
                    for a in ListOfStrings[1:]:
                        prev = ListOfStrings[ListOfStrings.index(a)-1]
                        if a[0][1] == prev[0][1]:
                            finals[-1][1] += ' ' + a[1]
                        elif a[0][0] != prev[0][0]:
                            finals.append(a)
                        elif prev[0][1] - a[0][1] > 15:
                            finals.append(a)
                        elif (prev[0][2] > 500 and a[1][0].islower())  or (prev[1].strip()[-1].isalpha() and prev[1].strip()[-1].islower() and  len(a[1])<18) or prev[0][2] > 540:
                            finals[-1][1] += ' ' + a[1]
                        else:
                            finals.append(a)


                    if not finals:
                        continue


                    for a in finals:
                        if 'SECTION ' in a[1]:
                            continue
                        if a[2].lower() == 'bold' and a[1].strip().replace('PART 2 - ', '').replace('PART 1 - ', '').replace('PART 3 - ', '').replace('PART 4 - ', '') in ['GENERAL', 'PRODUCTS', "EXECUTION"]:
                            part+=1
                            section = 0
                            res = a[1].strip().replace('PART 2 - ', '').replace('PART 1 - ', '').replace('PART 3 - ', '').replace('PART 4 - ', '')
                            result.append([0 + 1, res, res])
                        elif a[2].lower() == 'bold' and a[1].strip() not in ['GENERAL', 'PRODUCTS', "EXECUTION"]:
                            section +=1
                            result.append([2, '{}.{}'.format(part,section), a[1]])
                            for x in range(2, len(lvl_list) - 1):
                                lvl_list[x] = 0
                        else:

                            if 86 in levels:
                                lvl_list[lvls_dict[a[0][0]] + 1] +=1
                                result.append([lvls_dict[a[0][0]] + 1, str(lvl_list[lvls_dict[a[0][0]] + 1]), a[1]])
                                for x in range(lvls_dict[a[0][0]] + 2, len(lvl_list)-1):
                                    lvl_list[x] = 0
                            else:
                                lvl_list[lvls_dict[a[0][0]] + 2] += 1
                                result.append([lvls_dict[a[0][0]] + 2, str(lvl_list[lvls_dict[a[0][0]] + 2]),  a[1]])

                                for x in range(lvls_dict[a[0][0]] + 3, len(lvl_list) - 1):
                                    lvl_list[x] = 0

                    ListOfStrings.clear()
                except Exception:
                    print("Exception in file: {}".format(file_name))
                    print(traceback.format_exc())
                    ListOfStrings.clear()

            #result = [x for x in result if re.search(r"{}".format(data[x[0]][2].strip()), x[1].strip())]

            indexes = ['', '', '', '', '', '', '', '', '']
            for c in result:
                if c[0] != 1:
                    indexes[c[0]] = c[1]
                    for x in range(c[0] + 1, 8):
                        indexes[x] = ''
                    result[result.index(c)][1] = '-'.join([x for x in indexes if x])

            with open(os.path.join(save_folder, os.path.basename(file_name).lower().replace('.pdf', '.csv')), "w",
                      newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(result)
            result_searches = self.postprocess_results(L, data, file_name, result)
            return result_searches

        except Exception:
            print("Exception in file: {}".format(file_name))
            print(traceback.format_exc())

    def postprocess_results(self, L, data, file_name, result):
        result_searches = []
        for x in result:

            level = x[0]
            if level != 2:
                continue
            for level in range(1, 5):
                level_primaries = [x for x in data[level][0]]
                level_sec = [x.lower() for x in data[level][1]]
                if not level_primaries:
                    return
                detected_lp = ''
                for lp in level_primaries:
                    if lp.lower() in x[2].lower():
                        detected_lp = lp

                if detected_lp:
                    category = x[1].split('-')[0]
                    if category:
                        try:
                            category_name = [d[2] for d in result if d[1] == category][0]
                            if [os.path.basename(file_name), detected_lp, '', x[1], x[2]] not in L:
                                L.append([os.path.basename(file_name), detected_lp, '', x[1], x[2]])
                        except Exception:
                            print(traceback.format_exc())
                            exit(0)

                    else:
                        if [os.path.basename(file_name), detected_lp, '', x[1], x[2]] not in L:
                            L.append([os.path.basename(file_name), detected_lp, '', x[1], x[2]])
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
                                if [os.path.basename(file_name), detected_lp, ','.join(detected_sec), c[1],
                                    c[2]] not in L:
                                    L.append(
                                        [os.path.basename(file_name), detected_lp, ','.join(detected_sec), c[1], c[2]])
        print(result_searches)
        return result_searches


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
