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


"""Ce fichier contient l'éditeur EdtBalises, détaillé plus bas."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .edt_balise import EdtBalise
from primaires.format.fonctions import supprimer_accents

class EdtBalises(Editeur):
    
    """Contexte-éditeur des balises d'une salle.
    Ces balises sont observables avec la commande look ; voir ./edt_balise.py
    pour l'édition des balises une par une.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("d", self.opt_supprimer_balise)
        self.ajouter_option("s", self.opt_synonymes)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        salle = self.objet
        msg = "| |tit|" + "Edition des balises de {}".format(salle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Balises existantes :\n"
        
        # Parcours des balises
        balises = salle.balises
        liste_balises = ""
        for nom, balise in balises.iter():
            liste_balises += "\n |ent|" + nom + "|ff| "
            if balise.synonymes:
                if len(balise.synonymes) == 1:
                    liste_balises += "(synonyme : |ent|"
                else:
                    liste_balises += "(synonymes : |ent|"
                liste_balises += "|ff|, |ent|".join(balise.synonymes)
                liste_balises += "|ff|)"
            liste_balises += balise.description.paragraphes_indentes
        if not liste_balises:
            liste_balises += "\n Aucune balise pour l'instant."
        msg += liste_balises
        
        return msg
    
    def opt_supprimer_balise(self, arguments):
        """Supprime la balise passée en paramètre.
        Syntaxe : /d <balise existante>
        
        """
        salle = self.objet
        balises = salle.balises
        nom = supprimer_accents(arguments)
        
        try:
            del balises[nom]
        except KeyError:
            self.pere << "|err|La balise spécifiée n'existe pas.|ff|"
        else:
            self.actualiser()
    
    def opt_synonymes(self, arguments):
        """Edite les synonymes de la balise donnée en premier paramètre :
            - si un synonyme existe, il est détruit
            - sinon, il est créé
        Syntaxe :
            /a <balise existante> / <synonyme 1> (/ <synonyme 2> / ...)
        
        """
        salle = self.objet
        balises = salle.balises
        a_synonymes = []
        a_synonymes = arguments.split(" / ")
        nom_balise = a_synonymes[0]
        del a_synonymes[0]
        
        if not balises.balise_existe(nom_balise):
            self.pere << \
                "|err|La balise spécifiée n'existe pas.|ff|"
            return
        if not a_synonymes:
            self.pere << \
                "|err|Vous devez préciser au moins un synonyme.|ff|"
            return
        
        balise = balises.get_balise(nom_balise)
        for synonyme in a_synonymes:
            if balises.balise_existe(synonyme) \
            and (balises.get_balise(synonyme) != balise \
            or balise.nom == synonyme):
                self.pere << \
                    "|err|Le synonyme '{}' est déjà utilisé.|ff|" \
                            .format(synonyme)
            elif synonyme in balise.synonymes:
                balise.synonymes.remove(synonyme)
                self.actualiser()
            else:
                balise.synonymes.append(supprimer_accents(synonyme))
                self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        salle = self.objet
        balises = salle.balises
        msg = supprimer_accents(msg)
        
        balise = balises.get_balise(msg)
        if balise is None:
            balise = balises.ajouter_balise(msg)
        enveloppe = EnveloppeObjet(EdtBalise, balise, "description")
        enveloppe.parent = self
        enveloppe.aide_courte = \
            "Entrez une |cmd|phrase|ff| à ajouter à la balise ou |ent|/|ff| " \
            "pour revenir à la\nfenêtre mère.\n" \
            "Symboles :\n" \
            " - |ent||tab||ff| : symbolise une tabulation\n" \
            " - |ent||nl||ff| : symbolise un saut de ligne\n" \
            "Options :\n" \
            " - |ent|/d <numéro>/*|ff| : supprime un paragraphe ou toute la " \
            "description\n" \
            " - |ent|/r <texte 1> / <texte 2>|ff| : remplace " \
            "|cmd|texte 1|ff| par |cmd|texte 2|ff|\n" \
            " - |ent|/n <nouveau nom>|ff| : renomme la balise en " \
            "|ent|nouveau nom|ff|\n" \
            " - |ent|/s <synonyme 1> (/ <synonyme 2> / ...)|ff| : permet de " \
            "modifier les synonymes" \
            "\n   de la balise passée en paramètre. Pour chaque synonyme " \
            "donné à l'option,\n" \
            "   s'il existe, il sera supprimé ; sinon, il sera ajouté à la " \
            "liste.\n\n"
        contexte = enveloppe.construire(self.pere)
        
        self.migrer_contexte(contexte)
