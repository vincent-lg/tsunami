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
from primaires.communication.correspondants import Correspondants

class CmdRepondre(Commande):
    
    """Commande 'repondre'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "repondre", "reply")
        self.nom_categorie = "parler"
        self.schema = "(<id_corresp>) (<message>)"
        self.aide_courte = "répond à un joueur"
        self.aide_longue = \
            "Cette commande permet de répondre au dernier joueur qui vous a " \
            "parlé avec à la commande %parler%. Sans argument, %repondre% " \
            "retourne une liste numérotée des personnes qui vous ont parlé " \
            "au cours de cette session. Vous pouvez répondre à l'une d'entre " \
            "elles en particulier avec %repondre% |ent|<numéro de la liste> " \
            "<message>|ff|. Vous pouvez aussi bloquer la réponse automatique " \
            "sur un personnage de la liste en entrant %repondre% " \
            "ent|<numéro du personnage>|ff|."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        corresp = type(self).importeur.communication.correspondants
        p_corresp = []
        for couple in corresp:
            if personnage == couple.emetteur:
                p_corresp.append(couple)
                
        # Si on n'a pas envoyé de message
        if dic_masques["message"] is None:
            if dic_masques["id_corresp"] is None:
                # On liste les correspondants
                res = ""
                for couple in p_corresp:
                    res += "\n " + str(couple.id) + ". " + couple.cible.nom
                if not res:
                    personnage << "|err|Personne ne vous a parlé pour le " \
                            "moment.|ff|"
                else:
                    personnage << res
            else:
                # On place le focus sur le correspondant indiqué
                id = dic_masques["id_corresp"].id_corresp
                cible = dic_masques["id_corresp"].correspondant
                for couple in type(self).importeur.communication.correspondants:
                    if couple.id == id and couple.emetteur == personnage and couple.cible == cible:
                        if not couple.focus:
                            couple.ch_focus()
                            personnage << "|att|La réponse automatique a bien été " \
                                    "bloquée sur {}.|ff|".format(cible.nom)
                        else:
                            personnage << "|err|Le focus est déjà sur {}.|ff|".format(cible.nom)
        # Sinon
        else:
            message = dic_masques["message"].message
            clr = type(self).importeur.anaconf. \
                    get_config("config_com").couleur_tell
            cible = None
            # On récupère la cible du reply
            if dic_masques["id_corresp"] is not None:
                cible = dic_masques["id_corresp"].correspondant
            # Si le masque id n'a rien donné
            if cible is None:
                for couple in p_corresp:
                    cible = couple.cible
                    if couple.focus:
                        break
            # On envoie le message
            if cible is None:
                personnage << "|err|Personne ne vous a parlé pour le " \
                        "moment.|ff|"
            else:
                if cible not in type(self).importeur.connex.joueurs_connectes:
                    personnage << "|err|Le joueur {} passé en paramètre n'a pu " \
                            "être trouvé.|ff|".format(cible.nom)
                else:
                    couple = Correspondants(cible, personnage)
                    type(self).importeur.communication.correspondants \
                            .append(couple)
                    personnage << clr + "Vous répondez à {} : {}|ff|" \
                            .format(cible.nom, message)
                    cible << clr + "{} vous répond : {}|ff|" \
                            .format(personnage.nom, message)
