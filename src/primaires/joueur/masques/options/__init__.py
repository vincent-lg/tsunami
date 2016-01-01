# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le masque <options>."""

import getopt
import shlex

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation


class Options(Masque):
    
    """Masque <options>.
    
    """
    
    nom = "options"
    nom_complet = "options"

    def __init__(self):
        """Constructeur du masque."""
        Masque.__init__(self)
        self.proprietes["options_courtes"] = "''"
        self.proprietes["options_longues"] = "[]"
    
    def init(self):
        """Initialisation des attributs"""
        self.options = {}
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        options = liste_vers_chaine(commande)
        self.a_interpreter = options
        commande[:] = []
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        chn_options = self.a_interpreter
        lst_options = shlex.split(chn_options)
        courtes = self.options_courtes
        courtes_net = courtes.replace(":", "")
        longues = self.options_longues
        longues_net = [o.rstrip("=") for o in longues]
        try:
            opts, args = getopt.getopt(lst_options, courtes, longues)
        except getopt.GetoptError as err:
            print(err, type(err))
            raise ErreurValidation("|err|Options invalides.|ff|")
        else:
            lst_courtes = ["-{}".format(c) for c in list(courtes_net)]
            longues_net = ["--{}".format(l) for l in longues_net]
            for nom, val in opts:
                for o_court, o_long in zip(lst_courtes, longues_net):
                    if nom in (o_court, o_long):
                        self.options[o_long[2:]] = val
            
            return True
