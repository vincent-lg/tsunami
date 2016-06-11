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


"""Ce module contient la classe Affection, détaillée plus bas."""

from abstraits.obase import BaseObj

class Affection(BaseObj):

    """Affection concrète, affectant un subissant (personnage, salle...).

    Quand un subissant est affecté (la neige tombe dans une salle, par
    exemple), si l'affection n'est pas encore présente, un objet de cette
    classe est créé. Il contient :
        L'objet indirectement hérité de AffectionAbstraite (Neige ici)
        Des valeurs propres à cette affection (sa durée restante, sa forcce)

    """

    def __init__(self, affection, affecte, duree, force):
        BaseObj.__init__(self)
        self.affecte = affecte
        self.affection = affection
        self.age = 0
        self.duree = duree
        self.force = force
        self._construire()
        if affection:
            affection.initialiser(self)

    def __getnewargs__(self):
        return (None, None, 0, 0)

    def __repr__(self):
        return "<affection de {} par {} (force={}, duree={})>".format(
                self.nom_affecte, self.cle_affection, self.force, self.duree)

    def __setstate__(self, dico_attrs):
        """Méthode appelée à la récfupération de l'objet."""
        BaseObj.__setstate__(self, dico_attrs)
        self.prevoir_tick()

    @property
    def nom_affecte(self):
        return self.affecte and self.affecte.nom_unique or "inconnu"

    @property
    def cle_affection(self):
        return self.affection and self.affection.cle or "aucune"

    def detruire(self):
        """Destruction de l'affection."""
        self.affection.programmer_destruction(self)
        BaseObj.detruire(self)

    def prevoir_tick(self):
        """Ajoute l'action à exécuter dans diffact."""
        nom = "aff_" + str(id(self))
        if self.affection.tick_actif:
            if nom not in importeur.diffact.actions:
                importeur.diffact.ajouter_action(nom,
                        self.affection.duree_tick, self.affection.tick, self)
