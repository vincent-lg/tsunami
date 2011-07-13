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


"""Package contenant l'éditeur 'messagerie'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.editeur.presentation import Presentation

class EdtMessagerie(Presentation):
    
    """Classe définissant l'éditeur 'messagerie'.
    
    """
    
    nom = "messagerie"
    
    def __init__(self, personnage, objet=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, None)
        if personnage:
            self.construire()
        self.ajouter_option("h", self.opt_help)
    
    def __getnewargs__(self):
        return (None, )
    
    def accueil(self):
        """Message d'accueil du contexte"""
        msg = "| |tit|Messagerie|ff|".ljust(87) + "|\n"
        msg += self.opts.separateur + "\n\n"
        msg += \
            " Bienvenue dans votre messagerie.\n" \
            " Nouveau ? Entrez |cmd|/h <sujet>|ff| pour de l'aide (par " \
            "exemple : |ent|/h brouillons|ff|).\n"
        # Parcours des choix possibles
        for nom, objet in self.choix.items():
            raccourci = self.get_raccourci_depuis_nom(nom)
            # On constitue le nom final
            # Si le nom d'origine est 'description' et le raccourci est 'd',
            # le nom final doit être '[D]escription'
            pos = nom.find(raccourci)
            raccourci = ((pos == 0) and raccourci.capitalize()) or raccourci
            nom_maj = nom.capitalize()
            nom_m = nom_maj[:pos] + "[|cmd|" + raccourci + "|ff|]" + \
                    nom_maj[pos + len(raccourci):]
            msg += "\n " + nom_m
            enveloppe = self.choix[nom]
            apercu = enveloppe.get_apercu()
            if apercu:
                msg += " : " + apercu
        
        return msg
    
    def opt_help(self, arguments):
        """Options /h <sujet>"""
        sujet = supprimer_accents(arguments.lower())
        if sujet == "messages recus":
            self.pere.joueur << "Aide sur les messages reçus."
        else:
            self.pere.joueur << "|err|Aucune aide sur ce sujet.\n" \
                    "Sujets disponibles : messages reçus.|ff|"
    
    def construire(self):
        """Construction de l'éditeur"""
        pass
