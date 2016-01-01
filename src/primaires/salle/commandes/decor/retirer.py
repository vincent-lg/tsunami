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


"""Package contenant le paramètre 'retirer' de la commande 'décor'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRetirer(Parametre):
    
    """Commande 'décor retirer'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "retirer", "remove")
        self.schema = "<cle>"
        self.aide_courte = "retire un décor"
        self.aide_longue = \
            "Cette commande permet de retirer un ou plusieurs décors " \
            "dans la salle où vous vous trouvez. Vous devez préciser " \
            "la clé du prototype de décor. Si plusieurs décors de " \
            "ce prototype sont dans la salle, ils seront tous retirés."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cle = dic_masques["cle"].cle
        try:
            decor = importeur.salle.decors[cle]
        except KeyError:
            personnage << "|err|Ce décor {} est inconnu.|ff|".format(cle)
        else:
            nb_avt = len(personnage.salle.decors)
            personnage.salle.supprimer_decors(decor.cle)
            nb_apr = len(personnage.salle.decors)
            nb = nb_avt - nb_apr
            if nb == 0:
                personnage << "|err|aucun décor n'a été retiré.|ff|"
            else:
                personnage << "{} décor(s) retiré(s).".format(nb)
