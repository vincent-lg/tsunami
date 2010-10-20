# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Ce fichier définit la classe Logger, détaillée plus bas."""

import os
import time

from primaires.log.message import Message

# Constantes prédéfinies
# Niveaux d'erreur
DBG = DEBUG = 0
INFO = 1
WARN = WARNING = 2
FATAL = ERROR = EXCEPTION = 3

# Dictionnaire des niveaux
NIVEAUX = {
    INFO: "info",
    WARNING: "warning",
    DEBUG: "debug",
    FATAL: "fatal",
}

# Correspondances inverses
REV_NIVEAUX = {}
for cle, val in NIVEAUX.items():
    REV_NIVEAUX[val] = cle

# Format (voir méthode formater de la classe Logger)
FORMAT = "%date% %heurems% [%niveau%] : %message%"

class Logger:
    """Cette classe représente des loggers.
    Ce sont des objets permettant d'enregistrer différentes informations.
    Une instance d'un logger est créée à chaque fois qu'on souhaite obtenir
    une information indépendante des autres. Par exemple, chaque module
    primaire ou secondaire doit posséder son propre logger. Le corps
    également.
    
    Chaque logger possède :
    -   un fichier de log qui peut être à None
    -   un flag concernant l'affichage des messages dans la console
    -   un format d'enregistrement des messages
    -   un niveau minimum pour afficher le message. A noter que tous les
        messages sont enregistrés dans le fichier. Mais on peut par exemple
        demander que seuls les informations critiques soient affichées
        dans la console

    NOTE IMPORTANTE: le logger doit s'abstenir de logger des messages
    pendant un certain lapse de temps. Les messages à logger sont alors
    stockées dans une fil d'attente et enregistrées après coup.
    C'est le module 'log' lui-même qui change l'information d'état
    et autorise le logger à écrire en temps réel ses messages.
    En effet, tant que le module log se configure, aucun message ne devra
    être enregistré.
    
    NOTE IMPORTANTE : sauf depuis l'intérieur de la classe, on ne doit pas
    appeler les méthodes log et log_formate. Elles ne sont ici que pour
    garantir une certaine généricité de l'enregistrement des fichiers de log.
    Pour enregistrer des messages, utiliser les méthodes debug, info, warning
    et fatal, respectivement pour chaque niveau d'erreur.

    """
    def __init__(self, rep_base, sous_rep, nom_fichier, nom_logger, \
            console=True, format=FORMAT, niveau_min=INFO):
        """Constructeur du logger. Seuls les quatre premiers paramètres
        sont obligatoires :
        -   le répertoire de base (probablement constant d'un logger à l'autre)
        -   le sous-répertoire
        -   le nom du fichier de log
            Ces trois informations peuvent contenir des chaînes vides
            si l'on ne souhaite pas enregistrer dans un fichier (déconseillé).
        -   le nom du logger
        -   console (True pour afficher dans la console, False sinon)
        -   le format du message de log enregistré (voir méthode formater)
        -   le niveau minimum pour afficher un message
        
        """
        self.nom = nom_logger
        self.en_fil = True # par défaut, on stock en fil d'attente
        self.fil_attente = [] # liste des messages en attente d'être écrits
        self.rep_base = rep_base
        self.sous_rep = sous_rep
        self.nom_fichier = nom_fichier
        self.fichier = None # on essayera de l'ouvrir au moment du logging
        self.console = console
        self.format = format
        self.niveau_min = niveau_min

    def _get_rep_complet(self):
        """Cette méthode retourne le répertoire complet rep_base et sous_rep.
        Si sous_rep est vide on s'assure que le chemin reste cohérent.
        
        """
        rep_base = self.rep_base
        sous_rep = self.sous_rep
        if sous_rep == "":
            rep_complet = rep_base
        else:
            rep_complet = rep_base + os.sep + sous_rep

        return rep_complet

    rep_complet = property(_get_rep_complet)

    def filtrer_niveau(self, niveau_str):
        """Permet de changer le niveau minimum de filtrage des messages.
        ATTENTION : le niveau est donné sous la forme d'une chaîne.
        En efffet, les autres modules n'ont pas accès aux différents niveaux
        de message. On se base sur le dictionnaire REV_NIVEAUX pour trouver
        l'entier correspondant.
        
        """
        self.niveau_min = REV_NIVEAUX[niveau_str]

    def verif_rep(self):
        """Cette méthode vérifie si le répertoire de log existe.
        Si ce n'est pas le cas, on le créée.

        """
        rep = self.rep_complet
        if not os.path.exists(rep):
            os.makedirs(rep)

    def ouvrir_fichier(self):
        """Méthode chargée d'ouvrir le fichier configuré."""
        rep = self.rep_complet
        nom_fichier = rep + os.sep + self.nom_fichier
        try:
            # On tente d'ouvrir le fichier
            self.fichier = open(nom_fichier, "a")
        except IOError:
            print("Impossible d'ouvrir le fichier de log {0}".format( \
                    nom_fichier))
            self.fichier = None

    def fermer_fichier(self):
        """Méthode chargée de fermer le fichier de log."""
        if self.fichier is not None:
            self.fichier.close()
            self.fichier = None

    def formater(self, niveau, message):
        """Méthode retournant la chaîne formattée.
        
        Si des formats spécifiques sont ajoutés, les définir ici.
        On définit un format spécifique comme une partie de chaîne entourée
        de deux signes %.
        Par exemple, %date% sera remplacé par la date actuel dans le message.

        """
        sdate = time.struct_time(time.localtime())
        ms = "{0:f}".format(time.time()).split(".")[1][:3]
        date = "{0}-{1:02}-{2:02}".format(sdate.tm_year, sdate.tm_mon, \
                sdate.tm_mday)
        heure = "{0:02}:{1:02}:{2:02}".format(sdate.tm_hour, \
                sdate.tm_min, sdate.tm_sec)
        heurems = "{0:02}:{1:02}:{2:02},{3}".format(sdate.tm_hour, \
                sdate.tm_min, sdate.tm_sec, ms)
        chaine = self.format
        chaine = chaine.replace("%date%", date)
        chaine = chaine.replace("%heure%", heure)
        chaine = chaine.replace("%heurems%", heurems)
        chaine = chaine.replace("%niveau%", niveau)
        chaine = chaine.replace("%message%", message)
        return chaine

    def doit_afficher(self, niveau, module):
        """Retourne True si le logger doit afficher le message de ce
        niveau, False sinon.
        
        """
        doit = False
        if module == self.nom:
            if self.console is True and self.niveau_min <= niveau:
                doit = True
        return doit

    def log_formate(self, niveau, message, formate, module):
        """Cette méthode permet de logger un message déjà formaté. les
        méthodes log et enregistrer_fil_attente font directement appel
        à elle.
        
        """
        self.ouvrir_fichier()
        if self.fichier is not None:
            # On essaye d'écrire dans le fichier
            try:
                self.fichier.write(formate + "\n")
            except IOError:
                pass
        self.fermer_fichier()

    def log(self, niveau, message, module):
        """Méthode permettant de logger un message.
        Les méthodes info, debug, warning et fatal redirigent dessus.
        
        """
        s_niveau = NIVEAUX[niveau]
        f_message = self.formater(s_niveau, message)
        if self.en_fil:
            self.fil_attente.append(Message(s_niveau, message, f_message))
            if self.doit_afficher(niveau, module):
                print(message)
        else:
            if self.doit_afficher(niveau, module):
                print(message)

            self.log_formate(niveau, message, f_message, self.nom)

    def enregistrer_fil_attente(self):
        """Cette méthode ne doit être appelée qu'une fois.
        Elle permet d'enregistrer la fil d'attente du logger.
        Cette fil d'attente s'est remplie pendant que le module 'log' se
        configurait. Dès son initialisation, le module demande à cette méthode
        que la fil d'attente de chaque logger créé soit enregistrée.
        
        """
        for message in self.fil_attente:
            self.log_formate(message.niveau, message.message, \
                    message.message_formate,self.nom)

    def debug(self, message):
        """Méthode permettant de logger un niveau de message DEBUG"""
        self.log(DEBUG, message, self.nom)

    def info(self, message):
        """Méthode permettant de logger un niveau de message INFO"""
        self.log(INFO, message, self.nom)

    def warning(self, message):
        """Méthode permettant de logger un niveau de message WARNING"""
        self.log(WARNING, message, self.nom)

    def fatal(self, message):
        """Méthode permettant de logger un niveau de message FATAL"""
        self.log(FATAL, message, self.nom)

