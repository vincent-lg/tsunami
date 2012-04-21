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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier contient l'éditeur EdtDetail, détaillé plus bas."""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne

class EdtDetail(Presentation):
    
    """Ce contexte permet d'éditer un detail observable d'une salle.
    
    """
    
    def __init__(self, pere, detail=None, attribut=None):
        """Constructeur de l'éditeur"""
        Presentation.__init__(self, pere, detail, attribut, False)
        if pere and detail:
            self.construire(detail)
    
    def opt_renommer_detail(self, arguments):
        """Renomme le détail courant.
        Syntaxe : /n <nouveau nom>
        
        """
        detail = self.objet
        salle = detail.parent
        nouveau_nom = supprimer_accents(arguments)
        
        if not nouveau_nom:
            self.pere << \
                "|err|Vous devez indiquer un nouveau nom.|ff|"
            return
        if nouveau_nom == detail.nom:
            self.pere << \
                "|err|'{}' est déjà le nom du détail courante.|ff|".format(
                        nouveau_nom)
            return
        if nouveau_nom in detail.synonymes:
            self.pere << \
                "|err|'{}' est déjà un synonyme de ce détail.|ff|".format(
                        nouveau_nom)
            return
        if salle.details.detail_existe(nouveau_nom):
            self.pere << \
                "|err|Ce nom est déjà utilisé.|ff|"
            return
        
        salle.details.ajouter_detail(nouveau_nom, modele=detail)
        del salle.details[detail.nom]
        self.objet = salle.details[nouveau_nom]
        self.actualiser()
    
    def opt_synonymes(self, arguments):
        """Ajoute ou supprime les synonymes passés en paramètres.
        syntaxe : /s <synonyme 1> (/ <synonyme 2> / ...)
        
        """
        detail = self.objet
        salle = detail.parent
        a_synonymes = [supprimer_accents(argument) for argument in \
                arguments.split(" / ")]
        
        if not a_synonymes:
            self.pere << \
                "|err|Vous devez préciser au moins un synonyme.|ff|"
            return
        
        for synonyme in a_synonymes:
            if detail.nom == synonyme \
                    or (salle.details.detail_existe(synonyme) \
                    and salle.details.get_detail(synonyme) != detail):
                self.pere << \
                    "|err|Le synonyme '{}' est déjà utilisé.|ff|" \
                            .format(synonyme)
            elif not synonyme:
                self.pere << \
                    "|err|C'est vide...|ff|"
            elif synonyme in detail.synonymes:
                detail.synonymes.remove(synonyme)
                self.actualiser()
            else:
                detail.synonymes.append(synonyme)
                self.actualiser()
    
    def construire(self, detail):
        """Construction de l'éditeur"""
        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, detail, "titre")
        titre.parent = self
        titre.prompt = "Titre du détail : "
        titre.apercu = "{objet.titre}"
        titre.aide_courte = \
            "Entrez le |ent|titre|ff| du détail ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nTitre actuel : |bc|{objet.titre}|ff|"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                detail)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description du détail {}".format(detail).ljust(76) + \
            "|ff||\n" + self.opts.separateur
