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


"""Ce fichier définit plusieurs fonctions gérant l'affichage des dates."""

import time

def get_date(temps=None):
    """Retourne la date et l'heure sous la forme :
        le mardi 1 janvier 1970 à 00:00:00
    
    Si le paramètre n'est pas précisé, retourne la date et l'heure
    actuelle.
    Sinon, le temps peut être :
        -   un timestamp
        -   une structime
    
    """
    if temps is None:
        temps = time.time()
        struct = time.localtime(temps)
    elif isinstance(temps, float):
        struct = time.localtime(temps)
    elif isinstance(temps, time.struct_time):
        struct = temps
    else:
        raise TypeError("le type {} n'est pas un temps valide".format(
                type(temps)))
    
    semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', \
            'samedi', 'dimanche']
    mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', \
        'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
    
    jour_semaine = semaine[struct.tm_wday]
    mois_courant = mois[struct.tm_mon - 1]
    ret = "le {} {} {} {} à {:02}:{:02}:{:02}".format(
        jour_semaine, struct.tm_mday, mois_courant, struct.tm_year,
        struct.tm_hour, struct.tm_min, struct.tm_sec)
    return ret
