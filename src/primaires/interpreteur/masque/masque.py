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


"""Fichier définissant la classe Masque détaillée plus bas"""

import re

masques_def = {}


# Constantes
RE_MOT_CLE = re.compile(r"^([a-z]*)/([a-z]*)$")
RE_PROPRIETES = re.compile(r"([a-z:]*)(\{(.*)\})?$")

class MetaMasque(type):
    
    """Métaclasse des masques.
    Cette métaclasse permet d'ajouter les masques dans dic_masques
    dès leur définition en classe.
    
    """
    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        type.__init__(cls, nom, bases, contenu)
        if cls.nom:
            masques_def[cls.nom] = cls
            module = cls.__module__
            cls.module = module.split(".")[1]

class Masque(metaclass=MetaMasque):
    
    """Classe représentant un masque.
    
    Un masque est un élément interprétable d'une commande.
    Par exemple, un masque peut représenter, dans le nom d'une commande,
    le nom d'un personnage. La commande 'regarder' par exemple précise
    qu'elle attend en paramètre un nom de joueur et définit dans son schéma
    de validation le masque correspondant.
    
    Au moment de l'interprétation de la commande, les différents masques sont
    automatiquement validés. Cela signifie que la commande entrée
    par le joueur est testée par le masque. Si le masque confirme qu'elle
    tient un nom de joueur, il autorise la commande à s'interpréter. Sinon,
    il renvoie une erreur au joueur.
    
    Vu que la plupart des masques sont réutilisés, ce procédé permet de
    gagner du temps sur le développement de commandes.
    
    D'un point de vue plus technique, à chaque fois que, dans son schéma,
    une commande fait appel à un masque, une instance du masque est créée.
    Pour définir un masque, il faut faire une sous-classe de Masque en
    lui donnant un nom bien précis.
    Les attributs spécifiques que vous voulez ajouter à votre masque
    ne doivent pas être définis dans le constructeur mais dans la méthode
    'init'.
    Exemple :
    >>> class MasquePersonnage(Masque):
    ...     '''Masque attendant un nom de personnage.'''
    ...     nom = "personnage"
    ...     def init(self):
    ...         self.personnage = None
    
    Pour comprendre comment un masque est validé, référez-vous à la
    méthode 'valider'.
    
    """
    
    importeur = None
    nom = ""
    
    def __init__(self):
        """Crée un nouveau masque"""
        self.nom = type(self).nom
        self.type = None
        self.proprietes = {}
        self.mot_cle = False
        self.a_interpreter = None
        self.mots_cles = {
            "francais": "",
            "anglais": "",
        }
    
    def init(self):
        """Méthode à redéfinir pour initialiser des attributs"""
        raise NotImplementedError
    
    def construire(self, schema):
        """Construction du masque depuis un schéma.
        
        Cette méthode est appelée au moment de la construction d'un masque
        depuis un NoeudMasque.
        
        Elle se charge :
        -   De savoir si le masque est un mot-clé ou non
        -   De savoir si le masque possède des propriétés
        
        """
        mot_cle = RE_MOT_CLE.search(schema)
        proprietes = RE_PROPRIETES.search(schema)
        if proprietes:
            groupes = proprietes.groups()
            nom, none, proprietes = groupes
            if proprietes:
                proprietes = proprietes.replace("=", ":")
    
    def repartir(self, personnage, masques, commande):
        """Méthode de répartition."""
        raise NotImplementedError
    
    def valider(self, personnage, dic_masques):
        """Méthode de validation.
        
        Elle prend en paramètres :
        -   le personnage qui a entré la commande
        -   le dic_masques : un dictionnaire ordonné contenant les masques
            déjà validés pour cette commande
        -   la commande, sous la forme d'une liste de caractères
        
        Cette méthode peut retourner :
        -   True : le masque a été validé correctement
        -   False : il s'est produit une erreur et le masque n'a pu
            être validé
        
        Habituellement, en cas de non validation, on préférera lever
        une exception ErreurValidation en lui passant en paramètre
        le message à envoyer au joueur.
        
        Cette commande permet également d'interpréter les propriétés.
        Il est donc conseillé, quand vous développez une sous-classe de
        Masque, d'appeler dans la méthode 'valider' la méthode parente.
        
        """
        # Interprétation des propriétés
        globales = {"personnage": personnage, "dic_masques": dic_masques}
        for cle, valeur in self.proprietes.items():
            propriete = eval(valeur, globales)
            setattr(self, cle, propriete)
        
        return True
    
    def __str__(self):
        """Affichage du masque"""
        return self.nom
    
    def est_parametre(self):
        """Return True si ce masque est un paramètre"""
        return False
    
    def afficher(self, personnage):
        """Retourne un affichage du masque pour le personnage"""
        return self.nom
    
