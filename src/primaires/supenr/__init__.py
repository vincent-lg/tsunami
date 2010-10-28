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
    Les objets enregistrés doivent dériver indirectement de
    'abstraits.id.ObjetID' (voir 'abstraits/id/__init__.py' pour plus
    d'informations).
    
    Habituellement, il n'est pas nécessaire de manipuler directement
    ce module. Il suffit de créer un nouveau groupe d'identification
    et de créer ses objets dérivés de ce groupe, sans se préoccuper
    de leur enregistrement (celui-ci sera automatique).
    Lors de la configuration de 'supenr', il récupérera les différents
    fichiers-données enregistrés lors de la dernière session et les stockera
    dans l'attribut de classe 'objets' du groupe, sous la forme d'une liste
    d'objets.
    
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
        Cette donnée peut également se trouver dans les données globales de
        configuration.
        
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
        
        Module.config(self)
    
    def init(self):
        """Méthode d'initialisation du module.
        On récupère les différents objets des groupes d'identification.
        Note importante : il est important dans ce contexte que le module
        'supenr' ait la priorité en initialisation par rapport aux autres
        modules l'utilisant.
        
        """
        global REP_ENRS
        for groupe in ObjetID.groupes.values():
            chemin = groupe.sous_rep
            chemin = REP_ENRS + os.sep + chemin
            if not os.path.exists(chemin):
                os.makedirs(chemin)
            objets = self.charger_groupe(groupe)
            groupe.objets = objets
            self.logger.info("{0} objets chargés dans le groupe {1}".format( \
                    len(objets), groupe.groupe))
        
        Module.init(self)
    
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
            raise TuntimeError("l'objet {0} n'est pas un objet ID. On ne " \
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
            if "fichier_enr" in locals():
                fichier_enr.close()
    
    def detruire_fichier(self, objet):
        """Méthode appelée pour détruire le fichier contenant l'objet
        passé en paramètre.
        
        """
        global REP_ENRS
        if not est_objet_id(objet):
            raise RuntimeError("l'objet {0} n'est pas un objet ID. On ne " \
                    "peut le supprimer".format(objet))
        chemin_dest = REP_ENRS + os.sep + type(objet).sous_rep
        nom_fichier = str(objet.id.id) + ".sav"
        chemin_dest += os.sep + nom_fichier
        try:
            os.remove(chemin_dest)
        except OSError as os_err:
            self.logger.warning("Le fichier {0} censé enregistrer {1} " \
                    "n'a pas pu être supprimé : {2}".format(chemin_dest, \
                    objet, os_err))
    
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
            fichier_enr = open(chemin_dest, 'rb')
        except IOError as io_err:
            self.logger.warning("Le fichier {0} n'a pas pu être ouvert " \
                    ": {1}".format(chemin_dest, io_err))
        else:
            unpickler = pickle.Unpickler(fichier_enr)
            unpickler.memo = self.unpic_memo
            objet = unpickler.load()
        finally:
            if "fichier_enr" in locals():
                fichier_enr.close()
        
        return objet
    
    def charger_groupe(self, groupe):
        """Cette fonction permet de charger tout un groupe d'un coup, d'un
        seul.
        Elle prend en paramètre la sous-classe d'ObjetID définissant le
        groupe.
        Elle retourne la liste des objets chargés.
        
        """
        global REP_ENRS
        chemin_dest = REP_ENRS + os.sep + groupe.sous_rep
        objets = [] # liste des objets récupérés
        if not os.path.exists(chemin_dest):
            self.logger.warning("Le dossier {0} devant contenir le groupe " \
                    "{1} n'existe pas".format(chemin_dest, groupe.groupe))
        else:
            liste_fichier = sorted(os.listdir(chemin_dest))
            for nom_fichier in liste_fichier:
                objet = self.charger(groupe.sous_rep, nom_fichier)
                if objet is not None:
                    objets.append(objet)
        
        return objets
