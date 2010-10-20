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


"""Ce fichier définit la classe Analyseur détaillée plus bas.

Note: on doit importer dans ce fichier les classes et fonctions susceptibles
d'être évaluées dans l'un ou l'autre des fichiers de configuration.

Pour par exemple faire appel à la méthode randrange, il est nécessaire de
l'importer dans ce fichier. Elle pourra alors être utilisée dans n'importe
quel fichier de configuration.

"""

import os
import sys

class Analyseur:
    """Cette classe définit un gestionnaire de fichier de configuration chargé
    de lire, écrire et interpréter les données de configuration.
    
    Le schéma d'exécution est le suivant :
    -   On souhaite charger un fichier de configuration. Le fichier est lu,
        mis en mémoire et filtré. La forme des données de configuration
        est des plus simple : une ligne, constituée du nom de l'information
        suivie d'un signe égal (=) puis du résultat. Le résultat de la donnée
        sera interprété par Python à l'aide de la fonction eval, au moment
        où elle sera demandée. Cela permet d'avoir des données variables,
        flottantes et propres à l'exécution d'une commande par exemple.
        Une ligne peut être découpée en plusieurs morceaux. Un signe \ doit
        être placé à la fin de la ligne qui doit se prolonger. Ce signe
        n'a aucun effet sur la dernière ligne du fichier.
        Note: si dans le fichier de configuration, une référence est faite
        à une fonction ou une classe, il est nécessaire que la fonction ou
        classe soit importée dans ce fichier-ci.
    -   Lors de la lecture, chaque nom de donnée est stockée à même l'objet,
        en tant qu'attribut propre. Ainsi les noms des donénes devront
        respecter une syntaxe propre, sans espaces ni accents ni caractères
        spéciaux, hormis le signe souligné (_). Il est également préférable
        de n'avoir aucun caractère en majuscule, pour des raisons de 
        convention. Le résultat de la donnée est enregistrée en tant
        que valeur de l'attribut, mais non interprétée.
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
        Autrement dit, analyseur.port appellera eval(3933)
        Cela est rendu possible par la redéfinition de __getattribute__
    
    """
    def __init__(self, nom_fichier, defauts):
        """Permet de lire et enregistrer les données de configuration propres
        au fichier de configuration. On passe en paramètre du constructeur
        le nom du fichier devant être lu, et un dictionnaire contenant la
        configuration de base du fichier. Si aucune configuration n'est trouvée
        dans le fichier, ou si celui-ci est absent, voire partiellement
        renseigné, ce dictionnaire servira à réécrire un fichier complet.
        
        En outre, si des données "périmées" sont trouvées dans le fichier de
        configuration, elles seront supprimées. Ces données "périmées"
        sont des données qui apparaissent dans le fichier de configuration,
        mais non dans le dictionnaire defauts. C'est pourquoi mettre à jour
        le dictionnaire defauts est si important.
        
        La configuration trouvée dans le fichier prime naturellement sur
        celle par défaut. Le dictionnaire defauts n'est utilisé que si des
        données ne sont pas trouvées, ou pour effacer des données périmées.
        
        """
        # On ne stock dans l'objet aucun attribut qui ne soit pas une donnée
        # de configuration
        # On cherche le fichier pour commencer
        recupere = {}
        if not os.path.exists(nom_fichier):
            print("Le fichier de configuration {0} n'existe pas encore" \
                    .format(nom_fichier))
        elif not os.path.isfile(nom_fichier):
            print("{0} n'est pas un fichier".format(nom_fichier))
        else: # on va pouvoir lire le fichier
            with open(nom_fichier, 'r') as fichier_conf:
                contenu = fichier_conf.read()
                # On va supprimer les espaces et tabulations en début de ligne
                t_contenu = []
                for ligne in contenu.split('\n'):
                    t_contenu.append(ligne.strip())
                contenu = "\n".join(t_contenu)
                # On imbrique les lignes découpées
                # Elles finissent par un signe \
                contenu = contenu.replace("\\\n", "")
                # A présent, on lit les données
                for i,ligne in enumerate(contenu.split("\n")):
                    if ligne == "":
                        continue
                    elif "=" not in ligne:
                        print("Le signe '=' n'a pas été trouvé sur la ligne " \
                                "{0}: {1}".format(i+1, ligne))
                    else:
                        nom_donnee = ligne.split("=")[0]
                        donnee = "=".join(ligne.split("=")[1:])
                        nom_donnee = nom_donnee.strip()
                        donnee = donnee.strip()
                        recupere[nom_donnee] = donnee
                
        # On convertit les valeurs de defauts en chaînes de caractères
        for nom in defauts.keys():
            defauts[nom] = str(defauts[nom])
        
        # On met à jour self.__dict__ en fonction de defauts
        complet = dict(defauts)
        complet.update(recupere)

        # On supprime les noms de données qui n'ont plus court (ceux qui
        # sont stockés dans le fichier mais n'ont aucune valeur par défaut)
        for nom in list(complet.keys()):
            if nom not in defauts.keys():
                del complet[nom]

        # On met à jour self.__dict__
        self.__dict__.update(complet)

        # On réenregistre le fichier de configuration si nécessaire
        if defauts.keys() != recupere.keys():
            print("On enregistre la nouvelle configuration")
            try:
                fichier_conf = open(nom_fichier, 'w')
            except IOError:
                print("Le fichier de configuration ne peut pas être édité")
            else:
                for nom, donnee in self.__dict__.items():
                    fichier_conf.write("{0} = {1}\n".format(nom, donnee))
                fichier_conf.close()

    def __getattribute__(self, nom):
        """Méthode qui, au lieu de retourner la valeur de l'objet, retourne
        la donnée interprétée.
        
        """
        if nom.startswith("_"):
            return object.__getattribute__(self, nom)
        elif nom in self.__dict__.keys():
            attribut = object.__getattribute__(self, nom)
            return eval(attribut)
        else:
            raise ValueError("la donnée '{0}' n'a pu être trouvée dans " \
                    "cette configuration".format(nom))
