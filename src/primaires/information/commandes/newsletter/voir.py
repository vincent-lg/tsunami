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
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'voir' de la commande 'newsletter'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmVoir(Parametre):
    
    """Commande 'newsletter voir'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "voir", "view")
        self.schema = "<nombre>"
        self.aide_courte = "affiche le détail d'une news letter"
        self.aide_longue = \
            "Cette commande permet d'afficher le détail d'une news letter " \
            "(si elle est envyée, la date d'envoi est affichée)."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        id = dic_masques["nombre"].nombre
        try:
            newsletter = importeur.information.newsletters[id - 1]
        except IndexError:
            personnage << "|err|Cette news letter n'existe pas.|ff|"
        else:
            msg = "Newsletter numéro {} : {}\n".format(id, newsletter.sujet)
            msg += "Créée le : {}     Statut : {}\n".format(
                    newsletter.date_creation.date(), newsletter.statut)
            if newsletter.envoyee:
                msg += "Envoyée le : {}   Nombre d'envois : {}\n".format(
                        newsletter.date_envoi.date(), newsletter.nombre_envois)
            
            msg += "-" * 79 + "\n"
            msg += str(newsletter.contenu)
            personnage << msg
