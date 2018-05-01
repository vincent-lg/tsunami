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


"""Package contenant la commande 'scripting alerte info'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.format.fonctions import echapper_accolades
from primaires.format.date import get_date

class PrmInfo(Parametre):
    
    """Commande 'scripting alerte info'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "info", "info")
        self.schema = "<nombre>"
        self.aide_courte = "affiche des informations sur l'alerte"
        self.aide_longue = \
            "Affiche des informations sur l'alerte permettant de la corriger."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        nombre = dic_masques["nombre"].nombre
        try:
            alerte = type(self).importeur.scripting.alertes[nombre]
        except KeyError:
            personnage << "|err|Ce numéro d'alerte est invalide.|ff|"
        else:
            msg = "Informations sur l'alerte {} :".format(alerte.no)
            msg += "\n  S'est produit sur {} {}".format(alerte.type,
                    alerte.objet) + " " + get_date(alerte.date.timetuple())
            msg += "\n  Evenement {}, test {}, ligne {}".format(
                    alerte.evenement, echapper_accolades(alerte.test),
                    alerte.no_ligne)
            msg += "\n      {}\n".format(echapper_accolades(alerte.ligne))
            msg += "\n  Message d'erreur : |err|{}|ff|".format(
                    echapper_accolades(alerte.message))
            if personnage.nom_groupe == "administrateur":
                msg += "\n  Traceback Python :\n  {}".format(
                        echapper_accolades(alerte.traceback))
            
            personnage << msg
