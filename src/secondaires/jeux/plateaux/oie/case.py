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


"""Fichier contenant la classe Case définissant une case.

Elle contient également les différentes classe shéritées de Case et
définissant chacune une case spéciale (comme un piège).

"""

from abstraits.obase import BaseObj

class Case(BaseObj):

    """Classe définissant une case simple.

    Par défaut, une case simple possède :
        un titre
        un symbole
        une couleur
        un article ("sur" par défaut)
        un verbe ("arrivez" par défaut)
        un verbe pour les autres ("arrive" par défaut)

    Les méthodes définies dans une case sont :
        arrive -- un pion arrive sur cette case

    """

    numero = 1
    def __init__(self, titre, symbole, couleur, article="sur",
            verbe="arrivez", a_verbe="arrive", ponctuation="."):
        """Constructeur d'une case."""
        BaseObj.__init__(self)
        self.titre = titre
        self.symbole = symbole
        if len(symbole) > 1:
            raise ValueError("le symbole de la case {} fait plus " \
                    "d'un caractère".format(titre))
        self.couleur = couleur
        self.article = article
        self.verbe = verbe
        self.a_verbe = a_verbe
        self.ponctuation = ponctuation
        self.numero = Case.numero
        Case.numero += 1
        self._construire()

    def __getnewargs__(self):
        return ("", "", "")

    def __str__(self):
        return self.couleur + self.symbole + "|ff|"

    def arrive(self, jeu, plateau, partie, personnage, coup):
        """Le pion du personnage arrive sur la case."""
        pion = jeu.pions[personnage]
        personnage << "Vous {} {} {} ({}){}".format(
                self.verbe, self.article, self.titre, self.numero,
                self.ponctuation)
        partie.envoyer("Le pion {} {} {} {} ({}){}".format(
                pion.couleur, self.a_verbe,
                self.article, self.titre, self.numero, self.ponctuation),
                personnage)

class CaseOie(Case):

    """Classe représentant une case oie."""

    def __init__(self):
        """Constructeur de la case."""
        Case.__init__(self, "l'oie", "o", "|rg|")

    def __getnewargs__(self):
        return ()

    def arrive(self, jeu, plateau, partie, personnage, coup):
        """Le pion du personnage arrive sur la case."""
        Case.arrive(self, jeu, plateau, partie, personnage, coup)
        jeu.avancer(personnage, coup)

class CasePont(Case):

    """Classe représentant la case du pont."""

    def __init__(self):
        """Constructeur de la case."""
        Case.__init__(self, "le pont", "t", "|rg|")

    def __getnewargs__(self):
        return ()

    def arrive(self, jeu, plateau, partie, personnage, coup):
        """Le pion du personnage arrive sur la case."""
        Case.arrive(self, jeu, plateau, partie, personnage, coup)
        jeu.avancer(personnage, 6)

class CaseHotellerie(Case):

    """Classe représentant l'hôtellerie."""

    def __init__(self):
        """Constructeur de la case."""
        Case.__init__(self, "l'auberge", "x", "|rg|")

    def __getnewargs__(self):
        return ()

    def arrive(self, jeu, plateau, partie, personnage, coup):
        """Le pion du personnage arrive sur la case."""
        Case.arrive(self, jeu, plateau, partie, personnage, coup)
        pion = jeu.pions[personnage]
        personnage << "Vous êtes condamné à occuper cette case trois " \
                "tours durant."
        partie.envoyer("Le pion {} est condamné à occuper cette case trois " \
                "tours durant.".format(pion.couleur), personnage)
        jeu.hotellerie[personnage] = 2

class CasePuits(Case):

    """Classe représentant le puits."""

    def __init__(self):
        """Constructeur de la case."""
        Case.__init__(self, "le puits", "O", "|rg|", "dans", "tombez",
                "tombe", " !")

    def __getnewargs__(self):
        return ()

    def arrive(self, jeu, plateau, partie, personnage, coup):
        """Le pion du personnage arrive sur la case."""
        Case.arrive(self, jeu, plateau, partie, personnage, coup)
        if jeu.puits:
            autre = jeu.puits
            autre << "Vous pouvez sortir du puits !"
            a_pion = jeu.pions[autre]
            partie.envoyer("Le pion {} sort du puits.".format(a_pion.couleur),
                    autre)
        pion = jeu.pions[personnage]
        personnage << "Vous devez attendre que quelqu'un vous délivre."
        jeu.puits = personnage

class CasePrison(Case):

    """Classe représentant la prison."""

    def __init__(self):
        """Constructeur de la case."""
        Case.__init__(self, "la prison", "*", "|rg|", "dans", "entrez",
                "entre", " !")

    def __getnewargs__(self):
        return ()

    def arrive(self, jeu, plateau, partie, personnage, coup):
        """Le pion du personnage arrive sur la case."""
        Case.arrive(self, jeu, plateau, partie, personnage, coup)
        if jeu.prison:
            autre = jeu.prison
            autre << "Vous êtes libre ! Vous pouvez quitter la prison."
            a_pion = jeu.pions[autre]
            partie.envoyer("Le pion {} quitte la prison.".format(
                    a_pion.couleur), autre)
        pion = jeu.pions[personnage]
        personnage << "Vous devez attendre que quelqu'un vous délivre."
        jeu.prison = personnage

class CaseLabyrinthe(Case):

    """Classe représentant le labyrinthe."""

    def __init__(self):
        """Constructeur de la case."""
        Case.__init__(self, "le labyrinthe", "h", "|rg|", "sur", "arrivez",
                "arrive", " !")

    def __getnewargs__(self):
        return ()

    def arrive(self, jeu, plateau, partie, personnage, coup):
        """Le pion du personnage arrive sur la case."""
        Case.arrive(self, jeu, plateau, partie, personnage, coup)
        pion = jeu.pions[personnage]
        personnage << "Vous retournez à la case 30."
        partie.envoyer("Le pion {} retourne à la case 30.".format(
                pion.couleur), personnage)
        jeu.placer(personnage, 29)

class CaseMort(Case):

    """Classe représentant la tête de mort."""

    def __init__(self):
        """Constructeur de la case."""
        Case.__init__(self, "la tête de mort", "x", "|rg|", "sur", "tombez",
                "tombe", " !")

    def __getnewargs__(self):
        return ()

    def arrive(self, jeu, plateau, partie, personnage, coup):
        """Le pion du personnage arrive sur la case."""
        Case.arrive(self, jeu, plateau, partie, personnage, coup)
        pion = jeu.pions[personnage]
        personnage << "Vous devez recommencer du début !"
        partie.envoyer("Le pion {} doit recommencer du début !".format(
                pion.couleur), personnage)
        jeu.placer(personnage, 0)

class CaseJardin(Case):

    """Classe représentant le jardin, fin de la partie."""

    def __init__(self):
        """Constructeur de la case."""
        Case.__init__(self, "le jardin", "+", "|rg|")

    def __getnewargs__(self):
        return ()

    def arrive(self, jeu, plateau, partie, personnage, coup):
        """Le pion du personnage arrive sur la case."""
        Case.arrive(self, jeu, plateau, partie, personnage, coup)
        pion = jeu.pions[personnage]
        personnage << "|rg|Vous gagnez la partie !|ff|"
        partie.envoyer("|rg|Le pion {} gagne la partie !|ff|".format(
                pion.couleur), personnage)
        partie.terminer()
