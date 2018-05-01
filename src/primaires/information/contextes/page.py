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


"""Fichier contenant le contexte 'page'.

Ce contexte est chargé d'afficher une grande quantité de texte page par page.

"""

from textwrap import wrap

from primaires.interpreteur.contexte import Contexte
from primaires.interpreteur.commande.commande import Commande

class Page(Contexte):
    
    """Contexte affichant de grandes quantités de texte en plusieurs pages.
    
    """
    
    nom = "information:page"
    
    def __init__(self, pere, texte):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.prompt_prf = ""
        self.opts.prompt_clr = ""
        self.texte = texte
        self.curseur = 0
        self.chapitres = []
        self.pages = []
        if texte:
            self.chapitres, self.pages = self.decouper(self.pere.joueur, texte)
    
    def __getnewargs__(self):
        return (None, "")
    
    def get_prompt(self):
        """Retourne le prompt"""
        return "[{}/{}]  (|ent|Entrée|ff| pour continuer / " \
                "[|ent|C|ff|]hapitre |ent|<numéro>|ff| / " \
                "[|ent|Q|ff|]uitter)  ".format(self.curseur + 1,
                len(self.pages)).ljust(111, ">")
    
    def accueil(self):
        """Message d'accueil du contexte"""
        try:
            page = self.pages[self.curseur]
        except IndexError:
            self.fermer()
            return "Arrêt de la lecture."
        else:
            if self.curseur + 1 == len(self.pages):
                self.fermer()
            
            return page
    
    @staticmethod
    def decouper(personnage, texte, nb_lignes=25):
        """Découpe le texte en plusieurs pages retournées comme une liste.
        
        On formatte d'abord l'intégralité du texte :
        *  Formattage des symboles spéciaux (|tab|, |sp|...)
        *  Formattage de chaque paragraphe
        
        """
        paragraphes = []
        for paragraphe in texte.split("\n"):
            paragraphe = Commande.remplacer_mots_cles(personnage, paragraphe)
            paragraphe = paragraphe.replace("|tab|", "   ")
            paragraphe = "\n".join(wrap(paragraphe, 75))
            paragraphes.append(paragraphe)
        
        # Constitution des pages et chapitres
        chapitres = []
        pages = []
        page = ""
        for paragraphe in paragraphes:
            for ligne in paragraphe.split("\n"):
                if page.count("\n") >= nb_lignes - 1:
                    pages.append(page)
                    page = ""
                if ligne.lstrip(" ").lower() == "|sp|":
                    if page != "":
                        page += "\n"
                    page += "\n" * (nb_lignes - page.count("\n") - 1)
                    pages.append(page)
                    chapitres.append(len(pages))
                    page = ""
                    continue
                if page:
                    page += "\n"
                page += ligne
        
        if page:
            pages.append(page)
        return chapitres, pages
    
    def interpreter(self, msg):
        """Méthode d'interprétation du contexte"""
        msg = msg.strip().lower()
        if not msg:
            self.curseur += 1
            self.pere.envoyer(self.accueil())
        elif msg.startswith("c"):
            mots = msg.split(" ")
            if len(mots) < 2:
                self.pere << "|err|Précisez un numéro de chapitre.|ff|"
                return
            try:
                num_chap = int(mots[1])
                assert 0 < num_chap <= len(self.chapitres)
            except (ValueError, AssertionError):
                self.pere << "|err|Précisez un numéro de chapitre valide.|ff|"
            else:
                self.curseur = self.chapitres[num_chap - 1]
                self.pere.envoyer(self.accueil())
        elif msg == "q":
            self.fermer()
            self.pere << "Arrêt de la lecture."
        else:
            self.pere << "|err|Entrée invalide.|ff|"
