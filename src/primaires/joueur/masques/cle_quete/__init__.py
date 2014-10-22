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


"""Fichier contenant le masque <cle_quete>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class Quete(Masque):
    
    """Masque <cle_quete>.
    On attend une clé de quête existante.
    
    """
    
    nom = "cle_quete"
    nom_complet = "clé d'une quête"
    
    def init(self):
        """Initialisation des attributs"""
        self.joueur = None
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        lstrip(commande)
        cle_quete = liste_vers_chaine(commande).lower()
        if not cle_quete:
            raise ErreurValidation(
                "Précisez une clé de quête.")
        
        cle_quete = cle_quete.split(" ")[0].lower()
        commande[:] = commande[len(cle_quete):]
        masques.append(self)
        self.a_interpreter = cle_quete
        return True

    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        cle_quete = self.a_interpreter
        
        # On cherche dans les quêtes
        quetes = importeur.scripting.quetes.values()
        quete = None
        for t_quete in quetes:
            nom = t_quete.cle.lower()
            if nom == cle_quete:
                quete = t_quete
                break
        
        if not quete:
            raise ErreurValidation(
                "|err|La quête passée en paramètre n'existe pas.|ff|")
        
        self.quete = quete
        
        return True
