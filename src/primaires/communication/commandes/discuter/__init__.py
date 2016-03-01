# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Package contenant la commande 'discuter'.

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import echapper_accolades

class CmdDiscuter(Commande):

    """Commande 'discuter'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "discuter", "talk")
        self.nom_categorie = "parler"
        self.schema = "<nom_pnj> (de/about <message>)"
        self.aide_courte = "engage une discussion avec un PNJ"
        self.aide_longue = \
            "Cette commande permet d'engager la discussion avec " \
            "un PNJ (personnage non joueur) présent dans la salle " \
            "où vous vous trouvez. Dans sa forme la plus simple, " \
            "vous devez simplement entrer %discuter% suivi du nom " \
            "du personnage (par exemple %discuter%|cmd| tavernier|ff|). " \
            "Cette syntaxe permet d'engager la conversation avec le " \
            "PNJ sans aborder aucun sujet en particulier, ce qui " \
            "est parfois utile pour débuter une quête dont vous ne " \
            "connaissez pas le début. Tous les PNJ ne réagiront pas " \
            "forcément. Vous pouvez aussi discuter d'un sujet précis " \
            "en le précisant après le mot-clé |cmd|de|ff| (ou " \
            "|cmd|about|ff| en anglais). Par exemple : |cmd|discuter " \
            "tavernier de travail|ff| (ou |cmd|talk tavernier about " \
            "travail|ff|). Les sujets de conversation sont en général " \
            "constitués que d'un seul mot pour éviter la confusion " \
            "(n'essayez pas d'entrer une phrase complète, les PNJ " \
            "n'y réagiront vraissemblablement pas). Le sujet est " \
            "souvent lié au contexte : si le PNJ vous a posé une " \
            "question, n'hésitez pas à utiliser le sujet |ent|oui|ff| " \
            "ou |ent|non|ff| par exemple. Ce peut aussi être un " \
            "élément intriguant dans le lieu où se trouve le PNJ ou " \
            "bien des rumeurs concernant un évènement particulier, " \
            "pour ne citer que certaines des possibilités"

    def ajouter(self):
        """Méthode appelée quand on ajoute la commande à l'interpréteur"""
        mot_cle = self.noeud.suivant.suivant.interne.masque
        mot_cle.gauche = True

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        personnage.agir("parler")
        if dic_masques["message"] is None:
            message = ""
            ret = "Vous engagez la discussion avec {}."
        else:
            message = echapper_accolades(dic_masques["message"].message)
            ret = "Vous engagez la discussion avec {} à propos de \"{}\"."
        pnj = dic_masques["nom_pnj"].pnj
        personnage << ret.format(pnj.get_nom_pour(personnage), message)

        # Appel de l'évènement 'discute' du PNJ
        pnj.script["discute"].executer(sujet=message, personnage=personnage,
                pnj=pnj)
