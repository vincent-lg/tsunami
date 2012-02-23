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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur EdtEquipement."""

from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import supprimer_accents

class EdtEquipement(Editeur):
    
    """Contexte-éditeur d'édition de l'équipement du PNJ.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        prototype = self.objet
        msg = "| |tit|" + "Edition de l'équipement de {}".format(
                prototype).ljust(64)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Membres définis :"
        
        # Parcours des pnj
        eq = prototype.equipement
        membres = []
        for membre, objet in eq.items():
            membres.append(membre.ljust(20) + " : " + objet.cle)
        
        if membres:
             msg += "\n\n  " + "\n  ".join(membres)
        else:
            msg += "\n\n  Aucun"
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        prototype = self.objet
        if prototype.squelette is None:
            self.pere << "|err|Ce prototype de PNJ n'a aucun squelette " \
                    "défini.|ff|"
            return
        
        squelette = prototype.squelette
        liste = msg.split(" ")
        if len(liste) < 2:
            self.pere << "|err|Entrez le nom du membre suivi de la " \
                    "clé de l'objet ou 0 pour la supprimer.|ff|"
            return
        
        membre = " ".join(liste[:-1])
        cle = liste[-1]
        if cle == "0":
            nom = supprimer_accents(membre).lower()
            noms = [(supprimer_accents(membre).lower(), membre) for membre in \
                    prototype.equipement]
            noms = dict(noms)
            
            if nom not in noms.keys():
                self.pere << "|err|Le membre {} n'existe pas dans cet " \
                        "équipement.|ff|".format(membre)
            nom = noms[nom]
            del prototype.equipement[nom]
            self.actualiser()
            return
        
        if not squelette.a_membre(membre):
            self.pere << "|err|Le membre {} n'est pas défini " \
                    "dans ce squelette.|ff|".format(membre)
            return
        
        # On cherche l'objet
        try:
            objet = importeur.objet.prototypes[cle.lower()]
        except KeyError:
            self.pere << "|err|L'objet {} est introuvable.|ff|".format(cle)
        else:
            nom = squelette.get_membre(membre).nom
            prototype.equipement[nom] = objet
            self.actualiser()
