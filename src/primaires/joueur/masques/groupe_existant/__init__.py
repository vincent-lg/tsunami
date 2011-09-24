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


"""Fichier contenant le masque <groupe_existant>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation


class GroupeExistant(Masque):
    
    """Masque <groupe_existant>.
    On attend un nom de groupe en paramètre.
    
    """
    
    nom = "groupe_existant"
    nom_complet = "nom d'un groupe existant"
    
    def init(self):
        """Initialisation des attributs"""
        self.nom_groupe = ""
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        nom_groupe = liste_vers_chaine(commande)
        if not nom_groupe:
            raise ErreurValidation(
                "Précisez un nom de groupe existant.")
        
        nom_groupe = nom_groupe.split(" ")[0]
        self.a_interpreter = nom_groupe
        commande[:] = commande[len(nom_groupe):]
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom_groupe = self.a_interpreter
        noms_groupes = [groupe.nom for groupe in \
            type(self).importeur.interpreteur.groupes._groupes.values()]
        if nom_groupe not in noms_groupes:
            raise ErreurValidation(
                "|err|Ce groupe est inconnu.|ff|")

        self.nom_groupe = nom_groupe.lower()
        return True
