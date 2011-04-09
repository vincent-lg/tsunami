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


"""Package contenant la commande 'repondre'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdRepondre(Commande):
    
    """Commande 'repondre'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "repondre", "reply")
        self.nom_categorie = "parler"
        self.schema = "(<message>)"
        self.aide_courte = "répond à un joueur"
        self.aide_longue = \
            "Cette commande permet de répondre au dernier joueur qui vous a  " \
            "parlé avec à la commande %tell%. Sans argument, %reply% " \
            "retourne une liste numérotée des personnes qui vous ont parlé " \
            "au cours de cette session. Vous pouvez répondre à l'une d'entre " \
            "elles en particulier avec %reply% |ent|<numéro de la liste> " \
            "<message>|ff|. Vous pouvez aussi bloquer la réponse automatique " \
            "sur un personnage de la liste en entrant %reply% |ent|<numéro " \
            "du personnage>|ff|."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        corresp = type(self).importeur.communication.correspondants
        if dic_masques["message"] is None:
            liste_aff = []
            i = 1
            for id_cible, id_perso in corresp.items():
                if personnage.id.id == id_cible:
                    liste_aff.append(str(i) + ". " + type(self).importeur. \
                            parid["joueurs"][id_perso].nom)
                    i += 1
            if not liste_aff:
                personnage << "|err|Personne ne vous a parlé pour le " \
                        "moment.|ff|"
            else:
                personnage << "\n ".join(liste_aff)
        else:
            message = dic_masques["message"].message
            clr = type(self).importeur.anaconf. \
                    get_config("config_com").couleur_tell
            try:
                id_cible = corresp[personnage.id.id]
            except KeyError:
                personnage << "|err|Personne ne vous a parlé pour le " \
                        "moment.|ff|"
            else:
                cible = type(self).importeur.parid["joueurs"][id_cible]
                if cible not in type(self).importeur.connex.joueurs_connectes:
                    personnage << "|err|Le joueur passé en paramètre n'a pu " \
                            "être trouvé.|ff|"
                else:
                    type(self).importeur.communication. \
                            correspondants[cible.id.id] = personnage.id.id
                    personnage << clr + "Vous répondez à {} : {}|ff|" \
                            .format(cible.nom, message)
                    cible << clr + "{} vous répond : {}|ff|" \
                            .format(personnage.nom, message)