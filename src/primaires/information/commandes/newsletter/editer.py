# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package contenant le paramètre 'editer' de la commande 'newsletter'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEditer(Parametre):
    
    """Commande 'newsletter edit'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "editer", "edit")
        self.schema = "<nombre>"
        self.aide_courte = "ouvre l'éditeur de newsletter"
        self.aide_longue = \
            "Cette commande ouvre l'éditeur de news letter pour vous " \
            "permettre d'éditer une news letter non envoyée (en statut " \
            "\"brouillon\"). Vous pourrez ainsi modifier son sujet et " \
            "sa description, ainsi que l'envoyer si elle est prête."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        id = dic_masques["nombre"].nombre
        try:
            newsletter = importeur.information.newsletters[id - 1]
        except IndexError:
            personnage << "|err|Cette newsletter n'existe pas.|ff|"
        else:
            if newsletter.envoyee:
                personnage << "|err|Cette news letter a déjà été envoyée.|ff|"
                return
            
            if newsletter.editee:
                personnage << "|err|Cette news letter est en cours " \
                        "d'édition par un autre administrateur.|ff|"
                return
            
            editeur = importeur.interpreteur.construire_editeur(
                    "nledit", personnage, newsletter)
            personnage.contextes.ajouter(editeur)
            editeur.actualiser()
