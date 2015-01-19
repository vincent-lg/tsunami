# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Package contenant les éditeurs qedit (éditeurs de quête).

Ce fichier en particulier contient l'éditeur racine de qedit.

"""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .presentation import EdtPresentation
from primaires.format.fonctions import supprimer_accents, contient
from primaires.scripting.quete.quete import Quete, RE_QUETE_VALIDE

class EdtQedit(Editeur):

    """Classe définissant l'éditeur de quête 'qedit'.

    """

    nom = "qedit"

    def __init__(self, personnage, objet=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Editeur.__init__(self, instance_connexion, objet)
        self.personnage = personnage

        # Options
        self.ajouter_option("d", self.opt_supprimer_quete)

    def __getnewargs__(self):
        return (None, None)

    def opt_supprimer_quete(self, arguments):
        """Supprime une quête.

        Syntaxe :
            /d <cle_de_quête>

        """
        cle = arguments.lower()
        if cle in importeur.scripting.quetes:
            quete = importeur.scripting.quetes[cle]
            if len(quete.etapes) > 1:
                self.pere << "|err|Cette quête a des étapes enregistrées. " \
                        "Opération annulée.|ff|"
                return

            quete.detruire()
            del importeur.scripting.quetes[cle]
            self.actualiser()
        else:
            self.pere << "|err|Cette quête n'existe pas.|ff|"

    def accueil(self):
        """Message d'accueil de l'éditeur.

        On affiche les quêtes existantes.

        """
        quetes = type(self).importeur.scripting.quetes.values()
        liste_quetes = [str(q) for q in quetes]
        liste_quetes.sort()
        msg = "| |tit|" + "Editeur de quêtes".ljust(76) + "|ff||\n" + \
                self.opts.separateur + "\n"
        msg += "Ci-dessous se trouve la liste des quêtes existantes. " \
                "Entrez simplement\n" \
                "la |ent|clé|ff| d'une quête pour l'éditer, ou une " \
                "nouvelle pour la créer.\n" \
                "Tapez |cmd|q|ff| pour quitter cet éditeur.\n\n"
        if not liste_quetes:
            msg += "|att|Aucune quête en jeu pour le moment.|ff|"
        else:
            str_quetes = "\n  ".join(liste_quetes)
            msg += "Quêtes disponibles :\n  " + str_quetes
        return msg

    def interpreter(self, msg):
        """Interprétation du message"""
        msg = msg.lower()
        if msg == "q":
            self.fermer()
            self.pere.envoyer("Fermeture de l'éditeur de quêtes.")
        else:
            if msg in type(self).importeur.scripting.quetes.keys():
                quete = type(self).importeur.scripting.quetes[msg]
            elif RE_QUETE_VALIDE.search(msg) is None:
                self.pere << "|err|Cette clé de quête est invalide.|ff|"
                return
            else:
                quete = Quete(msg, self.personnage)
                type(self).importeur.scripting.quetes[msg] = quete

            enveloppe = EnveloppeObjet(EdtPresentation, quete, "")
            enveloppe.parent = self
            contexte = enveloppe.construire(self.personnage)

            self.migrer_contexte(contexte)
