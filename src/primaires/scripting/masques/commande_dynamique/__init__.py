# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant le masque <commande_dynamique>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.format.fonctions import supprimer_accents

class CommandeDynamique(Masque):
    
    """Masque <commande_dynamique>.
    
    On attend une commande dynamique en paramètre sous sa forme
    francais/anglais.
    
    """
    
    nom = "commande_dynamique"
    nom_complet = "commande dynamique"
    
    def init(self):
        """Initialisation des attributs"""
        self.commande = ""
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        lstrip(commande)
        nom = liste_vers_chaine(commande)
        
        if not nom:
            raise ErreurValidation( \
                "Précisez une commande dynamique.")
        
        if nom.count("/") != 1 or " " in nom:
            raise ErreurValidation( \
                "Précisez le nom français, un signe |cmd|/|ff| puis " \
                "le nom anglais.")
        
        nom = nom.split(" ")[0].lower()
        self.a_interpreter = nom
        commande[:] = commande[len(nom):]
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom = self.a_interpreter
        nom_sa = supprimer_accents(nom)
        for cmd in importeur.scripting.commandes_dynamiques.values():
            t_nom = str(cmd)
            if supprimer_accents(t_nom) == nom_sa:
                self.commande = cmd
                return True
        
        raise ErreurValidation(
            "|err|La commande dynamique '{}' n'existe pas.|ff|".format(nom))
