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
# ARE DISCLAIMED. IN NO Ematelot SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'poste' de la commande 'matelot'."""

from corps.fonctions import lisser
from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.equipage.postes.hierarchie import ORDRE

class PrmPoste(Parametre):

    """Commande 'matelot poste'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "poste", "position")
        self.schema = "<nom_matelot> <message>"
        self.tronquer = True
        self.aide_courte = "change un matelot de poste"
        self.aide_longue = \
            "Cette commande permet de demander à un matelot de changer de " \
            "poste. Cette commande est souvent utile au début d'un voyage " \
            "(ou juste après avoir recruté un nouveau membre d'équipage). " \
            "Certains matelots ont des postes de prédilection mais, par " \
            "choix, vous pourriez décider de les mettre à un autre poste. " \
            "Les matelots chargés de poste à responsabilité (capitaine, " \
            "second, maître d'équipage) doivent être choisis " \
            "indépendemment. Notez que le poste n'a pas de rapport direct " \
            "avec l'affectation : un voilier peut être affecté dans la " \
            "cale, une vigie dans la cabine. Il est préférable de placer " \
            "les matelots qui sont chargés de postes relativement statiques " \
            "proches des points du navire où ils devront opérer. Quand le " \
            "nombre de matelots sur un navire est plus important, il peut " \
            "être difficile d'affecter tout le monde et de leur changer " \
            "de poste : le maître d'équipage est là pour ça. Grâce à un " \
            "ordre (encore à venir), il se charge " \
            "d'affecter les matelots en fonction de leur aptitude " \
            "et de les mettre aux postes qui leur conviennent mieux. Il est " \
            "préférable cependant de choisir au moins le capitaine et " \
            "le maître d'équipage avant de donner cet ordre et il vous " \
            "appartient de choisir un second parmi les officiers " \
            "restants du bord, bien que cela ne soit, à proprement " \
            "parlé, pas nécessaire dans tous les cas. Pour utiliser " \
            "cette commande, vous devez d'abord préciser son nom (tel " \
            "qu'il s'affiche dans le %matelot% %matelot:liste%) et ensuite " \
            "le nom du poste, comme |ent|artilleur|ff|. Les postes " \
            "disponibles sont : " + ", ".join(ORDRE) + "."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        navire = salle.navire
        matelot = dic_masques["nom_matelot"].matelot
        nom_poste = dic_masques["message"].message
        equipage = navire.equipage

        if not navire.a_le_droit(personnage, "maître d'équipage"):
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        # On essaye de trouver le nom du poste (sans accents ni majuscules)
        nom = None
        for t_nom in ORDRE:
            if supprimer_accents(t_nom).lower() == supprimer_accents(
                    nom_poste).lower():
                nom = t_nom
                break

        if nom is None:
            personnage << "|err|Impossible de trouver le nom du poste : " \
                    "{}.|ff|".format(nom_poste)
        elif matelot.nom_poste == nom:
            personnage << "|err|Ce matelot est déjà à ce poste.|ff|"
        else:
            matelot.nom_poste = nom
            personnage << lisser("{} a bien été mis au poste de {}.".format(
                    matelot.nom, nom))
