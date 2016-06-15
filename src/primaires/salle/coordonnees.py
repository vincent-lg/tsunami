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


"""Fichier contenant la classe Coordonnees, détaillée plus bas."""

from math import ceil

from abstraits.obase import *

class Coordonnees(BaseObj):

    """Classe représentant les coordonnées
    Ces coordonnées servent à la représentation dans l'espace (x, y et z). La
    classe peut être utilisée pour générer des coordonnées invalides.

    """

    def __init__(self, x=0, y=0, z=0, valide=True, parent=None):
        """Constructeur des coordonnées"""
        BaseObj.__init__(self)
        self.x = x
        self.y = y
        self.z = z
        self.valide = valide
        self.parent = parent
        # On passe le statut en CONSTRUIT
        self._construire()

    def __getnewargs__(self):
        return ()

    @property
    def invalide(self):
        """Retourne le contraire de 'valide'"""
        return not self.valide

    def __str__(self):
        """Affiche les coordonnées plus proprement"""
        if self.valide:
            res = "{}.{}.{}".format(int(self.x), int(self.y), int(self.z))
        else:
            res = "INV"
        return res

    def __repr__(self):
        """Affichage des coordonnées dans un cas de debug"""
        return "Coords(x={}, y={}, z={}, valide={})".format(self.x, self.y,
                self.z, self.valide)

    def __setattr__(self, attr, val):
        """Enregistre le parent si le parent est précisé"""
        anc_tuple = self.tuple_complet()
        construit = self.construit
        BaseObj.__setattr__(self, attr, val)
        if not attr.startswith("_") and attr not in ["parent"] and \
                construit and self.parent:
            mod_salle = type(self.parent).importeur.salle
            mod_salle.changer_coordonnees(anc_tuple, self)

    def tuple(self):
        """Retourne le tuple (x, y, z)"""
        if self.construit:
            return (self.x, self.y, self.z)
        else:
            return ()

    def tuple_complet(self):
        """Retourne self.tuple + self.valide"""
        if self.construit:
            return self.tuple() + (self.valide, )
        else:
            return ()

    def get_copie(self):
        """Retourne une copie de self, non liée à parent"""
        copie = Coordonnees(self.x, self.y, self.z, self.valide)
        return copie

    def entier(self):
        resultat_x = []
        resultat_y = []
        resultat = []
        if self.x - ceil(round(self.x, 1)) <= 0.6:
            resultat_x.append(ceil(round(self.x, 1)))
        if self.x - ceil(round(self.x, 1)) >= 0.4:
            resultat_x.append(ceil(round(self.x, 1)) + 1)
        if self.y - ceil(round(self.y, 1)) <= 0.6:
            for x in resultat_x:
                resultat_y.append((x, ceil(round(self.y, 1))))
        if self.y - ceil(round(self.y, 1)) >= 0.4:
            for x in resultat_x:
                resultat_y.append((x, ceil(round(self.y, 1)) + 1))
        if self.z - ceil(round(self.z, 1)) <= 0.6:
            for x, y in resultat_y:
                resultat.append(Coordonnees(x, y, ceil(round(self.z, 1))))
        if self.z - ceil(round(self.z, 1)) >= 0.4:
            for x, y in resultat_y:
                resultat.append(Coordonnees(x, y, ceil(round(self.z, 1)) + 1))
        return resultat

    def __eq__(self, autre):
        return isinstance(autre, Coordonnees) and self.x == autre.x and \
                self.y == autre.y and self.z == autre.z

    def __hash__(self):
        return hash(hash(self.x) ^ hash(self.y) ^ hash(self.z))

    @property
    def est(self):
        """Retourne la coordonnée non-liée vers l'est"""
        copie = self.get_copie()
        if copie.valide:
            copie.x += 1
        return copie

    @property
    def sudest(self):
        """Retourne la coordonnée non-liée vers le sud-est"""
        copie = self.get_copie()
        if copie.valide:
            copie.x += 1
            copie.y -= 1
        return copie

    @property
    def sud(self):
        """Retourne la coordonnée non-liée vers le sud"""
        copie = self.get_copie()
        if copie.valide:
            copie.y -= 1
        return copie

    @property
    def sudouest(self):
        """Retourne la coordonnée non-liée vers le sud-ouest"""
        copie = self.get_copie()
        if copie.valide:
            copie.x -= 1
            copie.y -= 1
        return copie

    @property
    def ouest(self):
        """Retourne la coordonnée non-liée vers l'ouest"""
        copie = self.get_copie()
        if copie.valide:
            copie.x -= 1
        return copie

    @property
    def nordouest(self):
        """Retourne la coordonnée non-liée vers le nord-ouest"""
        copie = self.get_copie()
        if copie.valide:
            copie.x -= 1
            copie.y += 1
        return copie

    @property
    def nord(self):
        """Retourne la coordonnée non-liée vers le nord"""
        copie = self.get_copie()
        if copie.valide:
            copie.y += 1
        return copie

    @property
    def nordest(self):
        """Retourne la coordonnée non-liée vers le nord-est"""
        copie = self.get_copie()
        if copie.valide:
            copie.x += 1
            copie.y += 1
        return copie

    @property
    def bas(self):
        """Retourne la coordonnée non-liée vers le bas"""
        copie = self.get_copie()
        if copie.valide:
            copie.z -= 1
        return copie

    @property
    def haut(self):
        """Retourne la coordonnée non-liée vers le haut"""
        copie = self.get_copie()
        if copie.valide:
            copie.z += 1
        return copie

    se = sudest
    so = sudouest
    no = nordouest
    ne = nordest
