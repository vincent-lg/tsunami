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


"""Package contenant la commande 'supsortie'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.exceptions.erreur_interpretation import \
    ErreurInterpretation

class CmdSupsortie(Commande):
    
    """Commande 'supsortie'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "supsortie", "delexit")
        self.groupe = "administrateur"
        self.schema = "<direction>"
        self.nom_categorie = "batisseur"
        self.aide_courte = "supprime une sortie de la salle courante"
        self.aide_longue = \
            "Cette commande supprime une sortie de la salle courante. " \
            "Vous devez lui préciser le nom d'une sortie constante. La " \
            "sortie réciproque dans la salle de destination sera également " \
            "supprimée si elle existe."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        direction = dic_masques["direction"].direction
        salle = personnage.salle
        
        if not salle.sorties.sortie_existe(direction):
            raise ErreurInterpretation(
                "|err|Cette direction n'a pas été définie dans cette salle.|ff|")

        d_salle = salle.sorties[direction].salle_dest

        # ne supprimer la sortie réciproque que si elle est vraiment réciproque
        corresp = salle.sorties[direction].correspondante
        reciproque_definie = corresp is not None and corresp != "" and d_salle is not None
        if reciproque_definie:
            dir_opposee = salle.sorties.get_nom_oppose(direction)
            d_salle.sorties.supprimer_sortie(dir_opposee)

        salle.sorties.supprimer_sortie(direction)
        message = "La sortie {} a bien été supprimée de la salle " \
            "courante.".format(direction)
        if reciproque_definie:
            message += "\nLa réciproque a également été supprimée (sortie " \
                "{} dans {}).".format(dir_opposee, d_salle)

        personnage << "|att|" + message + "|ff|"
