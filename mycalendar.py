#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QTableView, QFrame, QHBoxLayout, QWidget, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDateTime, QPoint
from mycalendar_model 	import ModelCalendar
from mycalendar_prepare import PrepareOneYear
from mycalendar_proxy import ProxyCalendar


class ViewCalendar(QWidget):

	def __init__(self, year = None, mylanguage = 'French', parent = None):
		super(ViewCalendar, self).__init__()

		self.setWindowTitle(u"Calendrier InfoCentre")
		self.setWindowIcon(QIcon('mycalendar.ico'))
		self.resize(1500, 900)

		# curent year default
		if year is None:
			year = int(QDateTime.currentDateTime().toString('yyyy'))
		# create result
		self.classcal = PrepareOneYear(mylanguage)
		self.arraycal = self.classcal.getYear(year)
		# apply to model
		model = ModelCalendar(self.arraycal)
		# sort columns
		proxy = ProxyCalendar()
		proxy.setSourceModel(model)
		self.viewtable = QTableView(self)
		self.viewtable.setSortingEnabled(True)
		self.viewtable.setAlternatingRowColors(True)
		self.viewtable.setModel(proxy)
		# resize all columns to content
		counter = 0
		for col in model.columns:
			self.viewtable.resizeColumnToContents(counter)
			counter += 1
		#popup header albums
		self.resHeaderMenu = QMenu(self)
		header = self.viewtable.horizontalHeader()
		header.setContextMenuPolicy(Qt.CustomContextMenu)
		header.customContextMenuRequested.connect(self.headerRightClicked)
		# build pop-up menu header columns name
		for column in range(proxy.columnCount()):
			columnName = proxy.headerData(column, Qt.Horizontal).value()
			actn = QAction('%s'%columnName, self.resHeaderMenu, checkable = True)
			actn.setChecked(True)
			actn.triggered.connect(self.resHeaderMenuTriggered)
			self.resHeaderMenu.addAction(actn)
		# gui position
		posco = QHBoxLayout()
		posco.addWidget(self.viewtable)
		#self.setCentralWidget(QFrame())
		self.setLayout(posco)
		self.show()

	def headerRightClicked(self, QPos):
		parentPosition = self.viewtable.mapToGlobal(QPoint(0, 0))
		menuPosition = parentPosition + QPos
		self.resHeaderMenu.move(menuPosition)
		self.resHeaderMenu.show()	

	def resHeaderMenuTriggered(self, arg):
		for i, actn in enumerate(self.resHeaderMenu.actions()):
			if not actn.isChecked():
				self.viewtable.setColumnHidden(i, True)
			else:
				self.viewtable.setColumnHidden(i, False)

# languages
LANGUAGES = {
    'bg_BG': 'Bulgarian',
    'cs_CZ': 'Czech',
    'da_DK': 'Danish',
    'de_DE': 'German',
    'el_GR': 'Greek',
    'en_US': 'English',
    'es_ES': 'Spanish',
    'et_EE': 'Estonian',
    'fi_FI': 'Finnish',
    'fr_FR': 'French',
    'hr_HR': 'Croatian',
    'hu_HU': 'Hungarian',
    'it_IT': 'Italian',
    'lt_LT': 'Lithuanian',
    'lv_LV': 'Latvian',
    'nl_NL': 'Dutch',
    'no_NO': 'Norwegian',
    'pl_PL': 'Polish',
    'pt_PT': 'Portuguese',
    'ro_RO': 'Romanian',
    'ru_RU': 'Russian',
    'sk_SK': 'Slovak',
    'sl_SI': 'Slovenian',
    'sv_SE': 'Swedish',
    'tr_TR': 'Turkish',
    'zh_CN': 'Chinese',
}

if __name__ == "__main__":
	app = QApplication(sys.argv)
	#cal = ViewCalendar(2021, 'English')
	cal = ViewCalendar()
	sys.exit(app.exec_())