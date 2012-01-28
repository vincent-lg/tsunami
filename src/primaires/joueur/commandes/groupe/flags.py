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


"""Fichier contenant le paramètre 'flags' de la commande 'groupe'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.interpreteur.groupe.groupe import FLAGS

class PrmFlags(Parametre):
    
    """Commande 'groupe flags'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "flags", "flags")
        self.schema = "<groupe_existant> <flags_groupes>"
        self.aide_courte = "modifie les flags du groupe"
        self.aide_longue = \
            "Cette commande permet de modifier les flags du groupe. " \
            "Vous devez préciser en paramètre un ou plusieurs flags " \
            "séparés par des espaces. Si le flag est présent sur " \
            "le groupe, il sera désactivé. Si il ne l'est pas " \
            "au contraire, il sera activé. Les flags existants sont : " \
            "{}.".format(",  ".join(FLAGS.keys()))
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        nom_groupe = dic_masques["groupe_existant"].nom_groupe
        groupe = type(self).importeur.interpreteur.groupes[nom_groupe]
        flags = dic_masques["flags_groupes"].flags
        for nom in flags:
            groupe.flags = groupe.flags ^ FLAGS[nom]
        
        personnage << "Les flags du groupe ont bien été mis à jour."
