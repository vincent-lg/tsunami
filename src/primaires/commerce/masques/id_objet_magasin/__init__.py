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


"""Fichier contenant le masque <id_objet_magasin>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class IdObjetMagasin(Masque):
    
    """Masque <id_objet_magasin>.
    On attend l'id valide d'un objet dans le magasin de la salle dans laquelle
    se trouve le joueur.
    
    """
    
    nom = "id_objet_magasin"
    nom_complet = "ID en magasin"
    
    def init(self):
        """Initialisation des attributs du masque"""
        self.objet = None
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        print("répartition")
        id_objet = liste_vers_chaine(commande)
        if not id_objet:
            raise ErreurValidation( \
                "Vous devez préciser l'ID d'un objet.", False)
        
        id_objet = id_objet.split(" ")[0]
        try:
            assert id_objet.startswith("#")
            id_objet = int(id_objet[1:])
            print(id_objet)
        except (AssertionError, ValueError):
            raise ErreurValidation( \
                "L'ID doit être sous la forme #<nombre>.", False)
        else:
            self.a_interpreter = id_objet
            commande[:] = commande[(len(str(id_objet)) + 1):]
            masques.append(self)
            return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        print("validation")
        Masque.valider(self, personnage, dic_masques)
        id_objet = self.a_interpreter
        magasin = personnage.salle.magasin
        objet = magasin.get_item_par_id(id_objet)
        if objet is None:
            raise ErreurValidation( \
                "|err|L'ID spécifié ne correspond à aucun objet en " \
                "magasin.|ff|")
        else:
            self.objet = objet
            return True
