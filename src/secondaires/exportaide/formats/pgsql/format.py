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

    def peut_tourner(self):
        return driver

    def config(self):
        """Configure le format."""
        self.cfg = type(importeur).anaconf.get_config("exportaide.pg",
                "exportaide/pgsql/config.cfg", "modele export PG", TEXTE_CFG)

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
        commandes = [commande for commande in commandes if \
                commande.groupe in ("pnj", "joueur")]
        # Sélectionne les commandes déjà créées
        query = self.connexion.prepare("SELECT slug FROM commands")
        crees = list(query())
        crees = [ligne[0] for ligne in crees]
        nb_commandes = 0
        for commande in commandes:
            slug = self.get_slug_commande(commande)
            if slug in crees:
                query = \
                    "UPDATE commands SET french_name=$1, " \
                    "english_name=$2, category=$3, " \
                    "syntax=$4, synopsis=$5, help=$6" \
                    "WHERE slug=$7"
                preparation = self.connexion.prepare(query)
                preparation(commande.nom_francais, commande.nom_anglais,
                        commande.nom_categorie, commande.schema,
                        commande.aide_courte, commande.aide_longue, slug)
            else:
                query = \
                    "INSERT INTO commands (slug, french_name, " \
                    "english_name, category, syntax, synopsis, " \
                    "help) values($1, $2, $3, $4, $5, $6, $7)"
                preparation = self.connexion.prepare(query)
                preparation(slug, commande.nom_francais, commande.nom_anglais,
                        commande.nom_categorie, commande.schema,
                        commande.aide_courte, commande.aide_longue)
                crees.append(slug)
            nb_commandes += 1

        print(nb_commandes, "commandes migrées")

    def get_slug_commande(self, commande):
        """Retourne le slug de la commande."""
        nom = supprimer_accents(commande.nom_francais)
        return nom
