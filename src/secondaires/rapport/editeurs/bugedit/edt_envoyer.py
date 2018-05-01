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


"""Fichier contenant le contexte éditeur EdtEnvoyer."""

from primaires.interpreteur.editeur import Editeur

class EdtEnvoyer(Editeur):
    
    """Classe définissant le contexte éditeur 'envoyer'.
    
    Ce contexte permet d'envoyer un rapport de bug si il est complété.
    
    """
    
    def entrer(self):
        """En entrant dans l'éditeur."""
        rapport = self.objet
        if not rapport.est_complete():
            champs = rapport.get_champs_a_completer()
            s = ""
            if len(champs) > 1:
                str_champs = "'" + "', '".join(champs[:-1]) + "'"
                str_champs += " et '" + champs[-1] + "'"
                s = "s"
            else:
                str_champs = "'" + champs[0] + "'"
            
            self.pere.joueur << "|err|Ce rapport n'est pas proprement " \
                    "complété.\nVous devez encore remplir le{s} champ{s} " \
                    "{champs}.|ff|\n".format(s=s, champs=str_champs)
            self.migrer_contexte(self.opts.rci_ctx_prec)
        else:
            importeur.rapport.ajouter_rapport(rapport)
            self.fermer()
            self.pere.joueur << "|att|Le rapport #{} a bien été " \
                    "envoyé.|ff|".format(rapport.id)
