# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Fichier contenant le module secondaire jeux."""

from abstraits.module import *
from . import commandes
from . import types

class Module(BaseModule):
    
    """Module gérant les jeux dans le jeu
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "jeux", "secondaire")
        
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "jeux", "jeux")
        self.jeux = {}
        self.plateaux = {}
        self.parties = []
    
    def init(self):
        """Initialisation du module."""
        # On charge automatiquement les jeux définis dans jeux
        self.charger_jeux()
        self.charger_plateaux()
        BaseModule.init(self)
    
    def charger_jeux(self):
        """Chargement des jeux.
        
        Notez qu'un plateau peut être utilisé pour jouer à plusieurs jeux.
        
        """
        # On peut préciser en dur des exceptions qui ne seront pas chargées
        # En outre, tous les répertoires commençant par un _ ne sont pas chargés
        exceptions = []
        chemin = self.chemin + os.sep + "jeux"
        chemin_py = "secondaires.jeux.jeux"
        for nom_fichier in os.listdir(chemin):
            if not nom_fichier.startswith("_") and nom_fichier not in \
                    exceptions:
                nom_module = nom_fichier
                chemin_py_mod = chemin_py + ".{}".format(nom_module)
                jeu = __import__(chemin_py_mod)
                jeu = getattr(getattr(getattr(getattr(jeu, "jeux"),
                        "jeux"), nom_module), "Jeu")
                self.jeux[jeu.nom] = jeu
                print("On charge le jeu", nom_module)
    
    def charger_plateaux(self):
        """Chargement des plateaux."""
        # On peut préciser en dur des exceptions qui ne seront pas chargées
        # En outre, tous les répertoires commençant par un _ ne sont pas chargés
        exceptions = []
        chemin = self.chemin + os.sep + "plateaux"
        chemin_py = "secondaires.jeux.plateaux"
        for nom_fichier in os.listdir(chemin):
            if not nom_fichier.startswith("_") and nom_fichier not in \
                    exceptions:
                nom_module = nom_fichier
                chemin_py_mod = chemin_py + ".{}".format(nom_module)
                plateau = __import__(chemin_py_mod)
                plateau = getattr(getattr(getattr(getattr(plateau, "jeux"),
                        "plateaux"), nom_module), "Plateau")
                self.plateaux[plateau.nom] = plateau
                print("On charge le plateau", nom_module)
    
    def get_jeu(self, nom):
        """Retourne le jeu portant le nom nom.
        
        Si aucun jeu n'est trouvé, retourne None.
        
        """
        for jeu in self.jeux.values():
            if jeu.nom == nom:
                return jeu
        
        return None
    
    def ajouter_commandes(self):
        self.commandes = [
            commandes.jouer.CmdJouer()
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
