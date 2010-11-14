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


"""Package des différents contextes utiles à la connexion et la création de
compte.

"""

# Contextes de connexion
from primaires.connex.contextes.connexion.afficher_motd import AfficherMOTD
from primaires.connex.contextes.connexion.entrer_nom import EntrerNom

# Contextes de création de compte
from primaires.connex.contextes.creation.nouveau_nom import NouveauNom
from primaires.connex.contextes.creation.ch_encodage import ChangerEncodage
from primaires.connex.contextes.creation.choisir_pass import ChoisirPass
from primaires.connex.contextes.creation.confirmer_pass import ConfirmerPass
from primaires.connex.contextes.creation.entrer_email import EntrerEmail
from primaires.connex.contextes.creation.validation import Validation

liste_contextes = [
    # Contexes de connexion
    AfficherMOTD,
    EntrerNom,
    
    # Contextes de création de compte
    NouveauNom,
    ChangerEncodage,
    ChoisirPass,
    ConfirmerPass,
    EntrerEmail,
    Validation,
]
