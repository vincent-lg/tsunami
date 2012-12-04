# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce fichier contient l'éditeur EdtEtat, étatlé plus bas."""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne

class EdtEtat(Presentation):
    
    """Ce contexte permet d'éditer un état de prototype de bonhomme de neige.
    
    """
    
    def __init__(self, pere, etat=None, attribut=None):
        """Constructeur de l'éditeur"""
        Presentation.__init__(self, pere, etat, attribut, False)
        if pere and etat:
            self.construire(etat)
    
    def opt_renommer_etat(self, arguments):
        """Renomme le état courant.
        Syntaxe : /n <nouveau nom>
        
        """
        etat = self.objet
        salle = etat.parent
        nouveau_nom = supprimer_accents(arguments)
        
        if not nouveau_nom:
            self.pere << \
                "|err|Vous devez indiquer un nouveau nom.|ff|"
            return
        if nouveau_nom == etat.nom:
            self.pere << \
                "|err|'{}' est déjà le nom du état courante.|ff|".format(
                        nouveau_nom)
            return
        if nouveau_nom in etat.synonymes:
            self.pere << \
                "|err|'{}' est déjà un synonyme de ce état.|ff|".format(
                        nouveau_nom)
            return
        if salle.etats.etat_existe(nouveau_nom):
            self.pere << \
                "|err|Ce nom est déjà utilisé.|ff|"
            return
        
        salle.etats.ajouter_etat(nouveau_nom, modele=etat)
        del salle.etats[etat.nom]
        self.objet = salle.etats[nouveau_nom]
        self.actualiser()
    
    def opt_synonymes(self, arguments):
        """Ajoute ou supprime les synonymes passés en paramètres.
        syntaxe : /s <synonyme 1> (/ <synonyme 2> / ...)
        
        """
        etat = self.objet
        salle = etat.parent
        a_synonymes = [supprimer_accents(argument) for argument in \
                arguments.split(" / ")]
        
        if not a_synonymes:
            self.pere << \
                "|err|Vous devez préciser au moins un synonyme.|ff|"
            return
        
        for synonyme in a_synonymes:
            if etat.nom == synonyme \
                    or (salle.etats.etat_existe(synonyme) \
                    and salle.etats.get_etat(synonyme) != etat):
                self.pere << \
                    "|err|Le synonyme '{}' est déjà utilisé.|ff|" \
                            .format(synonyme)
            elif not synonyme:
                self.pere << \
                    "|err|C'est vide...|ff|"
            elif synonyme in etat.synonymes:
                etat.synonymes.remove(synonyme)
                self.actualiser()
            else:
                etat.synonymes.append(synonyme)
                self.actualiser()
    
    def construire(self, etat):
        """Construction de l'éditeur"""
        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, etat, "titre")
        titre.parent = self
        titre.prompt = "Titre du état : "
        titre.apercu = "{objet.titre}"
        titre.aide_courte = \
            "Entrez le |ent|titre|ff| du état ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nTitre actuel : |bc|{objet.titre}|ff|"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                etat)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description du état {}".format(etat).ljust(76) + \
            "|ff||\n" + self.opts.separateur
        
        # Est visible
        visible = self.ajouter_choix("est visible", "v", Flag, etat,
                "est_visible")
        visible.parent = self
        
        # Repos
        repos = self.ajouter_choix("repos", "r", EdtRepos, etat)
        repos.parent = self
        repos.apercu = "{objet.repos}"
        repos.aide_courte = \
            "Paramétrez ici le repos possible sur ce état.\nOptions :\n" \
            " - |ent|/s <nombre de places> (<facteur>)|ff| : permet de " \
            "modifier le repos assis.\n" \
            "   Le deuxième nombre correspond au facteur de récupération " \
            "(optionnel).\n" \
            "   Si vous précisez |ent|0|ff| en nombre de places, le repos " \
            "assis sera désactivé.\n" \
            " - |ent|/l <nombre de places> (<facteur>)|ff| : permet de " \
            "modifier le repos allongé de\n" \
            "   la même manière\n" \
            " - |ent|/c <connecteur>|ff| : spécifie le connecteur de ce état. " \
            "Le connecteur fait\n" \
            "   la liaison entre l'action et le titre du état. Par " \
            "exemple : \"Vous vous\n" \
            "   allongez |vr|sur|ff| une table.|ff|\"\n\n"
        
        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                etat.script)
        scripts.parent = self
