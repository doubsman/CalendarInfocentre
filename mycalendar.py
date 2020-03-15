#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QTableView, QFrame, QHBoxLayout, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime
from mycalendar_model 	import ModelCalendar
from mycalendar_prepare import PrepareOneYear


class ViewCalendar(QMainWindow, ):

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
		self.viewtable = QTableView(self)
		self.viewtable.setModel(model)
		self.viewtable.setSortingEnabled(True)
		# resize all columns to content
		counter = 0
		for col in model.columns:
			self.viewtable.resizeColumnToContents(counter)
			counter += 1
		# gui position
		posco = QHBoxLayout()
		posco.addWidget(self.viewtable)
		self.setCentralWidget(QFrame())
		self.centralWidget().setLayout(posco)
		self.show()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	#cal = ViewCalendar(2021, 'English')
	cal = ViewCalendar()
	sys.exit(app.exec_())