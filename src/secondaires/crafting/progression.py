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


"""Fichier contenant la classe Progression, détaillée plus bas."""

from abstraits.obase import BaseObj

class Progression(BaseObj):

    """Classe représentant la progression d'un membre dans une guilde.

    Un membre d'une guilde (un personnage) possède un rang, mais
    aussi une progression, c'est-à-dire un niveau dans ce rang. La
    propriété 'progression' retourne un nombre entre 0 et 100 (un
    pourcentage d'avancement). Quand le joueur fabrique un objet de
    rang, il peut avancer dans son rang. Chaque objet de rang peut
    être configuré pour nécessiter d'être fait un certain nombre de
    fois. Par exemple :
        Une guilde possède un rang apprenti avec :
          Une épée (à faire 2 fois)
          Une hache (à faire 3 fois)
        Le joueur faisant une épée aura 1 point sur 5 (le total),
        donc 20% d'avancement. Si il fait deux épées, il aura 40%.
        Si il fait 3 épées, il aura toujours 40%, car l'épée n'a
        besoin d'être faite que deux fois.

    """

    def __init__(self, membre, rang):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.membre = membre
        self.rang = rang
        self.recettes = {}
        self._construire()

    def __getnewargs__(self):
        return (None, None)

    @property
    def progression(self):
        """Retourne la progression du membre en pourcentage."""
        if self.recettes:
            total = sum(r.nb_max for r in self.rang.recettes)
            accompli = sum(list(self.recettes.values()))
            progression = accompli / total * 100
            if progression < 1:
                return 1
            elif progression >= 100:
                return 100
            else:
                return int(progression)

        return 0

    def reussir_recette(self, recette):
        """Valide la recette.

        Les recettes validées par ce membre sont conservées dans
        le dictionnaire 'recettes' (clé de la recette: nombre de
        succès). Si le nombre de succès est supérieur au nombre
        nécessaire configuré, ne fait rien. Sinon augmente le nombre
        de succès.

        """
        # Cherche la recette dans le rang
        nb_max = -1
        for t_recette in self.rang.recettes:
            if t_recette.resultat == recette:
                nb_max = t_recette.nb_max
                break

        if nb_max < 0:
            raise ValueError("la recette {} n'a pas pu être trouvée " \
                    "dans le rang {}".format(recette, self.rang))

        nb = self.recettes.get(recette, 0)
        if nb < nb_max:
            self.recettes[recette] = nb + 1
            self._enregistrer()
            return True

        return False
