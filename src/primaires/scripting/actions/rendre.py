# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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
# LIABLE FOR ANY rendreCT, INrendreCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action rendre."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Rend les objets donnés au PNJ.

    Cette action est très spécifique. Elle est à utiliser dans un
    évènement 'donne' dans le cas où on souhaite rendre ce que l'on
    a donné au PNJ. Elle peut être utilisé dans d'autres évènements,
    mais les variables 'pnj', 'personnage', 'objet' et 'quantite'
    doivent alors être présentes.

    """

    entrer_variables = True

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.rendre)
        cls.ajouter_types(cls.rendre, "str")

    @staticmethod
    def rendre(verbe="redonne", variables=None):
        """Rend les objets donnés au PNJ.

        Paramètres à entrer :

          * verbe : le verbe à utiliser (optionnel)

        Cette action suppose que les variables de l'évènement 'donne'
        existent : 'pnj' doit contenir le PNJ auquel on a donné les
        objets, 'personnage' doit contenir le personnage (joueur ou
        non) qui lui a donné les objets, 'objet' doit contenir l'objet
        ou le prototype d'objet donné et 'quantite' doit contenir la
        quantité d'objet donnés.
        L'utiliser est très simple si ces variables existent (ce qui
        est le cas dans l'évènement 'donner').

          rendre
          # Ou bien de façon plus personnalisée
          rendre "donne"

        La seule différence entre les deux syntaxes est le message
        qui sera envoyé au personnage qui reçoit les objets. Dans
        le premier cas, le message sera "${pnj} vous redonne ${objets}.">
        Dans le second, ce sera "${pnj} vous donne ${objets}.

        Cette action est plus rapide qu'un script désigné pour faire
        la même chose. Outre redonner les objets donnés, elle se charge
        des cas un peu plus difficiles à scripter qui se produisent quand :

          * Plusieurs objets sont donnés d'un coup au PNJ ;
          * L'objet en question est de l'argent, donc un objet non unique.

        """
        pnj = variables.get("pnj")
        personnage = variables.get("personnage")
        objet = variables.get("objet")
        quantite = variables.get("quantite")

        # Vérifie que les objets sont bien renseignés
        if any(v is None for v in (pnj, personnage, objet, quantite)):
            raise ErreurExecution("Des variables n'ont pas été définies " \
                    ": pnj={}, personnage={}, objet={}, quantite={}".format(
                    pnj, personnage, objet, quantite))

        quantite = int(quantite)
        personnage.envoyer("{{}} vous {verbe} {}.".format(objet.get_nom(
                quantite), verbe=verbe), pnj)
        if objet.unique:
            if quantite == 1:
                objets = {objet}
            else:
                objets = [o for o in pnj.equipement.inventaire if \
                        o.cle == objet.cle]
                objets = list(reversed(objets))[:quantite]

            for objet in objets:
                if objet.contenu:
                    try:
                        objet.contenu.retirer(objet)
                    except ValueError:
                        pass

                personnage.ramasser_ou_poser(objet)
        else:
            # L'objet est non unique
            pnj.retirer(objet, quantite)
            personnage.ramasser_ou_poser(objet, quantite)
