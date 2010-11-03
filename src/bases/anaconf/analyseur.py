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


from bases.anaconf.fichier_configuration import FichierConfiguration

"""Ce fichier définit la classe Analyseur détaillée plus bas.

Note : l'analyse se fait par évaluation de chaînes contenant du code Python.
Si ces chaînes font référence à des objets, fonctions, méthodes, elles doivent
être définies dans les globales de l'interpréteur grâce à la méthode
'set_globales'. Voir l'aide pour plus d'informations.

"""

import os
import sys

class Analyseur:
    """Cette classe définit un gestionnaire de fichiers de configuration chargé
    de lire, écrire et interpréter les données de configuration.
    
    Le schéma d'exécution est le suivant :
    -   On souhaite charger un fichier de configuration. Le fichier est lu,
        mis en mémoire et filtré. La forme des données de configuration
        est des plus simples : une ligne, constituée du nom de l'information
        suivie d'un signe égal (=) puis du résultat. Le résultat de la donnée
        sera interprété par Python à l'aide de la fonction eval, au moment
        où elle sera demandée. Cela permet d'avoir des données variables,
        flottantes et propres à l'exécution d'une commande par exemple.
        Une ligne peut être découpée en plusieurs morceaux. Un signe \ doit
        être placé à la fin de la ligne qui doit se prolonger. Ce signe
        n'a aucun effet sur la dernière ligne du fichier.
        Une ligne peut également être un commentaire, elle commencera alors par
        '#' et sera ignorée.
        Note: si dans le fichier de configuration, une référence est faite
        à une fonction ou une classe, il est nécessaire que la fonction ou
        classe soit déclarée comme globales de l'interpréteur (voir
        'set_globales').
    -   Lors de la lecture, chaque nom de donnée est stocké à même l'objet,
        en tant qu'attribut propre. Ainsi les noms des donénes devront
        respecter une syntaxe propre, sans espaces ni accents ni caractères
        spéciaux, hormis le signe souligné (_). Il est également préférable
        de n'avoir aucun caractère en majuscule, pour des raisons de 
        convention. Le résultat de la donnée est enregistré en tant
        que valeur de l'attribut, mais non interprété.
        Les commentaires sont tout simplement ignorés.
    -   On demande à l'objet d'obtenir la valeur d'une donnée. Dans ce cas et
        dans ce cas uniquement, la donnée est interprétée, puis retournée.
        On se base sur la fonction eval pour interpréter la donnée.
    
    Exemple :
    *   fichier general.cfg
        port = 3933
        attente_connexion = 0.2
    *   le constructeur d'Analyseur construit un objet contenant deux
        attributs, port et attente_connexion
    *   quand on souhaite y accéder, on interprète la donnée
        Autrement dit, analyseur.port appellera eval("3933")
        Cela est rendu possible par la redéfinition de __getattribute__
    
    """
    def __init__(self, nom_fichier, nom_defaut, defaut, logger):
        """Permet de lire et enregistrer les données de configuration propres
        au fichier de configuration.
        
        Notez qu'un analyseur doit être construit depuis la méthode
        'get_config' d''anaconf' et non directement.
        On passe en paramètre du constructeur :
        *   Le nom du fichier de configuration. Il permet naturellement
            de l'ouvrir, étape indispensable pour l'analyser
        *   Le nom du fichier par défaut (il s'agit d'un repère, si une erreur
            est trouvée dans l'interprétation du modèle)
        *   La chaîne contenant le fichier de configuration par défaut.
            Cette chaîne se trouve en dur dans le code. Elle est
            indispensable : un fichier de configuration ne peut être interprété
            sans son modèle. Pour le modèle de la configuration globale, voir :
            src/corps/config.py
        *   Le logger : il est propre à cet analyseur et permet de faire
            remonter les erreurs liées à l'interprétation du modèle ou du
            fichier de configuration
        
        La configuration trouvée dans le fichier prime naturellement sur
        celle par défaut. La chaîne defaut n'est utilisé que si des
        données ne sont pas trouvées, ou pour effacer des données périmées.
        
        """
        self._globales = {}
        self._logger = logger
        self._logger.filtrer_niveau("warning")
        # On cherche le fichier pour commencer
        fichier_charge = None
        if not os.path.exists(nom_fichier):
            self._logger.info("Le fichier de configuration {0} n'existe pas " \
                    "encore".format(nom_fichier))
        elif not os.path.isfile(nom_fichier):
            self._logger.info("Le fichier de configuration {0} n'est pas un " \
                    "fichier, accès impossible".format(nom_fichier))
        else: # on va pouvoir lire le fichier
            with open(nom_fichier, 'r') as fichier_conf:
                contenu = fichier_conf.read()           
            # On analyse le fichier de configuration
            fichier_charge = FichierConfiguration(nom_fichier, contenu, \
                    self._logger)
        
        # On analyse le fichier par défaut
        fichier_defaut = FichierConfiguration(nom_defaut, defaut, \
                self._logger)
        
        # On met à jour self
        complet = dict(fichier_defaut.donnees)
        if fichier_charge:
            complet.update(fichier_charge.donnees)

        # On met à jour self.__dict__
        self.__dict__.update(complet)

        # On réenregistre le fichier de configuration si nécessaire
        if fichier_charge is None or fichier_defaut.donnees.keys() != \
                fichier_charge.donnees.keys():
            self._logger.info("On réécrit le fichier {0}".format(nom_fichier))
            try:
                fichier_conf = open(nom_fichier, 'w')
            except IOError:
                self._logger.warning("Le fichier de configuration ne peut pas être édité")
            else:
                # On demande au fichier par défaut de prendre en compte les
                # données de configuration du fichier chargé
                if fichier_charge:
                    fichier_defaut.mettre_a_jour(fichier_charge)
                fichier_conf.write(fichier_defaut.fichier.strip("\n"))
                fichier_conf.close()

    def __getattribute__(self, nom):
        """Méthode qui, au lieu de retourner la valeur de l'objet, retourne
        la donnée interprétée.
        
        """
        if nom.startswith("_") or not object.__getattribute__(self, nom):
            return object.__getattribute__(self, nom)
        elif nom in self.__dict__.keys():
            attribut = object.__getattribute__(self, nom)
            return eval(attribut)
        else:
            raise ValueError("La donnée '{0}' n'a pu être trouvée dans " \
                    "cette configuration".format(nom))
    
    def set_globales(self, globales):
        """Paramètre les globales, données sous la forme d'un dictionnaires.
        Ces globales sont utilisées dans l'évaluation de données de
        configuration.
        Si par exemple une de vos données de configuration fait appel à la
        fonction 'randrange', il faut l'ajouter dans les globales.
        >>> import random
        >>> analyseur = Analyseur("....cfg")
        >>> analyseur.set_globales({"randrange":random.randrange})
        >>> analyseur.hasard # contient randrange(8)
        6
        
        """
        self._globales = globales
