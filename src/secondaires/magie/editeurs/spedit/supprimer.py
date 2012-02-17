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


"""Fichier contenant le contexte éditeur Supprimer"""

from primaires.interpreteur.editeur.supprimer import Supprimer

class NSupprimer(Supprimer):
    
    """Classe définissant le contexte éditeur 'supprimer'.
    Ce contexte permet spécifiquement de supprimer un prototype d'objet.
    
    """
    
    def interpreter(self, msg):
        """Interprétation du contexte"""
        msg = msg.lower()
        sort = self.objet
        if msg == "oui":
            objet = type(self).importeur
            for nom in self.action.split("."):
                objet = getattr(objet, nom)
            
            nb_persos = 0
            for perso in type(self).importeur.connex.joueurs:
                if sort.cle in perso.sorts and perso.sorts[sort.cle] > 0:
                    nb_persos += 1
            if nb_persos > 0:
                s = nb_persos > 1 and "s" or ""
                i = nb_persos > 1 and "issen" or "î"
                self.pere << "|err|{} personnage{s} conna{i}t ce sort. " \
                        "Opération annulée.|ff|".format(nb_persos, s=s, i=i)
                self.migrer_contexte(self.opts.rci_ctx_prec)
            else:
                objet(sort.cle)
                self.fermer()
                self.pere << self.confirme
        elif msg == "non":
            self.migrer_contexte(self.opts.rci_ctx_prec)
        else:
            self.pere << "|err|Choix invalide.|ff|"
