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


"""Ce fichier contient la classe Anaconf, un analyseur de fichiers
de configuration.

Une instance de cette classe est créée à la fin du fichier.
Cette instance sera la seule nécessaire pour manipuler des données de
configuration.

Mode d'emploi :
*   On importe l'instance 'anaconf' :
    >>> from bases.anaconf import anaconf
*   Si c'est la première fois qu'on le manipule, on doit le configurer :
    >>> anaconf.config(parser_cmd) # le parser de la ligne de commande
    Normalement c'est la tâche du fichier principal à la racine du projet.
*   On peut ensuite créer et manipuler des données de configuration
    Pour créer un analyseur d'une donnée de configuration, on appelle
    'get_config' en lui passant en paramètre :
    -   nom_id : un nom identifiant
        Il doit identifier de manière unique un analyseur.
        Si l'analyseur est propre à un module, préférer mettre un nom
        comme 'nom_du_module:nom_analyseur'
        Ce nom sera nécessaire si on souhaite récupérer la configuration
        depuis un autre point du code ('get_config crée un analyseur
        s'il n'existe pas, retourne celui existant sinon)
    -   le chemin menant au fichier de configuration. Celui-ci doit être
        un chemin relatif, à partir de REP_CONFIG
    -   le nom du fichier par défaut [1]
    -   la chaîne de configuration par défaut [1]
    Ces trois derniers paramètres ne sont indispensables que si on veut créer
    un analyseur. Si on souhaite en récupérer un existant, on n'a besoin que de
    préciser le nom identifiant 'nom_id'.
*   Avec cet analyseur, vous pouvez ensuite avoir accès aux données
    configurées. Si dans le fichier de configuration vous trouvez :
        ma_donnee = 5 * 12
    Vous pourrez accéder à l'attribut 'ma_donnee' de votre analyseur qui
    contiendra 60 (voir la note plus bas).

[1] L'analyse des données de configuration s'effectue depuis un modèle
    contenu en dur dans le code. Chaque module a charge de ses modèles de
    configuration. Pour le corps, voir dans src/corps/config.py
    Ces modèles sont enregistrés dans une chaîne de caractères du même
    format qu'un fichier de configuration. Ce modèle permet à l'analyseur
    de savoir quelles données doivent être définies dans le fichier de
    configuration analysé. Si les données ne sont pas présentes dans le
    fichier analysé, on prend leur valeur par défaut dans le modèle.
    Le modèle permet également de construire un fichier si certaines données
    manquent ou même si le fichier de configuration n'existe pas.
    On doit également donner un nom au modèle. Celui-ci est interprété comme
    un fichier de configuration et si une erreur est détectée, c'est ce nom
    qui sera loggé pour avertir d'une erreur. Les modèles ne doivent
    naturellement pas en comporter (alors que les fichiers de configuration le
    peuvent jusqu'à un certain point).

NOTE IMPORTANTE: les données présentes dans un modèle sont interprétées
    comme du code Python. Si vous devez mettre une chaîne de caractère comme
    donnée de configuration, n'oubliez donc pas de l'entourer de guillemets ou
    autres délimiteurs.

"""

import os

from bases.anaconf.analyseur import Analyseur
from bases.logs import man_logs

# Dossier d'enregistrement des fichiers de configuration
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
REP_CONFIG = os.path.expanduser("~") + os.sep + "kassie" + os.sep + "config"

class Anaconf:
    
    """Classe manipulant les fichiers de configuration.
    
    Elle gère la lecture, l'écriture et l'interprétation de ces fichiers.
    
    Chaque module primaire ou secondaire ayant besoin d'enregistrer des
    informations de configuration devra passer par anaconf.
    C'est également vrai pour les informations du corps
    (configuration générale).
    
    """
    
    def __init__(self):
        """Constructeur du gestionnaire de configuration."""
        self.configs = {}
    
    def config(self, parser_cmd):
        """Méthode de configuration.
        
        On se charge ici de modifier la valeur de REP_CONFIG
        (le chemin menant au fichier de configuration) si la ligne
        de commande précise un autre chemin. On crée le dossier
        si il n'existe pas.
        
        """
        global REP_CONFIG
        if "chemin-configuration" in parser_cmd.keys():
            REP_CONFIG = parser_cmd["chemin-configuration"]
        
        # On construit le répertoire s'il n'existe pas
        if not os.path.exists(REP_CONFIG):
            os.makedirs(REP_CONFIG)
    
    def get_config(self, nom_id, chemin="", nom_defaut="", defaut=""):
        """Charge ou retourne une configuration existante.
        
        Cette méthode permet de charger une configuration contenue dans
        le fichier passé en paramètre.
        Si le fichier a déjà été chargé, on retourne l'analyseur correspondant.
        Le paramètre 'nom_id' sert d'identifiant pour les configurations déjà
        chargées.
        Le paramètre 'defaut' est une chaîne écrite comme un fichier
        de configuration, analysée comme telle et contenant les données par
        défaut du modèle.
        Si certaines données ne sont pas trouvées dans le fichier chargé,
        on les met à jour grâce à ce paramètre et on met à jour
        le fichier de configuration.
        
        """
        global REP_CONFIG
        chemin = REP_CONFIG + os.sep + chemin
        if not nom_id in self.configs.keys():
            # On construit l'analyseur
            # Cela revient à charger le fichier de configuration
            # ATTENTION : si le chemin est laissé vide, on lève une exception
            # De même, l'utilisateur doit avoir accès en lecture
            # et écriture au fichier
            if chemin == "":
                raise RuntimeError("le chargement de l'analyseur {} " \
                        "a échoué. Aucun chemin passé en paramètre".format(
                        nom_id))
            elif os.path.exists(chemin) and not os.access(chemin, os.R_OK):
                raise RuntimeError("le chargement de l'analyseur {} " \
                        "a échoué. Droits en lecture refusés sur {}".format(
                        nom_id, chemin))
            elif os.path.exists(chemin) and not os.access(chemin, os.W_OK):
                raise RuntimeError("le chargement de l'analyseur {} " \
                        "a échoué. Droits en écriture refusés sur {}".format(
                        nom_id, chemin))
            
            logger = man_logs.creer_logger("anaconf", nom_id)
            # On construit le répertoire s'il n'existe pas
            rep = os.path.split(chemin)[0]
            if not os.path.exists(rep):
                os.makedirs(rep)
            
            # On l'ajoute aux configurations chargées
            self.configs[nom_id] = Analyseur(chemin,
                    nom_defaut, defaut, logger)
        
        # On retourne l'analyseur
        return self.configs[nom_id]

# On crée l'anaconf (analyseur des fichiers de configuration)
anaconf = Anaconf()
