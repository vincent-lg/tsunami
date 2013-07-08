# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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

"""Module contenant la classe PGFormat."""

driver = True

import re

try:
    import postgresql
    from postgresql.exceptions import ClientCannotConnectError
except ImportError:
    driver = False

from primaires.format.fonctions import supprimer_accents

from secondaires.exportaide.formats.pgsql.config import TEXTE_CFG

class PGFormat:

    """Classe contenant la définition du format d'export 'pgsql'."""

    def __init__(self):
        self.cfg = None
        self.connection = None
        self.adresse_commandes = ""

    def peut_tourner(self):
        return driver

    def config(self):
        """Configure le format."""
        self.cfg = type(importeur).anaconf.get_config("exportaide.pg",
                "exportaide/pgsql/config.cfg", "modele export PG", TEXTE_CFG)
        self.adresse_commandes = self.cfg.adresse_commandes

    def init(self):
        """Initialisation du module.

        On essaye de se connecter. Si on ne peut pas, False est
        retourné.

        """
        host = self.cfg.host
        port = self.cfg.port
        dbuser = self.cfg.dbuser
        dbpass = self.cfg.dbpass
        dbname = self.cfg.dbname
        try:
            self.connexion = postgresql.open(
                    "pq://{user}:{password}@{host}:{port}/{database}".format(
                    user=dbuser, password=dbpass, host=host, port=port,
                    database=dbname))
        except ClientCannotConnectError:
            return False

        return True

    def exporter_commandes(self):
        """Exporte les commandes."""
        commandes = [noeud.commande for noeud in \
                importeur.interpreteur.commandes]
        # Sélectionne les commandes déjà créées
        query = self.connexion.prepare("SELECT slug FROM commands")
        crees = list(query())
        crees = [ligne[0] for ligne in crees]
        nb_commandes = 0
        for commande in commandes:
            nb_commandes += self.exporter_commande(commande, crees)

        print(nb_commandes, "commandes migrées")

    def exporter_sujets(self):
        """Exporte les sujets d'aide."""
        sujets = [sujet for sujet in importeur.information.sujets.values() if \
                sujet.str_groupe in ("aucun", "joueur", "pnj")]

        # Sélectionne les sujets déjà créés
        query = self.connexion.prepare("SELECT slug FROM topics")
        crees = list(query())
        crees = [ligne[0] for ligne in crees]
        nb_sujets = 0
        for sujet in sujets:
            nb_sujets += self.exporter_sujet(sujet, crees)

        print(nb_sujets, "sujets d'aide migrées")

    def get_slug_commande(self, commande):
        """Retourne le slug de la commande."""
        nom = supprimer_accents(commande.adresse)
        nom = nom.replace(":", "_")
        return nom

    def get_nom_commande(self, commande):
        """Retourne le nom français et anglais de la commande."""
        return commande.nom_francais + "/" + commande.nom_anglais

    def transformer_texte(self, texte):
        """Retourne le texte transformé.

        Les caractères spéciaux comme |att|, |cmd| sont transformés
        en tags HTML.

        """
        re_cmd = r"\%(.*?)\%"
        for autre_cmd in list(re.findall(re_cmd, texte)):
            autre = importeur.interpreteur.trouver_commande(autre_cmd)
            slug = supprimer_accents(autre_cmd).replace(":", "_")
            link = "<a href=\"" + self.adresse_commandes + slug
            link += "\">" + self.get_nom_commande(autre) + "</a>"
            texte = texte.replace("%" + autre_cmd + "%", link)

        balises = (
            (r"\|cmd\|(.*?)\|ff\|", r"<span class=\"commande\">\1</span>"),
            (r"\|ent\|(.*?)\|ff\|", r"<span class=\"commande\">\1</span>"),
            (r"\|att\|(.*?)\|ff\|", r"<span class=\"attention\">\1</span>"),
            (r"\|err\|(.*?)\|ff\|", r"<span class=\"erreur\">\1</span>"),
            (r"\|[a-z]+?\|", r""),
        )

        for pattern, repl in balises:
            texte = re.sub(pattern, repl, texte)

        return texte

    def exporter_commande(self, commande, crees):
        """Exporte la commande spécifiée."""
        if commande.groupe not in ("pnj", "joueur"):
            return 0

        nb = 1
        slug = self.get_slug_commande(commande)
        parent = ""
        if commande.parente:
            parent = self.get_slug_commande(commande.parente)

        aide_courte = self.transformer_texte(commande.aide_courte)
        aide_longue = self.transformer_texte(commande.aide_longue)
        syntaxe = commande.noeud.afficher()
        if slug in crees:
            query = \
                "UPDATE commands SET french_name=$1, " \
                "english_name=$2, category=$3, " \
                "syntax=$4, synopsis=$5, help=$6, parent_id=$7 " \
                "WHERE slug=$8"
            preparation = self.connexion.prepare(query)
            preparation(commande.nom_francais, commande.nom_anglais,
                    commande.categorie.nom, syntaxe, aide_courte,
                    aide_longue, parent, slug)
        else:
            query = \
                "INSERT INTO commands (slug, french_name, " \
                "english_name, category, syntax, synopsis, " \
                "help, parent_id) values($1, $2, $3, $4, $5, $6, $7, $8)"
            preparation = self.connexion.prepare(query)
            preparation(slug, commande.nom_francais, commande.nom_anglais,
                    commande.nom_categorie, syntaxe, aide_courte,
                    aide_longue, parent)
            crees.append(slug)

        if commande.parametres:
            for parametre in commande.parametres.values():
                nb += self.exporter_commande(parametre.commande, crees)

        return nb

    def exporter_sujet(self, sujet, crees):
        """Exporte le sujet d'aide spécifié."""
        if sujet.str_groupe not in ("aucun", "pnj", "joueur"):
            return 0

        nb = 1
        cle = sujet.cle
        profondeur = self.get_profondeur_sujet(sujet)
        position = self.get_position_sujet(sujet)
        parent = ""
        if sujet.pere:
            parent = sujet.pere.cle

        contenu = []
        for paragraphe in sujet.contenu.paragraphes:
            contenu.append(self.transformer_texte(paragraphe))

        contenu = "\n".join(contenu)
        contenu = contenu.replace("\n\n", "</p><p>")
        contenu = "<p>" + contenu.replace("\n", "<br />") + "</p>"
        if cle in crees:
            query = \
                "UPDATE topics SET title=$1, content=$2, parent_id=$3, " \
                "depth=$4, position=$5 WHERE slug=$6"
            preparation = self.connexion.prepare(query)
            preparation(sujet.titre, contenu, parent, profondeur, position,
                    cle)
        else:
            query = \
                "INSERT INTO topics (slug, title, content, parent_id, " \
                "depth, position) values($1, $2, $3, $4, $5, $6)"
            preparation = self.connexion.prepare(query)
            preparation(cle, sujet.titre, contenu, parent, profondeur,
                    position)
            crees.append(cle)

        return nb

    def get_profondeur_sujet(self, sujet):
        """Retourne la profondeur du sujet."""
        if sujet.pere is None:
            return 0

        return 1 + self.get_profondeur_sujet(sujet.pere)

    def get_position_sujet(self, sujet):
        """Retourne la position du sujet.

        La position est une chaîne, "0" si le sujet n'a pas de parent,
        sinon un e information de position (comme "1.1.5").

        """
        if sujet.pere is None:
            return ""

        pos = sujet.pere.sujets_fils.index(sujet) + 1
        parent = self.get_position_sujet(sujet.pere)
        if parent:
            return parent + "." + str(pos)

        return str(pos)
