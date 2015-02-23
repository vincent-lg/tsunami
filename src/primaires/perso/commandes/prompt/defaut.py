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


"""Fichier contenant le paramètre dynamique de la commande 'prompt'."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.parametre import Parametre

# Constantes
AIDE = """
            Utilisez cette commande pour consulter ou modifier
            votre {courte}.
            {longue}.
            Utilisez %prompt% %prompt:{nom}% sans argument pour
            consulter votre {courte} actuel. Vous pouvez aussi :
                Masquer le prompt avec %prompt% %prompt:{nom}%|ent| caché|ff|
                Réinitialiser le prompt avec %prompt% %prompt:{nom}%|ent| init|ff|
            Ou encore %prompt% %prompt:{nom}% suivi du nouveau prompt
            pour le modifier.
""".strip()

class PrmDefaut(Parametre):

    """Commande dynamique de 'prompt'.

    Ce n'est pas un paramètre ordinaire car il est créé dynamiquement
    au moment de l'ajout de la commande. Voir la méthode
    'ajouter_commandes'.

    """

    def __init__(self, prompt):
        """Constructeur du paramètre"""
        Parametre.__init__(self, prompt.nom, prompt.nom_anglais)
        self.prompt = prompt
        self.schema = "(<prompt>)"
        self.aide_courte = prompt.aide_courte.capitalize()
        self.aide_longue = AIDE.format(nom=prompt.nom,
                courte=prompt.aide_courte, longue=prompt.aide_longue)
        if prompt.symboles_sup:
            self.aide_longue += "\n            Symboles " \
                    "supplémentaires :\n" + prompt.symboles_sup.replace(
                    "%", "|pc|")

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        prompt = dic_masques["prompt"] or None
        if prompt:
            prompt = prompt.prompt
            if supprimer_accents(prompt).lower() in ("cache", "cacher"):
                personnage.prompts[self.prompt.nom] = ""
                personnage << "Votre {} a bien été masqué.".format(
                        self.prompt.aide_courte)
                return
            if supprimer_accents(prompt).lower() == "init":
                if self.prompt.nom in personnage.prompts:
                    del personnage.prompts[self.prompt.nom]

                personnage << "Votre {} a bien été réinitialisé.".format(
                        self.prompt.aide_courte)
                return

            prompt = prompt.replace("{", "{{")
            prompt = prompt.replace("}", "}}")
            for symbole, repl in sorted(tuple(self.prompt.symboles.items()),
                    key=lambda c: len(c[0]), reverse=True):
                prompt = prompt.replace("%{}".format(symbole), "{" + \
                        repl + "}")
            personnage.prompts[self.prompt.nom] = prompt
            personnage << "Votre {} a bien été modifié.".format(
                    self.prompt.aide_courte)

        prompt = personnage.prompts.get(self.prompt.nom,
                self.prompt.defaut)
        for symbole, repl in self.prompt.symboles.items():
            prompt = prompt.replace("{" + repl + "}", "%" + symbole)

        prompt = prompt.replace("{", "{{").replace("}", "}}")
        personnage << self.prompt.aide_courte.capitalize() + " actuel : " + \
                prompt
