# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 AYDIN Ali-Kémal
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


"""Ce fichier définit le contexte-éditeur EdtResponsables."""

from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import format_nb

class EdtResponsables(Editeur):

    """Contexte-éditeur d'édition des responsables.
    
    """

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("a", self.ajouter_resp)
        self.ajouter_option("s", self.suppr_resp)

    def accueil(self):
        """Message d'accueil du contexte"""
        evenement = self.objet
        msg = "| |tit|" + "Responsables de {}".format(evenement.id).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += format_nb(len(evenement.responsables), \
                "{nb} responsable{s} actuel{s} :\n")
        
        # Parcours des responsables
        responsables = evenement.responsables
        
        for resp in responsables:
            msg += "\n  {}".format(resp.nom)
        
        return msg

    def suppr_resp(self, arguments):
        """Supprime un responsable ; syntaxe : /s <responsable>."""
        evenement = self.objet
        nom_resp = arguments.split(" ")[0].capitalize()
        responsable = None
        for r in evenement.responsables:
            if r.nom == nom_resp:
                responsable = r
                break
        
        if responsable is None:
            self.pere << "|err|Ce responsable n'existe pas.|ff|"
        else:
            evenement.responsables.remove(responsable)
            self.actualiser()

    def ajouter_resp(self, arguments):
        """Ajoute un responsable ; syntaxe : /a <responsable>."""
        evenement = self.objet
        nom_resp = arguments.split(" ")[0].capitalize()
        
        try:
            nouveau_resp = importeur.joueur.joueurs[nom_resp]
        except KeyError:
            self.pere << "|err|Ce joueur n'existe pas.|ff|"
        else :
            if nouveau_resp not in evenement.responsables:
                evenement.responsables.append(nouveau_resp)
                self.actualiser()
            else:
                self.pere << "|err|Ce joueur est déjà responsable.|ff|"
