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


"""Ce fichier définit le contexte-éditeur 'Description'."""

from . import Editeur

class Description(Editeur):
    
    """Contexte-éditeur description.
    Ce contexte sert à éditer des descriptions.    
        
    """
    
    nom = "editeur:base:description"
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.opts.echp_sp_cars = False
    
    def accueil(self):
        """Retourne l'aide"""
        description = self.objet
        msg = self.aide_courte.format(objet = self.objet) + "\n"
        msg += "Entrez une |tit|phrase|ff| à ajouter à la description\n" \
                "ou |cmd|/|ff| pour revenir à la fenêtre mère.\n\n" \
                "Symboles :\n" \
                "  |cmd||tab||ff| : symbolise une tabulation\n" \
                "  |cmd||nl||ff| : symbolise un saut de ligne\n"
        
        if len(description.paragraphes) > 0:
            no_ligne = 1
            for paragraphe in description.paragraphes:
                paragraphe = description.wrap_paragraphe(paragraphe,
                        aff_sp_cars=True)
                paragraphe = paragraphe.replace("\n", "\n   ")
                msg += "\n{: 2} {}".format(no_ligne, paragraphe)
                no_ligne += 1
        else:
            msg += "  Aucune description"
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation du contexte"""
        description = self.objet
        msg = msg.strip()
        if msg.startswith("/"):
            msg, reste = msg[1].lower(), msg[3:]
            if msg == "d":
                if reste == "*": # on supprime toute la description
                    description.vider()
                    self.actualiser()
                else:
                    try:
                        no = int(reste) - 1
                        assert no >= 0 and no < len(description.paragraphes)
                    except ValueError:
                        self.pere << "|err|Numéro de ligne invalide.|ff|"
                    except AssertionError:
                        self.pere << "|err|Numéro de ligne inexistant.|ff|"
                    else:
                        description.supprimer_paragraphe(no)
                        self.actualiser()
            else:
                self.pere << "|err|Option invalide.|ff|"
        else:
            description.ajouter_paragraphe(msg)
            self.actualiser()
