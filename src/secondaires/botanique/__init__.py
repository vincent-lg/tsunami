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


"""Fichier contenant le module secondaire botanique."""

from abstraits.module import *
from corps.fonctions import valider_cle
from primaires.format.fonctions import format_nb
from .plante import Plante

class Module(BaseModule):
    
    """Module secondaire définissant la botanique.
    
    Ce module contient la définition des plantes, conserve en mémoire
    l'association entre salle et végétal et définit les commandes propres
    à la botanique.
    
    Note à propos du stockage des plantes :
        Les plantes-mêmes sont des ObjetID, donc chacune est stockée dans
        un fichier différent. Cependant, le lien fait entre salle et plante
        (qui définit que dans telle salle on trouve telle(s) plantes(s))
        est fait dans un dictionnaire accessible depuis le module botanique.
        Ce dictionnaire a la forme :
            nid_salle: [(nid_plante1, etat1), (nid_plante2, etat2), ...]
        Le nid est la partie entière de l'ID. Ce dictionnaire, d'une
        structure assez complexe, est mis sous cette forme pour des raisons
        d'optimisation. En effet, il sera enregistré d'un bloc dans
        un fichier et si ce fichier est trop gros, les performances
        s'en ressentiraient.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "botanique", "secondaire")
        self.prototypes = {}
        self.plantes = {}
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "plantes", "plantes")
    
    def init(self):
        """Chargement des plantes et de leur position / état."""
        # On récupère les plantes
        plantes = self.importeur.supenr.charger_groupe(Plante)
        for plante in plantes:
            self.plantes[plante.cle] = plante
        
        nb_plantes = len(plantes)
        self.logger.info(format_nb(nb_plantes, "{nb} plante{s} récupérée{s}",
                fem=True))
        BaseModule.init(self)
    
    def creer_plante(self, cle):
        """Crée une plante et l'ajoute dans le dictionnaire.
        
        Retourne la plante créée.
        
        Lève une exception KeyError si la plante existe déjà.
        
        """
        valider_cle(cle)
        if cle in self.plantes:
            raise KeyError("la plante {} existe déjà".format(cle))
        
        plante = Plante(cle)
        self.ajouter_plante(plante)
        return plante
    
    def ajouter_plante(self, plante):
        """Ajoute la plante dans le dictionnaire."""
        self.plantes[plante.cle] = plante
    
    def supprimer_plante(self, cle):
        """Supprime la plante portant la clé passée en paramètre."""
        if cle not in self.plantes:
            raise KeyError("la plante de clé {} est inconnue".format(cle))
        
        plante = self.plantes[cle]
        del self.plantes[cle]
        plante.detruire()
