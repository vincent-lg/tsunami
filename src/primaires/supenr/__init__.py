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


"""Ce fichier contient le module primaire supenr."""

import copy
import os
import pickle
import sys
import time

from abstraits.module import *
from abstraits.obase import *

# Dossier d'enregistrement des fichiers-données
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
REP_ENRS = os.path.expanduser("~") + os.sep + "kassie"

class Module(BaseModule):
    
    """Classe du module 'supenr'.
    
    Ce module gère l'enregistrement des données et leur récupération.
    Les objets enregistrés doivent dériver indirectement de
    abstraits.obase.BaseObj (voir abstraits/obase/__init__.py pour plus
    d'informations).
    
    Habituellement, il n'est pas nécessaire de manipuler directement
    ce module.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "supenr", "primaire")
        self.logger = type(self.importeur).man_logs.creer_logger("supenr", \
                "supenr")
        self.enregistre_actuellement = False
        self.pret = False
    
    def config(self):
        """Configuration du module.
        
        On se base sur parser_cmd pour savoir si un dossier d'enregistrement
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
        
        # On construit le répertoire s'il n'existe pas
        if not os.path.exists(REP_ENRS):
            os.makedirs(REP_ENRS)
        
        self.pret = True
        BaseModule.config(self)
    
    def init(self):
        """Chargement de tous les objets."""
        self.charger()
        
        # Création de l'action différée pour enregistrer périodiquement
        importeur.diffact.ajouter_action("enregistrement", 60 * 15,
                self.enregistrer_periodiquement)
        
        BaseModule.init(self)
    
    def detruire(self):
        """Destruction du module"""
        self.enregistrer()
        BaseModule.detruire(self)
    
    def enregistrer(self):
        """Méthode appelée pour enregistrer TOUS les objets."""
        global REP_ENRS
        if not self.pret:
            raise RuntimeError("le supenr n'est pas prêt à enregistrer")
        
        if self.enregistre_actuellement:
            return
        
        a_enregistrer = [o for o in objets.values() if o.e_existe]
        self.logger.info("{} objets, dans {}o sont prêts à être " \
                "enregistrés.".format(str(len(a_enregistrer)),
                str(len(pickle.dumps(a_enregistrer)))))
        self.enregistre_actuellement = True
        chemin_dest = REP_ENRS + os.sep + "enregistrements.bin"
        
        # On essaye d'ouvrir le fichier
        try:
            fichier_enr = open(chemin_dest, 'wb')
        except IOError as io_err:
            self.logger.warning("Le fichier {} destiné à enregistrer " \
                    "les objets de Kassie n'a pas pu être ouvert : {}".format(
                    chemin_dest, io_err))
        else:
            pickler = pickle.Pickler(fichier_enr)
            pickler.dump(a_enregistrer)
        finally:
            if "fichier_enr" in locals():
                fichier_enr.close()
            self.enregistre_actuellement = False
            for classe, liste in objets_par_type.items():
                liste = [o for o in liste if o.e_existe]
    
    def enregistrer_periodiquement(self):
        """Cette méthode est appelée périodiquement pour enregistrer les objets.
        
        """
        importeur.diffact.ajouter_action("enregistrement", 60 * 15,
                self.enregistrer_periodiquement)
        if self.enregistre_actuellement:
            return
        
        t1 = time.time()
        self.enregistrer()
        t2 = time.time()
        print("Enregistrement fait en", t2 - t1)
        
    def charger(self):
        """Charge le fichier indiqué et retourne l'objet dépicklé"""
        global REP_ENRS
        chemin_dest = REP_ENRS + os.sep + "enregistrements.bin"
        try:
            fichier_enr = open(chemin_dest, 'rb')
        except IOError as io_err:
            self.logger.warning("Le fichier {} n'a pas pu être ouvert " \
                    ": {}".format(chemin_dest, io_err))
        else:
            unpickler = pickle.Unpickler(fichier_enr)
            try:
                rec = unpickler.load()
            except (EOFError, pickle.UnpicklingError):
                self.logger.warning("Le fichier {} n'a pas pu être " \
                        "chargé ".format(chemin_dest))
        finally:
            if "fichier_enr" in locals():
                fichier_enr.close()
            self.logger.info("{} objets récupérés".format(len(objets)))
        
    def charger_groupe(self, groupe):
        """Cette fonction retourne les objets d'un groupe.
        
        On se base sur objets_par_type.
        
        """
        if not self.pret:
            raise RuntimeError("le supenr n'est pas prêt à charger un groupe")
        
        return objets_par_type.get(groupe, [])
    
    def charger_unique(self, groupe):
        """Cette fonction retourne l'objet unique correspondant.
        
        Si plusieurs objets uniques semblent exister du même type, retourne
        le premier à avoir été chargé.
        
        """
        if not self.pret:
            raise RuntimeError("le supenr n'est pas prêt à charger un groupe")
        
        return objets_par_type.get(groupe, [None])[0]
