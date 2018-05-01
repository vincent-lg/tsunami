# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 CORTIER Benoît
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


"""Package contenant la commande 'decrire'"""

from primaires.interpreteur.masque.parametre import Parametre

class PrmAccepter(Parametre):

    """Commande 'valider voir'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "accepter", "accept")
        self.schema = "<nom_joueur>"
        self.aide_courte = "Valider la description d'un joueur."
        self.aide_longue = \
            "Valide la description d'un joueur."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        joueur = dic_masques["nom_joueur"].joueur
        if not joueur.description_modifiee:
            personnage << "|err|Le joueur n'a pas de description à " \
                    "valider.|ff|"
        else:
            joueur.description_modifiee = False
            joueur.description.paragraphes[:] = \
                    joueur.description_a_valider.paragraphes[:]
            personnage << "La description du joueur a bien été validée."
            joueur << "Votre nouvelle description vient d'être validée."
