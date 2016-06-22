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


"""Ce fichier contient le convertisseur binaire->MongoDB.

La configuration de 'supenr' doiit être réglée sur 'pickle'. Après
le chargement de la sauvegarde, on force l'enregistrement en MongoDB de
TOUS les objets de type BaseObj. Une connexion MongoDB sur une base vide
doit être également ouverte.

"""

from abstraits.obase import tous_objets
from kassie import importeur

# La préparation a eu lieu, on convertit
importeur.supenr.mode = "mongo"
importeur.supenr.config_mongo()

# On force l'enregistrement des objets en mode mongo
importeur.supenr.logger.info("Enregistrement forcé de {} objets".format(
        len(tous_objets)))
for objet in tous_objets.values():
    importeur.supenr.ajouter_objet(objet)

# Enregistrement
importeur.supenr.logger.info("Début de l'enregistrement...")
importeur.supenr.mongo_enregistrer_file()
importeur.supenr.logger.info("... fin de l'enregistrement.")
