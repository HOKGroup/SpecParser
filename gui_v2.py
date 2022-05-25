# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

"""
This is the GUI code.
I did not write it by hand
To create one you should install Qtcreator, then import .ui into .py
"""


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(980, 660)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selectPDF = QtWidgets.QPushButton(self.centralwidget)
        self.selectPDF.setGeometry(QtCore.QRect(20, 20, 140, 41))
        self.selectPDF.setObjectName("selectPDF")
        self.selectSaveFolder = QtWidgets.QPushButton(self.centralwidget)
        self.selectSaveFolder.setGeometry(QtCore.QRect(169, 20, 140, 41))
        self.selectSaveFolder.setObjectName("selectSaveFolder")

        self.selectPS = QtWidgets.QPushButton(self.centralwidget)
        self.selectPS.setGeometry(QtCore.QRect(345, 20, 250, 41))
        self.selectPS.setObjectName("selectPS")

        self.selectSS = QtWidgets.QPushButton(self.centralwidget)
        self.selectSS.setGeometry(QtCore.QRect(645, 20, 250, 41))
        self.selectSS.setObjectName("selectSS")

        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(800,565, 140, 41))
        self.runButton.setObjectName("runButton")


        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(650,565, 140, 41))
        self.closeButton.setObjectName("closeButton")

        """
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(20,565, 140, 41))
        self.saveButton.setObjectName("saveButton")
        """


        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(20,565, 140, 41))
        self.loadButton.setObjectName("loadButton")



        self.labelPATH = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH.setGeometry(QtCore.QRect(320, 25, 251, 20))
        self.labelPATH.setObjectName("labelPATH")


        self.pr_s = QtWidgets.QLabel(self.centralwidget)
        self.pr_s.setGeometry(QtCore.QRect(418, 70, 251, 20))
        self.pr_s.setObjectName("pr_s")

        self.se_s = QtWidgets.QLabel(self.centralwidget)
        self.se_s.setGeometry(QtCore.QRect(710, 70, 251, 20))
        self.se_s.setObjectName("pr_s")

        self.labelPATH1 = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH1.setGeometry(QtCore.QRect(30, 100, 251, 20))
        self.labelPATH1.setObjectName("labelPATH1")

        self.labelPATH2 = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH2.setGeometry(QtCore.QRect(30, 165, 251, 20))
        self.labelPATH2.setObjectName("labelPATH2")

        self.labelPATH3 = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH3.setGeometry(QtCore.QRect(30, 230, 251, 20))
        self.labelPATH3.setObjectName("labelPATH3")

        self.labelPATH4 = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH4.setGeometry(QtCore.QRect(30, 295, 251, 20))
        self.labelPATH4.setObjectName("labelPATH4")

        self.labelPATH5 = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH5.setGeometry(QtCore.QRect(30, 360, 251, 20))
        self.labelPATH5.setObjectName("labelPATH5")

        self.labelPATH6 = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH6.setGeometry(QtCore.QRect(30, 425, 251, 20))
        self.labelPATH6.setObjectName("labelPATH6")

        self.labelPATH7 = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH7.setGeometry(QtCore.QRect(30, 490, 251, 20))
        self.labelPATH7.setObjectName("labelPATH7")

        """
        self.text_edits = []
        for i in range(7):
            temp = QtWidgets.QPlainTextEdit(self.centralwidget)
            temp.setGeometry(QtCore.QRect(145, 100 + 65*i, 150, 35))
            temp.setObjectName("input{}".format(i))
            self.text_edits.append(temp)
        """

        self.text_edits = []
        for i in range(7):
            temp = QtWidgets.QLabel(self.centralwidget)
            temp.setGeometry(QtCore.QRect(145, 97 + 65*i, 200, 42))
            temp.setObjectName("label{}".format(i))
            self.text_edits.append(temp)

        self.text_edits_primary = []
        for i in range(7):
            temp = QtWidgets.QPlainTextEdit(self.centralwidget)
            temp.setGeometry(QtCore.QRect(345, 100 + 65*i, 250, 56))
            temp.setObjectName("input{}".format(i))
            self.text_edits_primary.append(temp)

        self.text_edits_secondary = []
        for i in range(7):
            temp = QtWidgets.QPlainTextEdit(self.centralwidget)
            temp.setGeometry(QtCore.QRect(645, 100 + 65*i, 250, 56))
            temp.setObjectName("input_sec{}".format(i))
            self.text_edits_secondary.append(temp)



        #self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        #elf.checkBox.setGeometry(QtCore.QRect(30, 110, 171, 20))
        #self.checkBox.setObjectName("checkBox")

        """
        self.cb = QtWidgets.QComboBox(self.centralwidget)
        self.cb.setGeometry(QtCore.QRect(155, 175, 141, 60))
        self.cb.setObjectName("cb")
        self.cb.addItem("Show primary searched")
        self.cb.addItem("1")
        self.cb.addItem("2")
        self.cb.addItem("3")
        self.cb.addItem("4")
        self.cb.setCurrentIndex(3)
        """""


        """
        self.centralwidget.setObjectName("text_edit")
        
        self.text_edit = QtWidgets.QPushButton(self.centralwidget)
        self.text_edit.setGeometry(QtCore.QRect(20, 140, 271, 41))
        self.text_edit.setObjectName("text_edit")
        """

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Specification Parser"))
        self.selectPDF.setText(_translate("MainWindow", "Select PDFs"))
        self.selectPS.setText(_translate("MainWindow", "Select Primary Search Text"))
        self.selectSS.setText(_translate("MainWindow", "Select Secondary Search Text"))
        self.selectSaveFolder.setText(_translate("MainWindow", "Output Location"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.closeButton.setText(_translate("MainWindow", "Close"))

        #self.saveButton.setText(_translate("MainWindow", "Save Pattern"))
        self.loadButton.setText(_translate("MainWindow", "Load Pattern"))


        #self.labelPATH.setText(_translate("MainWindow", "Save PATH: default pdf location"))

        self.labelPATH1.setText(_translate("MainWindow", "Level 1 Pattern"))
        self.labelPATH2.setText(_translate("MainWindow", "Level 2 Pattern"))
        self.labelPATH3.setText(_translate("MainWindow", "Level 3 Pattern"))
        self.labelPATH4.setText(_translate("MainWindow", "Level 4 Pattern"))
        self.labelPATH5.setText(_translate("MainWindow", "Level 5 Pattern"))
        self.labelPATH6.setText(_translate("MainWindow", "Level 6 Pattern"))
        self.labelPATH7.setText(_translate("MainWindow", "Level 7 Pattern"))
        self.text_edits[0].setText(_translate("MainWindow", ""))
        self.text_edits[1].setText(_translate("MainWindow", ""))
        self.text_edits[2].setText(_translate("MainWindow", ""))
        self.text_edits[3].setText(_translate("MainWindow", ""))
        self.text_edits[4].setText(_translate("MainWindow", ""))
        self.text_edits[5].setText(_translate("MainWindow", ""))
        #self.text_edits[6].setText(_translate("MainWindow", "Level 7 \nPattern"))

        self.pr_s.setText(_translate("MainWindow", "Primary search"))
        self.se_s.setText(_translate("MainWindow", "Secondary search"))

