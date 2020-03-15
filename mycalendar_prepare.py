#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QObject
from locale import setlocale, LC_ALL
from calendar import Calendar, MONDAY, SUNDAY
from mycalendar_model import ModelCalendar


class PrepareOneYear(QObject):

	def __init__(self, mylanguage = 'French', parent = None):
		"""Init."""
		super(PrepareOneYear, self).__init__(parent)
		self.parent = parent
		self.cur_year = None
		setlocale(LC_ALL, mylanguage)
		# norme ISO 8601
		self.cal = Calendar(firstweekday=MONDAY)

	def getYear(self, cur_year):
		self.cur_year = cur_year
		self.myCalendar = []
		myCaltempo = []
		# prepare days year
		for cur_month in range(0,12):
			myCaltempo += list(self.cal.itermonthdates(self.cur_year , cur_month + 1))
		# remove duplicate date
		myCaltempo = list(dict.fromkeys(myCaltempo))
		# complete specials days
		for row in myCaltempo:
			rowtab = []
			rowtab.append(row.strftime("%d/%m/%Y"))																				#Date
			rowtab.append(row.strftime('%Y%m%d'))																				#datetime
			rowtab.append(row.strftime('%d'))																					#days
			rowtab.append(row.strftime('%m'))																					#month
			rowtab.append(row.strftime('%Y'))																					#year
			rowtab.append(row.strftime('%w'))																					#WeekDay
			rowtab.append(row.strftime('%U'))																					#Week_number_Sunday
			rowtab.append(row.strftime('%W'))																					#Week_number_Monday
			rowtab.append(row.strftime('%j'))																					#Day_Year
			rowtab.append(row.strftime('%A')+' '+row.strftime('%d')+' '+row.strftime('%B')+' '+row.strftime('%Y'))				#litteral_Date
			rowtab.append(row.strftime('%a')+' '+row.strftime('%d').lstrip('0')+' '+row.strftime('%b')+' '+row.strftime('%y'))	#litteral_Date_short
			rowtab.append(row.strftime('%A'))																					#litteral_Day
			rowtab.append(row.strftime('%a'))																					#litteral_Day_short
			rowtab.append(row.strftime('%B'))																					#litteral_Month
			rowtab.append(row.strftime('%b'))																					#litteral_Month_short
			rowtab.append(self.estferie( [int(row.strftime('%d')) , int(row.strftime('%m')) , int(row.strftime('%Y'))] ))		#feries
			if row.strftime('%Y') == str(cur_year):
				self.myCalendar += [rowtab]
		return self.myCalendar
	
	# http://python.jpvweb.com/python/mesrecettespython/doku.php?id=date_de_paques
	def datepaques(self, an):
		"""Calcule la date de Pâques d'une année donnée an (=nombre entier)"""
		a=an//100
		b=an%100
		c=(3*(a+25))//4
		d=(3*(a+25))%4
		e=(8*(a+11))//25
		f=(5*a+b)%19
		g=(19*f+c-e)%30
		h=(f+11*g)//319
		j=(60*(5-d)+b)//4
		k=(60*(5-d)+b)%4
		m=(2*j-k-g+h)%7
		n=(g-h+m+114)//31
		p=(g-h+m+114)%31
		jour=p+1
		mois=n
		return [jour, mois, an]

	def joursferiesliste(self, an, sd=0):
		"""Liste des jours fériés France en date-liste de l'année an (nb entier).
			sd=0 (=defaut): tous les jours fériés.
			sd=1: idem sans les sammedis-dimanches.
			sd=2: tous + les 2 jours fériés supplémentaires d'Alsace-Moselle.
			sd=3: idem sd=2 sans les samedis-dimanches"""
		F = []  # =liste des dates des jours feries en date-liste d=[j,m,a]
		L = []  # =liste des libelles du jour ferie
		dp = self.datepaques(an)

		# Jour de l'an
		d = [1,1,an]
		nj = self.numjoursem(d)
		if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
			F.append(d)
			L.append(u"Jour de l'an")

		# Vendredi saint (pour l'Alsace-Moselle)
		d = self.jourmoins(dp, -2)
		if sd>=2:
			F.append(d)
			L.append(u"Vendredi saint")

		# Dimanche de Paques
		d = dp
		if (sd==0) or (sd==2):
			F.append(d)
			L.append(u"Dimanche de Pâques")

		# Lundi de Paques
		d = self.jourplus(dp, +1)
		F.append(d)
		L.append(u"Lundi de Pâques")

		# Fête du travail
		d = [1,5,an]
		nj = self.numjoursem(d)
		if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
			F.append(d)
			L.append(u"Fête du travail")

		# Victoire des allies 1945
		d = [8,5,an]
		nj = self.numjoursem(d)
		if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
			F.append(d)
			L.append(u"Victoire des alliés 1945")

		# Jeudi de l'Ascension
		d = self.jourplus(dp, +39)
		F.append(d)
		L.append(u"Jeudi de l'Ascension")

		# Dimanche de Pentecote
		d = self.jourplus(dp, +49)
		if (sd==0) or (sd==2):
			F.append(d)
			L.append(u"Dimanche de Pentecôte")

		# Lundi de Pentecote
		d = self.jourplus(d, +1)
		F.append(d)
		L.append(u"Lundi de Pentecôte")

		# Fete Nationale
		d = [14,7,an]
		nj = self.numjoursem(d)
		if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
			F.append(d)
			L.append(u"Fête Nationale")

		# Assomption
		d = [15,8,an]
		nj = self.numjoursem(d)
		if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
			F.append(d)
			L.append(u"Assomption")

		# Toussaint
		d = [1,11,an]
		nj = self.numjoursem(d)
		if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
			F.append(d)
			L.append(u"Toussaint")

		# Armistice 1918
		d = [11,11,an]
		nj = self.numjoursem(d)
		if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
			F.append(d)
			L.append(u"Armistice 1918")

		# Jour de Noel
		d = [25,12,an]
		nj = self.numjoursem(d)
		if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
			F.append(d)
			L.append(u"Jour de Noël")

		# Saint Etienne (pour l'Alsace-Moselle)
		d = [26,12,an]
		nj = self.numjoursem(d)
		if (sd==2) or (sd==3 and nj<6):
			F.append(d)
			L.append(u"Saint Etienne")

		return F, L

	def estferie(self, d, sd=0):
		"""estferie(d,sd=0): => dit si une date d=[j,m,a] donnée est fériée France
		si la date est fériée, renvoie son libellé
		sinon, renvoie une chaine vide
		F, J, L = joursferies(2009,0,'/')
		for i in range(0,len(F)):
		print F[i], "%10s" % (J[i]), L[i]"""
		j,m,a = d
		F, L = self.joursferiesliste(a, sd)
		for i in range(0, len(F)):
			if j==F[i][0] and m==F[i][1] and a==F[i][2]:
				return L[i]
		return ""

	def joursferies(self, an, sd=0, sep='/'):
		"""Liste des jours fériés France en date-chaine de l'année an (nb entier).
			sd=0 (=defaut): tous les jours fériés.
			sd=1: idem sans les sammedis-dimanches.
			sd=2: tous + les 2 jours fériés supplémentaires d'Alsace-Moselle.
			sd=3: idem sd=2 sans les samedis-dimanches"""
		C = []
		J = []
		F, L = self.joursferiesliste(an, sd)
		for i in range(0,len(F)):
			C.append(datechaine(F[i]))  # conversion des dates-liste en dates-chaine
			J.append(joursem(F[i]))  # ajout du jour de semaine
		return C, J, L
		#Exemple d'utilisation: tous les jours fériés (sd=0, valeur par défaut)
		#F, J, L = joursferies(2009,0,'/')
		#for i in range(0,len(F)):
		#print F[i], "%10s" % (J[i]), L[i]

	def numjoursem(self, d):
		"""Donne le numéro du jour de la semaine d'une date d=[j,m,a]
			lundi=1, mardi=2, ..., dimanche=7
			Algorithme de Maurice Kraitchik (1882–1957)"""
		j, m, a = d
		if m<3:
			m += 12
			a -= 1
		n = (j +2*m + (3*(m+1))//5 +a + a//4 - a//100 + a//400 +2) % 7
		return [6, 7, 1, 2, 3, 4, 5][n]

	def joursem(self, d):
		"""Donne le jour de semaine en texte à partir de son numéro
		lundi=1, mardi=2, ..., dimanche=7"""
		return ["", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
				"dimanche"][numjoursem(d)]

	def jourmoins(self, d, n=-1):
		"""Donne la date du nième jour précédent d=[j, m, a] (n<=0)"""
		j, m, a = d
		fm = [0,31,28,31,30,31,30,31,31,30,31,30,31]
		if (a%4==0 and a%100!=0) or a%400==0:  # bissextile?
			fm[2] = 29
		for i in range(0,abs(n)):
			j -= 1
			if j < 1:
				m -= 1
				if m<1:
					m = 12
					a -= 1
				j = fm[m]
		return [j,m,a]

	def jourplus(self, d, n=1):
		"""Donne la date du nième jour suivant d=[j, m, a] (n>=0)"""
		j, m, a = d
		fm = [0,31,28,31,30,31,30,31,31,30,31,30,31]
		if (a%4==0 and a%100!=0) or a%400==0:  # bissextile?
			fm[2] = 29
		for i in range(0,n):
			j += 1
			if j > fm[m]:
				j = 1
				m += 1
				if m>12:
					m = 1
					a += 1
		return [j,m,a]