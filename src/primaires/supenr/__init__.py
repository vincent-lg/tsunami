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


"""Ce fichier contient la classe Supenr, définissant le module primaire
du même nom.

"""

import os
import pickle

from abstraits.module import *
from abstraits.id import ObjetID, est_objet_id

# Dossier d'enregistrement des fichiers-données
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
REP_ENRS = os.path.expanduser("~") + os.sep + "kassie" + os.sep + "enregistrements"

class Supenr(Module):
    """Classe du module 'supenr'.
    
    Ce module gère l'enregistrement des données et leur récupération.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        Module.__init__(self, importeur, "supenr", "primaire")
        self.fil_attente = set() # fil d'attente des objets à enregistrer
        self.pic_memo = {} # mémo des picklers
        self.unpic_memo = {} # mémo des dépicklers
        self.logger = type(self.importeur).man_logs.creer_logger("supenr", \
                "supenr")
    
    def config(self):
        """Méthode de configuration. On se base sur
        parser_cmd pour savoir si un dossier d'enregistrement
        des fichiers-données a été défini.
        
        """
        global REP_ENRS
        parser_cmd = type(self.importeur).parser_cmd
        config_globale = type(self.importeur).anaconf.get_config("globale")
        if config_globale.chemin_enregistrement:
            REP_ENRS = config_globale.chemin_enregistrement
        
        if "chemin-enregistrement" in parser_cmd.keys():
            REP_ENRS = parser_cmd["chemin-enregistrement"]
        
        # On construit le répertoire si il n'existe pas
        if not os.path.exists(REP_ENRS):
            os.makedirs(REP_ENRS)
        
        ObjetID._supenr = self
        for chemin in ObjetID.groupes:
            chemin = REP_ENRS + os.sep + chemin
            if not os.path.exists(chemin):
                os.makedirs(chemin)

        Module.config(self)
    
    def construire_rep(self, sous_rep):
        """Construit le chemin REP_ENRS / sous_rep si il n'existe pas"""
        global REP_ENRS
        chemin = REP_ENRS + os.sep + sous_rep
        if not os.path.exists(chemin):
            os.makedirs(chemin)
    
    def enregistrer(self, objet):
        """Méthode appelée pour enregistrer un objet dans un fichier. Cette
        méthode est appelée par la méthode 'boucle' de ce module, ou par
        appel à la méthode 'enregistrer' de l'objet lui-même.
        
        """
        global REP_ENRS
        if not est_objet_id(objet):
            raise runtimeError("l'objet {0} n'est aps un objet ID. On ne " \
                    "peut l'enregistrer".format(objet))
        chemin_dest = REP_ENRS + os.sep + type(objet).sous_rep
        nom_fichier = str(objet.id.id) + ".sav"
        chemin_dest += os.sep + nom_fichier
        # On essaye d'ouvrir le fichier
        try:
            fichier_enr = open(chemin_dest, 'wb')
        except IOError as io_err:
            self.logger.warning("Le fichier {0} destiné à enregistrer {1} " \
                    "n'a pas pu être ouvert : {2}".format(chemin_dest, \
                    objet, io_err))
        else:
            pickler = pickle.Pickler(fichier_enr)
            pickler.memo = self.pic_memo
            pickler.dump(objet)
        finally:
            if "fichier_dest" in locals():
                fichier_dest.close()
    
    def boucle(self):
        """Méthode appelée à chaque tour de boucle synchro"""
        # On enregistre les objets en attente
        self.enregistrer_fil_attente()
    
    def enregistrer_fil_attente(self):
        """On enregistre la fil d'attente. On appelle la méthode 'enregistrer'
        de chaque objet contenu dans le set 'self.fil_attente'.
        
        """
        for objet in self.fil_attente:
            objet.enregistrer()
        self.fil_attente.clear()
    
    def charger(self, sous_rep, nom_fichier):
        """Charge le fichier indiqué et retourne l'objet dépicklé"""
        global REP_ENRS
        chemin_dest = REP_ENRS + os.sep + sous_rep + os.sep + nom_fichier
        objet = None
        try:
            fichier_enr = open(chemin_dest, 'wb')
        except IOError as io_err:
            self.logger.warning("Le fichier {0} n'a pas pu être ovuert " \
                    ": {1}".format(chemin_dest, io_err))
        else:
            unpickler = pickle.Unpickler(fichier_enr)
            unpickler.memo = self.unpic_memo
            objet = unpickler.load()
        finally:
            fichier_dest.close()
        return objet
