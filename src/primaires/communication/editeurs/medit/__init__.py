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


"""Package contenant l'éditeur 'medit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package.

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from .edt_destinataires import EdtDestinataires
from .edt_contenu import EdtContenu
from .edt_envoyer import EdtEnvoyer
from .edt_brouillon import EdtBrouillon
from .edt_annuler import EdtAnnuler

class EdtMedit(Presentation):
    
    """Classe définissant l'éditeur de mail 'medit'.
    
    """
    
    nom = "medit"
    
    def __init__(self, personnage, mail):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, mail)
        if personnage and mail:
            self.construire(mail)
        self.supprimer_choix("quitter la fenêtre")
    
    def __getnewargs__(self):
        return (None, None)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        msg = "| |tit|Rédaction : {}|ff|".format(self.objet.sujet).ljust(87) + \
                "|\n"
        msg += self.opts.separateur + "\n"
        # Parcourt des choix possibles
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
    
    def construire(self, mail):
        """Construction de l'éditeur"""
        # Sujet
        sujet = self.ajouter_choix("sujet", "s", Uniligne, mail, "sujet")
        sujet.parent = self
        sujet.prompt = "Nouveau sujet : "
        sujet.apercu = "{objet.sujet}"
        sujet.aide_courte = \
            "Entrez le |ent|sujet|ff| du message ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n" \
            "Sujet actuel : {objet.sujet}"
        
        # Destinataire
        destinataire = self.ajouter_choix("destinataire(s)", "d", \
                EdtDestinataires, mail)
        destinataire.parent = self
        destinataire.prompt = "Entrez un destinataire : "
        destinataire.apercu = "{objet.nom_dest}"
        destinataire.aide_courte = \
            "Choisissez un |ent|destinataire|ff| pour votre message ; " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n" \
            "Destinataire actuel : {objet.nom_dest}"
        
        # Contenu
        contenu = self.ajouter_choix("contenu", "c", EdtContenu, \
                mail, "contenu")
        contenu.parent = self
        contenu.apercu = "{objet.apercu_contenu}"
        contenu.aide_courte = \
            "| |tit|" + "Contenu du message".ljust(76) + "|ff||\n" + \
            self.opts.separateur
        
        # Envoyer
        envoyer = self.ajouter_choix("envoyer", "e", EdtEnvoyer, mail)
        envoyer.parent = self
        
        # Brouillon
        brouillon = self.ajouter_choix("enregistrer comme brouillon", "b", \
                EdtBrouillon, mail)
        brouillon.parent = self
        
        # Annuler
        annuler = self.ajouter_choix("annuler et quitter la fenêtre", "a", \
                EdtAnnuler, mail)
        annuler.parent = self
