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


"""Package contenant l'éditeur pour les chantiers navals.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

"""

from textwrap import dedent

from primaires.interpreteur.editeur.choix_objet import ChoixObjet
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.tableau import Tableau

class EdtChantierNaval(Presentation):

    """Classe définissant l'éditeur de chantier naval."""

    nom = "chnaedit"

    def __init__(self, personnage, chantier):
        """Constructeur de l'éditeur."""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, chantier)
        if personnage and chantier:
            self.construire(chantier)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, chantier):
        """Construction de l'éditeur"""
        # Étendue
        etendue = self.ajouter_choix("étendue", None, ChoixObjet,
                chantier, "etendue", importeur.salle.etendues)
        etendue.parent = self
        etendue.apercu = "{valeur}"
        etendue.prompt = "Étendue d'eau du chantier naval : "
        etendue.aide_courte = dedent("""
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

            Vous pouvez ici configurer l'étendue d'eau du chantier naval.
            Cette information est utile pour permettre au chantier de savoir
            dans quelle étendue mettre les navires en cale sèche, si cela
            s'avère nécessaire. Les points du chantier permettent de
            configurer plus précisément les limites du chantier naval
            (voir le paramètrage des points dans l'éditeur).

            Étendue d'eau actuelle : {valeur}
        """.strip("\n"))

        # Magasin
        magasin = self.ajouter_choix("magasin", None, ChoixObjet,
                chantier, "salle_magasin", importeur.salle._salles)
        magasin.parent = self
        magasin.apercu = "{valeur}"
        magasin.prompt = "Magasin du chantier naval : "
        magasin.aide_courte = dedent("""
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

            Vous pouvez ici configurer le magasin du chantier naval.
            Ce magasin est une salle de l'univers existante, configurée
            avec un magasin. Ce sera dans cette salle que les joueurs
            pourront faire les demandes au chantier (achat/vente de
            navire, réparation, changement de nom, etc).

            Magasin actuel : {valeur}
        """.strip("\n"))

        # Questeur
        questeur = self.ajouter_choix("questeur", None, ChoixObjet,
                chantier, "salle_questeur", importeur.salle._salles)
        questeur.parent = self
        questeur.apercu = "{valeur}"
        questeur.prompt = "Questeur du chantier naval : "
        questeur.aide_courte = dedent("""
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

            Vous pouvez ici configurer le questeur du chantier naval.
            Lier un chantier naval à un questeur permet de simplifier
            certaines transactions. Un chantier naval relié à un questeur
            accepte de servir de dépot-vente : les joueurs peuvent y
            vendre des navires à d'autres joueurs en fixant un prix. Si
            un autre joueur achète le navire, le produit de la vente
            (moins une commission prélevée par le chantier) sera versé
            au compte du questeur du joueur vendant le navire.

            Questeur actuel : {valeur}
        """.strip("\n"))

        # Points
        points = self.ajouter_choix("points", None, Tableau,
                chantier, "points",
                (("x", "entier"), ("y", "entier"), ("z", "entier")))
        points.parent = self
        points.apercu = "{taille}"
        points.aide_courte = dedent("""
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

            Vous pouvez ici configurer la liste des points du chantier.
            Un point est tout simplement une coordonnée entière (sous
            la forme X.Y.Z. Un chantier naval n'opère que dans les limites
            définies par ces points. Pour être géré par le chantier (être
            vendu, mis en cale sèche), un navire doit se trouver dans l'étendue
            d'eau du chantier naval et sur l'un des points définis ici.
            De même, un navire vendu par le chantier, ou remis à l'eau
            après un passage en cale sèche, sera placé sur l'un des
            points libres définis ici.
            Pour entrer un point, précisez ses coordonnées X, Y et Z
            séparées par un signe |cmd|/|ff|. Par exemple :
                |cmd|8 / -3 / 0|ff|
            Pour supprimer un point, entrez l'option |cmd|/s|ff| suivie
            du numéro de la ligne à supprimer. Par exemple :
                |cmd|/s 4|ff|

            Points actuels :
            {valeur}
        """.strip("\n"))
