# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Package contenant la commande 'emote'.

"""

from primaires.format.constantes import ponctuations_finales
from primaires.format.fonctions import echapper_accolades
from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

# Constantes
AIDE = r"""
Cette commande permet de jouer une action RP dans la salle où vous vous
trouvez. Tous les personnages présents dans la salle vous verront.
Par exemple, vous pouvez faire |ent|emote sifflote un air mélodieux|ff|
ou |ent|emote sourit|ff|.

Les messages que vous envoyez doivent être RP et réalistes, formattés
à la troisième personne du singulier, pour les autres joueurs présents
dans la salle. Quand vous entrez |cmd|emote chatonne d'un air distrait|ff|,
les autres personnages présents verront votre nom suivit du message
|ent|chantonne d'un air distrait.|ff|. Les règles de RP et de réalisme
impliquent que vous ne devez pas envoyer de message qui dépasse les
limites réalistes du gameplay (ne faites pas semblant de vous envoler
dans la salle) et ne doivent pas obliger d'autres personnages à
interagir (si vous interagissez avec un personnage présent, n'écrivez
pas la réaction pour lui, laissez-le libre de réagir comme il le semble
convenable).

Vous pouvez utiliser une syntaxe étendue pour inclure des noms
de personnages, objets ou détails de la salle. Dans votre emote, vous
pouvez précéder un nom du signe dollar ($). Le nom donné (la partie
se trouvant entre le signe dollar et un espace ou une ponctuation) sera
remplacé par le nom de l'élément observé (c'est la même règle que pour
la commande %regarder%). Par exemple, si vous voulez interagir avec
un personnage présent dans la salle dont le nom est "un orc à l'air
difficile", vous pouvez entrer |ent|emote regarde fixement $orc.|ff|
|ent|$orc|ff| sera cherché dans la salle et le personnage "un orc à l'air
difficile" sera sélectionné. Au final, les autres personnages présents
verront un message comme "un tel regarde fixement un orc à l'air difficile".
Si ils ont associé un nom à la distinction visible du personnage, ils
verront ce nom. Cette syntaxe peut être également utilisée pour les
objets (ceux au sol ou ceux dans votre inventaire) ainsi que les
détails de la salle, décors et autres informations.

Enfin, vous pouvez également affecter l'état de votre personnage avec cette
commande. L'état représente ce que les autres joueurs verront en regardant
la salle. Par exemple : se trouve ici, est assis au coin du feu, ronfle
bruyamment... Vous pouvez préciser votre état après un signe |ent|/|ff|.
Par exemple : |cmd|emote se met à chantonner / chantonne ici|ff|.
""".strip()

class CmdEmote(Commande):

    """Commande 'emote'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "emote", "emote")
        self.nom_categorie = "parler"
        self.schema = "<message>"
        self.aide_courte = "joue une emote dans la salle"
        self.aide_longue = AIDE

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        personnage.agir("geste")
        message = dic_masques["message"].message
        message = message.rstrip(" \n")
        message = echapper_accolades(message)

        # On vérifie la présence d'un / (barre oblique), qui signifie que
        # le joueur souhaite entrer un état pour son personnage
        if "/" in message:
            message, etat = message.split("/", 1)
            message = message.rstrip()
            etat = etat.rstrip(" .,?!").lstrip()
            personnage.etat_personnalise = etat

        # On traite les détails
        observable = importeur.interpreteur.masques["element_observable"]()
        elements = []
        for mot in list(message.split(" ")):
            if mot.startswith("$"):
                nom = mot[1:].rstrip(".,?; ")
                observable.init()
                masques = []
                try:
                    observable.repartir(personnage, masques, list(nom))
                except ErreurValidation as err:
                    personnage << str(err) + "."
                    return

                try:
                    observable.valider(personnage, {})
                except ErreurValidation as err:
                    personnage << str(err) + "."
                    return

                elements.append(observable.element)
                message = message.replace("$" + nom, "{}")

        if not message[-1] in ponctuations_finales:
            message += "."

        personnage.salle.envoyer("{{}} {}".format(message), personnage,
                *elements, ignore=False, lisser=True)
        if personnage.etat_personnalise:
            personnage.envoyer("{{}} {}".format(personnage.etat_personnalise),
                    personnage)

        importeur.communication.rapporter_conversation("emote",
                personnage, message)
