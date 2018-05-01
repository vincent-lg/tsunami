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
# ARE DISCLAIMED. IN NO Eéquipage SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'objectif' de la commande 'équipage'."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.parametre import Parametre

class PrmObjectif(Parametre):

    """Commande 'équipage objectif'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "objectif", "objective")
        self.tronquer = True
        self.schema = "(<nombre>)"
        self.aide_courte = "consulte ou modifie les objectifs"
        self.aide_longue = \
            "Les objectifs sont des ordres permanents qui peuvent " \
            "rester en sommeil pendant un temps indéfini. Généralement, " \
            "seul le premier objectif est actif, les autres sont en " \
            "attente, même si ils peuvent influencer la manoeuvre. " \
            "Concrètement, un objectif est un but fixé pour un équipage, " \
            "comme \"se rendre à un point indiqué\", \"attaquer le " \
            "navire que l'on voit à l'horizon\", \"chercher à accoster " \
            "dans le port voisin\". La différence avec de simples " \
            "ordres, c'est qu'ils sont maintenus pendant toute la durée " \
            "de leur accomplissement et sont faits pour évoluer au " \
            "cours d la manoeuvre. Par exemple, aller vers une côte " \
            "ou un autre navire peut être une combinaison d'ordres " \
            "assez simples, mais il faut tenir compte de plusieurs " \
            "facteurs qui pourraient modifier la manoeuvre, comme la " \
            "position du vent si il tourne, l'apparition d'un autre " \
            "navire sur la trajectoire assignée, la modification du " \
            "cap si le navire cible se déplace. Un objectif crée " \
            "généralement des contrôles : à la différence des objectifs, " \
            "les contrôles ne peuvent se contredire. Vous pourriez " \
            "avoir deux objectifs actifs : l'un demandant à se rendre " \
            "vers une côte située vers l'est, l'autre demandant " \
            "d'attaquer un navire à l'ouest. Dans ce cas, le commandant " \
            "choisit l'objectif le plus prioritaire (celui en haut " \
            "de la liste) et donne les ordres pour atteindre la " \
            "côte à l'est. En revanche, si l'objectif pour attaquer " \
            "le navire cible est maintenu, pendant l'accomplissement " \
            "du premier objectif, une manoeuvre pourrait permettre à " \
            "la cible d'être à portée de canon. C'est pour cela que " \
            "les objectifs sont maintenus même si ils s'opposent en " \
            "apparence. Vous pouvez entrer cette commande sans " \
            "paramètre pour voir les objectifs actuellement donnés " \
            "à votre équipage. Notez que le premier (numéroté |ent|1|ff|) " \
            "est considéré comme l'objectif actif, celui par lequel " \
            "les décisions conflictuelles sont tranchées. Les autres " \
            "objectifs sont conservés mais ne font pas partie des " \
            "décisions du commandant, sauf si il n'y a aucun conflit " \
            "dans les objectifs non prioritaires. Vous pouvez " \
            "également entrer cette commande en précisant un numéro " \
            ": l'objectif du numéro indiqué sera retiré et ne fera " \
            "plus parti des décisions prises par le commandant."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        navire = getattr(salle, "navire", None)
        if navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        if not navire.a_le_droit(personnage, "officier"):
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        equipage = salle.navire.equipage
        nombre = dic_masques["nombre"]
        if nombre:
            nombre = nombre.nombre
            if nombre < 0 or nombre > len(equipage.objectifs):
                personnage << "|err|Numéro d'objectif invalide.|ff|"
                return

            nombre = nombre - 1
            objectif = equipage.objectifs[nombre]
            equipage.retirer_objectif(nombre)
            personnage << "L'objectif a bien été supprimé : {}.".format(
                    objectif.afficher())
            return

        if not equipage.objectifs:
            personnage << "Aucun objectif actif sur cet équipage."
            return

        msg = "Objectifs actifs :\n"
        for i, objectif in enumerate(equipage.objectifs):
            msg += "\n|ent|{}|ff| - {}".format(str(i + 1).rjust(2),
                    objectif.afficher())

        personnage << msg
