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


"""Fichier contenant le contexte éditeur EdtStatuts."""

from primaires.interpreteur.editeur import Editeur

class EdtStatuts(Editeur):
    
    """Classe définissant le contexte éditeur 'statuts'.
    Ce contexte permet d'éditer les statuts de remplissage d'un conteneur
    de nourriture.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("d", self.opt_supprimer_statut)
    
    def accueil(self):
        """Message d'accueil"""
        conteneur = self.objet
        ret = "| |tit|"
        ret += "Edition des statuts de remplissage de {}".format(
                conteneur).ljust(76)
        ret += "|ff||\n" + self.opts.separateur + "\n"
        ret += self.aide_courte
        ret += "\nStatuts actuels :\n"
        for ratio, message in conteneur.statuts:
            ret += "\n  |vr|{:>2}|ff| : |bc|{}|ff|".format(ratio, message)
        return ret
    
    def opt_supprimer_statut(self, arguments):
        """Supprime un statut en prenant le ratio en argument"""
        prototype = self.objet
        if not arguments:
            self.pere << "|err|Vous devez préciser un nombre.|ff|"
            return
        if len(prototype.statuts) <= 1:
            self.pere << "|err|La liste de statuts ne peut être vide.|ff|"
            return
        try:
            nombre = int(arguments.split(" ")[0])
            assert nombre in [ligne[0] for ligne in prototype.statuts]
        except (ValueError, AssertionError):
            self.pere << "|err|Vous devez préciser un nombre valide faisant " \
                    "partie de la liste.|ff|"
        else:
            if nombre == 10:
                self.perre << "|err|Le statut 10 doit être précisé.|ff|"
                return
            i = 0
            for ratio, message in list(prototype.statuts):
                if ratio == nombre:
                    del prototype.statuts[i]
                i += 1
            self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation du message"""
        prototype = self.objet
        if not msg:
            self.pere << "|err|Vous devez préciser un nombre et un " \
                    "message.|ff|"
            return
        try:
            msg = msg.split(" ")
            nombre, message = msg[0], " ".join(msg[1:])
            nombre = int(nombre)
            assert 1 <= nombre <= 10
        except (ValueError, AssertionError):
            self.pere << "|err|Vous devez préciser un nombre et un message " \
                    "valides (nombre entre 1 et 10).|ff|"
        else:
            if nombre in [ligne[0] for ligne in prototype.statuts]:
                i = 0
                for ratio, statut in prototype.statuts:
                    if ratio == nombre:
                        break
                    i += 1
                del prototype.statuts[i]
            prototype.statuts.append((nombre, message))
            prototype.statuts = sorted(prototype.statuts,
                    key=lambda ligne: ligne[0])
            self.actualiser()
