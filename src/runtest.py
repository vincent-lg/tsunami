# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier chargé de lancer les tests unitaires.

Ne pas utiliser 'python -m unittest' mais exécutez ce script. La
raison est simple : ce script est un script de boostrap. Il charge
l'importeur et les modules. La sauvegarde des enregistrements
n'est cependant ni chargée, ni écrasée.

"""

import unittest

from lib import *

from bases.anaconf import anaconf
from bases.importeur import Importeur
from bases.logs import man_logs
from bases.parser_cmd import ParserCMD
from corps.config import pere
from primaires.format.date import *
from reseau.connexions.serveur import *

parser_cmd = ParserCMD()
parser_cmd.interpreter()
anaconf.config(parser_cmd)
config_globale = anaconf.get_config("globale", "kassie.cfg", \
        "modèle global", pere)
man_logs.config(anaconf, parser_cmd)
log = man_logs.creer_logger("", "sup", "kassie.log")

serveur = ConnexionServeur(4000, config_globale.nb_clients_attente, \
        config_globale.nb_max_connectes, config_globale.tps_attente_connexion,
        config_globale.tps_attente_reception)

importeur = Importeur(parser_cmd, anaconf, man_logs, serveur,
        sauvegarde=False)
importeur.tout_charger()
importeur.tout_instancier()
importeur.tout_configurer()
importeur.tout_initialiser()
importeur.tout_preparer()

tests = unittest.TestLoader().discover('.')
unittest.TextTestRunner().run(tests)

importeur.tout_detruire()
importeur.tout_arreter()
