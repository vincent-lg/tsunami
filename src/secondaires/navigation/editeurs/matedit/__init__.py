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


"""Package contenant l'éditeur 'matedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from .edt_aptitudes import EdtAptitudes

class EdtMatedit(Presentation):

    """Classe définissant l'éditeur de fiche de matelot 'matedit'."""

    nom = "matedit"

    def __init__(self, personnage, fiche):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, fiche)
        if personnage and fiche:
            self.construire(fiche)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, fiche):
        """Construction de l'éditeur"""
        # Nom singulier
        singulier = self.ajouter_choix("nom singulier", "n", Uniligne,
                fiche, "nom_singulier")
        singulier.parent = self
        singulier.prompt = "Nom singulier avec déterminant : "
        singulier.apercu = "{objet.nom_singulier}"
        singulier.aide_courte = \
            "Entrez le |ent|nom singulier|ff| du matelot ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nNom singulier actuel : " \
            "|bc|{objet.nom_singulier}|ff|"

        # Nom pluriel
        pluriel = self.ajouter_choix("nom pluriel", "p", Uniligne,
                fiche, "nom_pluriel")
        pluriel.parent = self
        pluriel.prompt = "Nom pluriel sans déterminant : "
        pluriel.apercu = "{objet.nom_pluriel}"
        pluriel.aide_courte = \
            "Entrez le |ent|nom pluriel|ff| du matelot ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nNom pluriel actuel : " \
            "|bc|{objet.nom_pluriel}|ff|"

        # Description
        description = self.ajouter_choix("description", "d", Description,
                fiche)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description de la fiche de matelot {}".format(
            fiche.cle).ljust(76) + "|ff||\n" + self.opts.separateur

        # Poste par défaut
        poste = self.ajouter_choix("poste par défaut", "t", Uniligne,
                fiche, "poste_defaut")
        poste.parent = self
        poste.prompt = "Nom du poste par défaut du matelot : "
        poste.apercu = "{objet.poste_defaut}"
        poste.aide_courte = \
            "Entrez le |ent|nom du poste|ff| du matelot ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nPoste actuel : " \
            "|bc|{objet.poste_defaut}|ff|"

        # Aptitudes
        aptitudes = self.ajouter_choix("aptitudes", "a", EdtAptitudes,
                fiche)
        aptitudes.parent = self

        # Prix unitaire
        prix = self.ajouter_choix("prix unitaire", "u", Entier, fiche,
                "m_valeur")
        prix.parent = self
        prix.apercu = "{objet.m_valeur} pièces de bronze"
        prix.prompt = "Entrez le prix du matelot : "
        prix.aide_courte = \
            "Entrez |ent|le prix|ff| du matelot.\n\nPrix actuel : " \
            "{objet.m_valeur} pièces de bronze"
