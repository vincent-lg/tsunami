# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce module contient la classe AffectionAbstraite, détaillée plus bas."""

from fractions import Fraction

from abstraits.obase import BaseObj
from corps.fonctions import valider_cle
from .affection import Affection

class AffectionAbstraite(BaseObj):

    """Affection abstraite, propre à toutes les affections."""

    nom_type = "non renseigné"
    enregistrer = True
    def_flags = {}

    def __init__(self, cle):
        if cle:
            valider_cle(cle)

        BaseObj.__init__(self)
        self.resume = "non spécifié"
        self.visible = True
        self.cle = cle
        self.force_max = 50
        self.duree_max = -1
        self.infinie = False
        self.variation = -1
        self.duree_tick = 60 # durée du tick en secondes
        self.flags = 0

        # Liste de tuple (force, message)
        self.messages_visibles = []

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return "<affection de {} {}>".format(self.nom_type, self.cle)

    def _get_duree_max_ticks(self):
        """Returne la durée en ticks."""
        return 60 * self.duree_max / self.duree_tick
    def _set_duree_max_ticks(self, duree):
        """Modifie la durée en ticks."""
        self.duree = Fraction(duree) * self.duree_tick / 60
    duree_max_en_ticks = property(_get_duree_max_ticks, _set_duree_max_ticks)

    @property
    def aff_duree_max_en_ticks(self):
        """Affichage de la durée."""
        duree_ticks = self.duree_max_en_ticks
        if duree_ticks < 0:
            return "infinie"

        return str(duree_ticks)

    def a_flag(self, nom_flag):
        """Retourne True si l'affection a le flag, False sinon."""
        valeur = type(self).def_flags[nom_flag]
        return self.flags & valeur != 0

    def initialiser(self, affection):
        """Initialise une affection concrète.

        ATTENTION : cette méthode est appelée quand une affection est donnée
        (à un personnage ou à une salle par exemple) mais n'est pas
        appelée quand l'affection est simplement modulée.

        """
        pass

    def message(self, affection):
        """Retourne le message visible en fonction de la forde."""
        messages = self.messages_visibles
        for t_force, message in messages:
            if affection.force <= t_force:
                return message

        if messages:
            return messages[-1][1]
        else:
            return ""

    def equilibrer_force(self, force):
        """Équilibre la force et retourne la force_max si besoin."""
        if self.force_max >= 0 and force > self.force_max:
            force = self.force_max

        return force

    def equilibrer_duree(self, duree):
        """Équilibre la durée et retourne la duree_max si besoin."""
        if self.duree_max >= 0 and duree > self.duree_max:
            duree = self.duree_max

        return duree

    def moduler(self, affection, duree, force):
        """Module, c'est-à-dire remplace simplement les forces et durées."""
        affection.duree = self.equilibrer_duree(duree)
        affection.force = self.equilibrer_force(force)

    def verifier_validite(self, affection):
        """Vérifie la validité de l'affection.

        On se contente ici d'appeler le script de l'affection.

        """
        self.executer_script("valide", affection)

    def dec_duree(self, affection, duree=1):
        """Décrémente (ou non) la durée (et/ou la force) de l'affection.

        Cette méthode est appelée toutes les minutes et permet de
        décrémenter ou modifier la durée d'une affection. Certaines
        affections sont 'infinies', donc leur durée ne se décrémente
        jamais (et elles doivent être détruites d'autre façon,
        par des scripts bien souvent).

        Cette méthode modifie également la force d'une affection. Elle
        la rééquilibre parfois en fonction de la durée. Mais parfois
        certaines affections deviennent de plus en plus fortes au fur
        et à mesure que le temps passe.

        """
        if self.infinie:
            return

        if affection.duree == 0:
            return

        fact_dec = (affection.duree - duree) / affection.duree
        duree = affection.duree - duree
        if self.variation == 0: # La force ne bouge pas
            force = affection.force
        elif self.variation < 0: # La force se décrémente
            force = affection.force * fact_dec
        else:
            force = affection.force / fact_dec

        force = self.equilibrer_force(force)
        duree = self.equilibrer_duree(duree)
        affection.force = force
        affection.duree = duree
        self.verifier_validite(affection)
        if affection.duree <= 0:
            affection.detruire()

    def programmer_destruction(self, affection):
        """L'affection concrète passée en paramètre se détruit."""
        pass

    def executer_script(self, evenement, affection, **variables):
        """Exécute le script lié."""
        raise NotImplementedError

    def tick(self, affection):
        """Méthode appelée à chaque tick de l'action.

        NOTE IMPORTANTE : le tick N'EST PAS forcément toutes les
        minutes. Pour les affections, le tick peut s'exécuter toutes
        les 3 secondes ou toutes les 20 secondes, ce paramètre est
        réglable par les adimnistrateurs.

        """
        # On appelle le script tick
        if affection.e_existe:
            self.executer_script("tick", affection)

        # On ajoute l'action différée
        if affection.e_existe:
            importeur.diffact.ajouter_action("aff_" + str(id(affection)),
                    self.duree_tick, self.tick, affection)
