# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Package contenant la commande 'quete'"""

from primaires.interpreteur.commande.commande import Commande

class CmdQuete(Commande):
    
    """Commande 'quete'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "quete", "quest")
        self.groupe = "joueur"
        self.schema = ""
        self.aide_courte = "récapitule vos quêtes"
        self.aide_longue = \
            "Cette commande récapitule l'état actuel de vos quêtes, en " \
            "cours ou terminées."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        faites = [q for q in importeur.scripting.quetes.values() \
                if personnage.quetes[q.cle].niveaux != [(0, )]]
        ret = "|tit|Vos quêtes en cours :|ff|"
        # on parcourt les quêtes en cours / terminees
        terminees = []
        for quete in faites:
            etapes_faites = [e for e in quete.etapes.values() \
                    if e.niveau in personnage.quetes[quete.cle].niveaux]
            etapes_a_faire = [e for e in quete.etapes.values() \
                    if e not in etapes_faites]
            # si la quête est terminee on passe le tour
            if all(e in etapes_faites for e in quete.etapes.values()):
                terminees.append(quete)
                continue
            ret += "\n|cy|" + quete.titre[0].upper() + quete.titre[1:] + "|ff|"
            if quete.ordonnee: # si c'est une quête ordonnée
                etape = sorted(etapes_faites, key=lambda e: e.niveau)[-1]
                # si l'étape courante fait partie d'une sous-quête non ordonée
                if etape.parent.type == "quete" and not etape.parent.ordonnee:
                    ret += "\n - " + etape.parent.titre + " :"
                    for s_etape in etape.parent.etapes.values():
                        if s_etape in etapes_a_faire \
                                and s_etape is not etape.parent \
                                and len(s_etape.niveau) == len(etape.niveau):
                            ret += "\n   " + s_etape.titre
                else:
                    ret += "\n - " + etape.titre
            else: # si elle n'est pas ordonnée
                for etape in quete.etapes.values():
                    if etape in etapes_a_faire and len(etape.niveau) == 1:
                        ret += "\n - " + etape.titre
        if all(q in terminees for q in faites):
            ret += "\n|att|Aucune quête en cours pour le moment.|ff|"
        if terminees:
            ret += "\n\n|tit|Vos quêtes accomplies :|ff|"
            for quete in terminees:
                ret += "\n - " + quete.titre
        personnage << ret
