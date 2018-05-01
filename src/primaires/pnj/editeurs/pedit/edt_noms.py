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


"""Fichier contenant le contexte éditeur EdtNoms"""

from primaires.interpreteur.editeur import Editeur

class EdtNoms(Editeur):
    
    """Classe définissant le contexte éditeur 'noms'.
    Ce contexte permet d'éditer les noms et états d'un prototype de pnj.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.opts.echp_sp_cars = False
        self.ajouter_option("n", self.opt_nom_singulier)
        self.ajouter_option("e", self.opt_etat_singulier)
        self.ajouter_option("s", self.opt_nom_pluriel)
        self.ajouter_option("p", self.opt_etat_pluriel)
        self.ajouter_option("a", self.opt_ajouter_nom_sup)
        self.ajouter_option("d", self.opt_supprimer_nom_sup)
    
    def accueil(self):
        """Message d'accueil"""
        prototype = self.objet
        ret = "Options :\n"
        ret += " - |cmd|/n <nom singulier avec déterminant>|ff| : |bc|"
        ret += prototype.nom_singulier + "|ff|\n"
        ret += " - |cmd|/s <nom pluriel sans déterminant>|ff|   : |bc|"
        ret += prototype.nom_pluriel + "|ff|\n"
        ret += " - |cmd|/e <état singulier>|ff| : |bc|"
        ret += prototype.etat_singulier + "|ff|\n"
        ret += " - |cmd|/p <état pluriel>|ff|   : |bc|"
        ret += prototype.etat_pluriel + "|ff|\n"
        ret += " - |cmd|/a <nombre> / <nom pluriel> / "
        ret += "<état pluriel>|ff| (ajoute un nom pluriel)\n"
        ret += " - |cmd|/d <nombre>|ff| (supprime le nom correspondant au "
        ret += "nombre)"
        if prototype.noms_sup:
            ret += "\n\nNoms pluriels supplémentaires :"
            for nom in prototype.noms_sup:
                ret += "\n  |bc|" + str(nom[0]) + "|ff| - " + nom[1] + " "
                ret += nom[2]
        return ret
    
    def opt_nom_singulier(self, arguments):
        """Change le nom singulier du prototype"""
        self.objet.nom_singulier = arguments
        self.actualiser()
    
    def opt_etat_singulier(self, arguments):
        """Change l'état singulier du prototype"""
        self.objet.etat_singulier = arguments
        self.actualiser()
    
    def opt_nom_pluriel(self, arguments):
        """Change le nom pluriel du prototype"""
        self.objet.nom_pluriel = arguments
        self.actualiser()
    
    def opt_etat_pluriel(self, arguments):
        """Change l'état pluriel du prototype"""
        self.objet.etat_pluriel = arguments
        self.actualiser()
    
    def opt_ajouter_nom_sup(self, arguments):
        """Ajoute un nom pluriel supplémentaire"""
        prototype = self.objet
        if not arguments:
            self.pere << "|err|Vous devez préciser un nombre, un nom et un " \
                    "état pluriel.|ff|"
            return
        try:
            nombre = arguments.split(" / ")[0]
            nom = arguments.split(" / ")[1]
            etat = arguments.split(" / ")[2]
        except IndexError:
            self.pere << "|err|Vous devez préciser un nombre, un nom et un " \
                    "état pluriel.|ff|"
        else:
            try:
                nombre = int(nombre)
                assert nombre > 1
            except (ValueError, AssertionError):
                self.pere << "|err|Vous devez préciser un nombre valide, " \
                        "supérieur à 1.|ff|"
            else:
                if nombre in [nom[0] for nom in prototype.noms_sup]:
                    for nom_sup in prototype.noms_sup:
                        if nom_sup[0] == nombre:
                            nom_sup[1] = nom
                            nom_sup[2] = etat
                            break
                else:
                    i = 0
                    for nom_sup in prototype.noms_sup:
                        if nom_sup[0] > nombre:
                            break
                        i += 1
                    prototype.noms_sup.insert(i, [nombre, nom, etat])
                self.actualiser()
    
    def opt_supprimer_nom_sup(self, arguments):
        """Supprime un nom pluriel supplémentaire"""
        prototype = self.objet
        if not arguments:
            self.pere << "|err|Vous devez préciser un nombre.|ff|"
            return
        try:
            nombre = int(arguments.split(" ")[0])
            assert nombre in [nom[0] for nom in prototype.noms_sup]
        except (ValueError, AssertionError):
            self.pere << "|err|Vous devez préciser un nombre valide " \
                    "correspondant à un nom pluriel déjà défini.|ff|"
        else:
            i = 0
            for nom in prototype.noms_sup:
                if nom[0] == nombre:
                    break
                i += 1
            del prototype.noms_sup[i]
            self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation du message"""
        self.pere << "|err|Option invalide.|ff|"
