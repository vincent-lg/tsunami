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


"""Ce fichier contient l'éditeur EdtBalise, détaillé plus bas."""

from primaires.interpreteur.editeur.description import Description
from primaires.format.fonctions import supprimer_accents

class EdtBalise(Description):
    
    """Ce contexte permet d'éditer une balise observable d'une salle.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Description.__init__(self, pere, objet, attribut)
        self.ajouter_option("n", self.opt_renommer_balise)
        self.ajouter_option("s", self.opt_synonymes)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        balise = self.objet
        description = self.description
        salle = balise.parent
        msg = "| |tit|"
        msg += "Edition de la balise {} de {}".format(balise, salle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Nom : " + balise.nom + "\n"
        if balise.synonymes:
            msg += "Synonymes : " + ", ".join(balise.synonymes) + "\n"
        msg += "Description existante :\n"
        
        # Aperçu de la description existante
        if len(description.paragraphes) > 0:
            no_ligne = 1
            for paragraphe in description.paragraphes:
                paragraphe = description.wrap_paragraphe(paragraphe,
                        aff_sp_cars=True)
                paragraphe = paragraphe.replace("\n", "\n   ")
                msg += "\n{: 2} {}".format(no_ligne, paragraphe)
                no_ligne += 1
        else:
            msg += "\n Aucune description."
        
        return msg
    
    def opt_renommer_balise(self, arguments):
        """Renomme la balise courante.
        Syntaxe : /r <nouveau nom>
        
        """
        balise = self.objet
        salle = balise.parent
        nouveau_nom = arguments
        
        if not nouveau_nom:
            self.pere << \
                "|err|Vous devez indiquer un nouveau nom.|ff|"
            return
        if nouveau_nom == balise.nom:
            self.pere << \
                "|err|'{}' est déjà le nom de la balise courante.|ff|" \
                        .format(nouveau_nom)
            return
        if nouveau_nom in balise.synonymes:
            self.pere << \
                "|err|'{}' est déjà un synonyme de cette balise.|ff|" \
                        .format(nouveau_nom)
            return
        if salle.balises.balise_existe(nouveau_nom):
            self.pere << \
                "|err|Ce nom est déjà utilisé.|ff|"
            return
        
        salle.balises.ajouter_balise(nouveau_nom, modele=balise)
        del salle.balises[balise.nom]
        self.objet = salle.balises[nouveau_nom]
        self.actualiser()
    
    def opt_synonymes(self, arguments):
        """Ajoute ou supprime les synonymes passés en paramètres.
        syntaxe : /s <synonyme 1> (/ <synonyme 2> / ...)
        
        """
        balise = self.objet
        salle = balise.parent
        a_synonymes = []
        a_synonymes = arguments.split(" / ")
        
        if not a_synonymes:
            self.pere << \
                "|err|Vous devez préciser au moins un synonyme.|ff|"
            return
        
        for synonyme in a_synonymes:
            if balise.nom == synonyme \
            or (salle.balises.balise_existe(synonyme) \
            and salle.balises.get_balise(synonyme) != balise):
                self.pere << \
                    "|err|Le synonyme '{}' est déjà utilisé.|ff|" \
                            .format(synonyme)
            elif not synonyme:
                self.pere << \
                    "|err|C'est vide...|ff|"
            elif synonyme in balise.synonymes:
                balise.synonymes.remove(synonyme)
                self.actualiser()
            else:
                balise.synonymes.append(supprimer_accents(synonyme))
                self.actualiser()
