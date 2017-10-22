#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports

import os, sys, configparser
from os.path import expanduser
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog

# Chargement options

config = configparser.ConfigParser()
config.read('pysauv.ini')

dossierSource = expanduser("~")
try:
	dossierDestination = config['options']['destination']
except:
	config.add_section('options')
	dossierDestination = ''

options = '-av --del'

# Liste Python des dossiers

listeDossiers = []
for i in os.listdir(dossierSource):
	if not i.startswith('.') and os.path.isfile(dossierSource+"/"+i) != 1:
		listeDossiers.append(i)

# Slots des boutons Qt

def fermer():
	sys.exit()
	
def sauv():
	dossier = str(liste.currentItem().text())
	if dossier == '[Sauvegarde totale]':
		os.system('xterm -T "Sauvegarde en cours..." -e "rsync '+options+' \\"'+dossierSource+'\\" \\"'+dossierDestination+'\\""')
	else:
		os.system('xterm -T "Sauvegarde en cours..." -e "rsync '+options+' \\"'+dossierSource+dossier+'/\\" \\"'+dossierDestination+dossier+'/\\""')	
	sys.exit()

def askDestination():
	dest_dialog = QFileDialog.getExistingDirectory(win, 'Emplacement de la sauvegarde', expanduser("~"), QFileDialog.ShowDirsOnly)
	if dest_dialog != '':
		dossierDestination = dest_dialog+"/"
		config['options']['destination'] = dossierDestination
		with open('pysauv.ini', 'w') as configfile:
			config.write(configfile)
		valider.setDisabled(0)
		nom_dest.setText(dossierDestination)
	

# Objets Qt : l'application et la fenêtre

app = QApplication(sys.argv)
win = QWidget()

# Propriétés de la fenêtre

win.setWindowTitle("Sauvegarder")
win.resize(250,400)

# Création du canevas et de ses widgets

canevas = QGridLayout(win)

liste = QListWidget()

valider = QPushButton('Valider')
destination = QPushButton('Média')
nom_dest = QLabel(dossierDestination)

if dossierDestination == '':
	valider.setDisabled(1)

# Ajout des dossiers au widget QListView

liste.addItem("[Sauvegarde totale]")
for i in listeDossiers:
    liste.addItem(i)

# Connection des signaux de widgets aux slots

valider.released.connect(sauv)
destination.released.connect(askDestination)
liste.doubleClicked.connect(sauv)

# Affichage de la fenêtre et disposition des widgets sur le canevas

win.show()
canevas.addWidget(liste, 0, 0, 1, 2)
canevas.addWidget(nom_dest, 1, 0, 1, 2)
canevas.addWidget(valider, 2, 1)
canevas.addWidget(destination, 2, 0)

# Boucle d'exécution

app.exec_()
sys.exit()
