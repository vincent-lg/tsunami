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


"""Ce fichier contient l'éditeur EdtDetails, détaillé plus bas."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .edt_detail import EdtDetail
from primaires.format.fonctions import supprimer_accents

class EdtDetails(Editeur):
    
    """Contexte-éditeur des détails d'une salle.
    Ces détails sont observables avec la commande look ; voir ./edt_detail.py
    pour l'édition des details un par un.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("d", self.opt_supprimer_detail)
        self.ajouter_option("s", self.opt_synonymes)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        salle = self.objet
        msg = "| |tit|" + "Edition des détails de {}".format(salle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Détails existants :\n"
        
        # Parcours des détails
        details = salle.details
        liste_details = ""
        for nom, detail in details.iter():
            liste_details += "\n |ent|" + nom + "|ff| "
            if detail.synonymes:
                if len(detail.synonymes) == 1:
                    liste_details += "(synonyme : |ent|"
                else:
                    liste_details += "(synonymes : |ent|"
                liste_details += "|ff|, |ent|".join(detail.synonymes)
                liste_details += "|ff|)"
            liste_details += detail.description.paragraphes_indentes
        if not liste_details:
            liste_details += "\n Aucun détail pour l'instant."
        msg += liste_details
        
        return msg
    
    def opt_supprimer_detail(self, arguments):
        """Supprime le détail passé en paramètre.
        Syntaxe : /d <détail existant>
        
        """
        salle = self.objet
        details = salle.details
        nom = supprimer_accents(arguments)
        
        try:
            del details[nom]
        except KeyError:
            self.pere << "|err|Le détail spécifiée n'existe pas.|ff|"
        else:
            self.actualiser()
    
    def opt_synonymes(self, arguments):
        """Edite les synonymes du détail donnée en premier paramètre :
            - si un synonyme existe, il est détruit
            - sinon, il est créé
        Syntaxe :
            /a <détail existant> / <synonyme 1> (/ <synonyme 2> / ...)
        
        """
        salle = self.objet
        details = salle.details
        a_synonymes = [supprimer_accents(argument) for argument in \
                arguments.split(" / ")]
        nom_detail = a_synonymes[0]
        del a_synonymes[0]
        
        if not details.detail_existe(nom_detail):
            self.pere << \
                "|err|Le détail spécifié n'existe pas.|ff|"
            return
        if not a_synonymes:
            self.pere << \
                "|err|Vous devez préciser au moins un synonyme.|ff|"
            return
        
        detail = details.get_detail(nom_detail)
        for synonyme in a_synonymes:
            if details.detail_existe(synonyme) \
                    and (details.get_detail(synonyme) != detail \
                    or detail.nom == synonyme):
                self.pere << \
                    "|err|Le synonyme '{}' est déjà utilisé.|ff|" \
                            .format(synonyme)
            elif synonyme in detail.synonymes:
                detail.synonymes.remove(synonyme)
                self.actualiser()
            else:
                detail.synonymes.append(supprimer_accents(synonyme))
                self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        salle = self.objet
        details = salle.details
        msg = supprimer_accents(msg)
        
        detail = details.get_detail(msg)
        if detail is None:
            detail = details.ajouter_detail(msg)
        enveloppe = EnveloppeObjet(EdtDetail, detail, "description")
        enveloppe.parent = self
        enveloppe.aide_courte = \
            "Entrez une |cmd|phrase|ff| à ajouter au détail ou |ent|/|ff| " \
            "pour revenir à la\nfenêtre mère.\n" \
            "Symboles :\n" \
            " - |ent||tab||ff| : symbolise une tabulation\n" \
            " - |ent||nl||ff| : symbolise un saut de ligne\n" \
            "Options :\n" \
            " - |ent|/d <numéro>/*|ff| : supprime un paragraphe ou toute la " \
            "description\n" \
            " - |ent|/r <texte 1> / <texte 2>|ff| : remplace " \
            "|cmd|texte 1|ff| par |cmd|texte 2|ff|\n" \
            " - |ent|/n <nouveau nom>|ff| : renomme le détail en " \
            "|ent|nouveau nom|ff|\n" \
            " - |ent|/t <nouveau titre>|ff| : change le titre du détail\n" \
            " - |ent|/s <synonyme 1> (/ <synonyme 2> / ...)|ff| : permet de " \
            "modifier les synonymes" \
            "\n   du détail passé en paramètre. Pour chaque synonyme " \
            "donné à l'option,\n" \
            "   s'il existe, il sera supprimé ; sinon, il sera ajouté à la " \
            "liste.\n\n"
        contexte = enveloppe.construire(self.pere)
        
        self.migrer_contexte(contexte)
