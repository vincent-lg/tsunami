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


"""Package contenant la commande 'setquest'"""

from primaires.interpreteur.commande.commande import Commande

class CmdSetQuest(Commande):

    """Commande 'setquest'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "setquest", "setquest")
        self.groupe = "administrateur"
        self.schema = "<nom_joueur> (<cle_quete> <message>)"
        self.aide_courte = "met à jour les quêtes d'un joueur"
        self.aide_longue = \
            "Cette commande modifie les niveaux qu'a accompli un joueur " \
            "une quête. Pour voir la liste des quêtes en cours ou " \
            "terminées, n'entrez que le |ent|nom|ff| du joueur ; si vous " \
            "ajoutez la |ent|clé|ff| d'une quête en particulier vous " \
            "obtiendrez la liste des étapes qu'il a complétées. Enfin, " \
            "précisez un ou plusieurs |ent|niveaux|ff| pour les ajouter " \
            "ou les retirer (par exemple : %setquest% |cmd|Alkareth " \
            "chasseur_picte 1,2.1,2.2,2.3,3|ff|). Le |ent|0|ff| nettoie " \
            "la liste."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage_mod = dic_masques["nom_joueur"].joueur
        quete = None
        if dic_masques["cle_quete"]:
            quete = dic_masques["cle_quete"].quete
        niveaux = ""
        if dic_masques["message"]:
            niveaux = dic_masques["message"].message

        if not quete:
            if not niveaux:
                ret = "Quêtes en cours ou finies pour {} :\n  ".format(
                        personnage_mod.nom)
                faites = [q.cle for q in importeur.scripting.quetes.values() \
                        if personnage.quetes[q.cle].niveaux != [(0, )]]
                if not faites:
                    ret += "|att|aucune pour l'instant|ff|"
                else:
                    ret += "\n  ".join(faites)
                personnage << ret
            else:
                personnage << "|err|Vous devez préciser une clé de quête.|ff|"
                return
        else:
            if not niveaux:
                if personnage_mod.quetes[quete.cle].niveaux == [(0, )]:
                    personnage << "|err|{} n'a pas fait la quête " \
                            "{}.|ff|".format(personnage_mod.nom, quete.cle)
                    return
                ret = "Etapes accomplies par {} dans la quête {} :\n  ".format(
                    personnage_mod.nom, quete.cle)
                etapes = []
                for n in personnage_mod.quetes[quete.cle].niveaux:
                    n = [str(niv) for niv in n]
                    etapes.append(quete.etapes[".".join(n)])
                ret += "\n  ".join(sorted([e.str_niveau + " - " + e.titre \
                        for e in etapes]))
                personnage << ret
            else:
                # On valide les niveaux
                if niveaux == "0":
                    try:
                        personnage_mod.quetes.vider(quete.cle)
                    except KeyError:
                        personnage << "|err|{} n'a pas fait la quête " \
                            "{}.|ff|".format(personnage_mod.nom, quete.cle)
                    else:
                        personnage << "|att|La quête {} a bien été " \
                                "réinitialisée pour {}.|ff|".format(
                                quete.cle, personnage_mod.nom)
                else:
                    niveaux = (tuple(int(n) for n in niveaux.split(".")), )
                    quete_mod = personnage_mod.quetes.get_quete(quete.cle)
                    quete_mod.changer_niveaux(niveaux)
                    personnage << "|att|La quête {} a bien été " \
                            "mise à jour pour {}.|ff|".format(
                            quete.cle, personnage_mod.nom)
