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
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Module contenant la classe PromptNavigation, détaillée plus bas."""

from primaires.perso.prompt import Prompt
from primaires.vehicule.vecteur import get_direction

class PromptNavigation(Prompt):

    """Classe représentant le prompt affiché en navigation."""

    nom = "navigation"
    nom_anglais = "sailing"
    defaut = "Vit   {stats.vitalite}     Man   {stats.mana} " \
            "    End   {stats.endurance}{sl}Vitesse {vitesse} " \
            "{nom_direction} ({direction}°), Vent {direction_relative_vent}" \
            ", {etat_coque}."

    aide_courte = "prompt de navigation"
    aide_longue = "Ce prompt est affiché quand votre personnage navigue"
    symboles_sup = """
                %n          Nom du navire
                %t          Vitesse en noeuds du navire
                %d          Direction en degrés du navire
                %nd         Nom de la direction du navire
                %dv         Direction en degrés du vent
                %ndv        Nom de la direction du vent
                %drv        Direction relative du vent
                %ec         État de la coque (intacte ou endommagée)
    """.strip("\n")

    symboles = Prompt.symboles.copy()
    symboles["t"] = "vitesse"
    symboles["d"] = "direction"
    symboles["nd"] = "nom_direction"
    symboles["dv"] = "direction_vent"
    symboles["ndv"] = "nom_direction_vent"
    symboles["n"] = "nom"
    symboles["drv"] = "direction_relative_vent"
    symboles["ec"] = "etat_coque"

    @classmethod
    def calculer(cls, personnage, prompt):
        """Calcul et retourne le prompt calculé."""
        prompt = prompt if prompt is not None else cls.defaut
        salle = personnage.salle
        nom = "?"
        vitesse = "?"
        direction = "?"
        nom_direction = "?"
        direction_vent = "?"
        nom_direction_vent = "?"
        direction_relative_vent = "?"
        etat_coque = "?"
        if salle and getattr(salle, "navire", None):
            navire = salle.navire
            nom = navire.nom_personnalise or "?"
            vitesse = navire.donnees.get("vitesse", "?")
            direction = navire.donnees.get("direction", "?")
            nom_direction = navire.donnees.get("nom_direction", "?")
            direction_vent = navire.donnees.get("direction_vent", "?")
            nom_direction_vent = navire.donnees.get("nom_direction_vent", "?")
            nav_direction = navire.direction.direction
            vent = navire.vent

            if vent.mag == 0:
                direction_relative_vent = "huile"
            else:
                ven_direction = get_direction(vent)
                angle = (nav_direction - ven_direction) % 360
                precision = 10 # précision en degré
                angle = round(angle / precision) * precision
                tribord = True
                if angle > 180:
                    angle = (180 - angle) % 180
                    tribord = False

                cote = "tribord" if tribord else "bâbord"
                if angle == 0:
                    msg_vent = "arrière"
                elif angle < 50:
                    msg_vent = "arrière-{cote} ({angle}°)."
                elif angle < 130:
                    msg_vent = "hanche {cote} ({angle}°)."
                elif angle < 180:
                    msg_vent = "avant-{cote} ({angle}°)."
                else:
                    msg_vent = "devant"


                angle_contraire = (-angle) % 180
                direction_relative_vent = msg_vent.format(cote=cote,
                        angle=angle_contraire)

            voies_eau = navire.nb_voies_eau
            if voies_eau > 1:
                etat_coque = "{} coques ouvertes".format(voies_eau)
            elif voies_eau == 1:
                etat_coque = "une coque ouverte"
            else:
                etat_coque = "intacte"

        return prompt.format(
                stats=personnage.stats,
                sl="\n",
                vitesse=vitesse,
                direction=direction,
                nom_direction=nom_direction,
                direction_vent=direction_vent,
                nom_direction_vent=nom_direction_vent,
                nom=nom,
                direction_relative_vent=direction_relative_vent,
                etat_coque=etat_coque,
        )
