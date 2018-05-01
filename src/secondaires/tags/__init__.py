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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le module secondaire tags."""

from textwrap import dedent

from abstraits.module import *
from corps.fonctions import valider_cle
from primaires.format.fonctions import format_nb
from secondaires.tags import commandes
from secondaires.tags.editeurs.selection_tags import SelectionTags
from secondaires.tags.tag import Tag
from secondaires.tags.tags import Tags

class Module(BaseModule):

    """Module gérant les tags de différentes natures.

    Un tag représente une fonctionnalité que l'on peut appliquer, par exemple, sur un objet ou un PNJ. Les tags facilitent aussi la copie de scripts.

    Par exemple, ce module permettrait de créer un tag 'marchand'
    pour les PNJ. Les PNJ vendeurs de magasin pourraient avoir ce
    tag, ce qui simplifierait la recherche dans plusieurs cas. En
    outre, les scripts sélectionnés seraient copiés, permettant
    d'avoir une réplique des fonctionnalités sur plusieurs PNJ. Bien
    que les types de tag soient définis dans le code, créer et appliquer
    un tag peut se faire dans l'univers sans difficulté.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "tags", "secondaire")
        self.tags = {}
        self.configuration = None
        self.types = ["objet", "pnj", "salle"]
        self.cles = {}
        self.logger = self.importeur.man_logs.creer_logger("tags", "tags")

    def config(self):
        """Configuration du module."""
        self.importeur.scripting.a_charger.append(self)
        BaseModule.config(self)

    def init(self):
        """Chargement des objets du module."""
        # Abonnement aux hooks
        self.importeur.hook["editeur:etendre"].ajouter_evenement(
                self.ajouter_tags)

        # Charge les tags
        self.configuration = self.importeur.supenr.charger_unique(Tags)
        if self.configuration is None:
            self.configuration = Tags()

        tags = self.importeur.supenr.charger_groupe(Tag)
        groupes = {}
        for tag in tags:
            self.ajouter_tag(tag)
            if tag.type not in groupes:
                groupes[tag.type] = []

            groupe = groupes[tag.type]
            groupe.append(tag)

        self.logger.info(format_nb(len(tags),
                "{nb} tag{s} récupéré{s}"))

        for type, groupe in groupes.items():
            self.logger.info(format_nb(len(groupe),
                    "Dont {nb} tag{s} du type " + type))

        # Réferencement des clés
        self.cles = {
                "objet": importeur.objet._prototypes,
                "pnj": importeur.pnj._prototypes,
                "salle": importeur.salle._salles,
        }

        # Abbonnement aux hooks
        self.importeur.hook["recherche:filtres"].ajouter_evenement(
                self.recherche_tags)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.tags.CmdTags(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

    def creer_tag(self, cle, type):
        """Crée un nouveau tag."""
        valider_cle(cle)

        if type not in self.types:
            raise ValueError("le type de tag {} n'existe pas".format(
                    repr(type)))

        if cle in self.tags:
            raise ValueError("le tag {} existe déjà".format(
                    repr(cle)))

        tag = Tag(cle, type)
        self.ajouter_tag(tag)
        return tag

    def ajouter_tag(self, tag):
        """Ajoute le tag."""
        if tag.cle in self.tags:
            raise ValueError("le tag de clé {} est " \
                    "déjà défini".format(repr(tag.cle)))

        self.tags[tag.cle] = tag

    def supprimer_tag(self, cle):
        """Supprime un tag."""
        if cle not in self.tags:
            raise ValueError("le tag {} n'existe pas".format(
                    repr(cle)))

        self.tags.pop(cle).detruire()

    def ajouter_tags(self, editeur, presentation, objet):
        """Ajoute l'éditeur de tags aux éditeurs."""
        if editeur.lower() in self.types:
            liste = [t.cle for t in self.tags.values() if t.type == \
                    editeur.lower()]
            liste.sort()
            lst_tags = self.configuration[objet]
            tags = presentation.ajouter_choix("tags", None,
                    SelectionTags, lst_tags,
                    "tags", liste, objet)
            tags.parent = presentation
            tags.apercu = "{valeur}"
            tags.aide_courte = dedent("""
                Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

                Vous pouvez ici ajouter et supprimer des tags pour '{nom}'.
                Si vous ajoutez un tag, en entrant son nom, les scripts
                associés à ce tag seront automatiquement copiés dans
                '{nom}'.

                Tags possibles : {liste}

                Tags actuels : {{valeur}}""".format(nom=str(objet),
                liste=liste).lstrip("\n"))

    def recherche_tags(self, cherchable):
        """Ajout de la recherche par tags."""
        if cherchable.nom_cherchable in ("probjet", "prpnj", "salle"):
            cherchable.ajouter_filtre("", "tags", self.filtrer_tags, "chaine")

    def filtrer_tags(self, objet, tags):
        """Filtre les données possédant le ou les tags indiqués.

        Vous pouvez préciser en argument un seul tag, ou bien une
        liste de tags séparés par un espace. Si l'un des tags est
        présent dans la donnée, elle sera affichée.

        """
        o_tags = importeur.tags.configuration[objet].tags
        return any(tag.lower() in o_tags for tag in tags.split(" "))
