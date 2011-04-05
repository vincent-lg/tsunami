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


"""Package contenant la commande 'goto'."""

from primaires.interpreteur.commande.commande import Commande

class CmdGoto(Commande):
    
    """Commande 'goto'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "goto", "goto")
        self.schema = "<ident_salle|nom_joueur>"
        self.nom_categorie = "bouger"
        self.aide_courte = "permet de se déplacer dans l'univers"
        self.aide_longue = \
            "Cette commande vous permet de vous déplacer rapidement dans " \
            "l'univers. Vous devez lui passer en paramètre l'identifiant " \
            "d'une salle sous la forme |cmd|zone:mnémonic|ff|, " \
            "par exemple |ent|picte:1|ff|."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if dic_masques["ident_salle"] is None:
            salle = dic_masques["nom_joueur"].joueur.salle
        if dic_masques["nom_joueur"] is None:
            salle = dic_masques["ident_salle"].salle
        salle_courante = personnage.salle
        salle_courante.envoyer("{} disparaît avec un éclair de " \
                "|cyc|lumière bleue|ff|.".format(personnage.nom), (personnage,))
        personnage.salle = salle
        personnage << personnage.regarder()
        salle.envoyer("{} apparaît avec un éclair de |cyc|lumière " \
                "bleue|ff|.".format(personnage.nom), (personnage,))
