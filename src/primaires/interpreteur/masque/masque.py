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

masques_def = {}

class MetaMasque(type):
    
    """Métaclasse des masques.
    Cette métaclasse permet d'ajouter les masques dans dic_masques
    dès leur définition en classe.
    
    """
    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        type.__init__(cls, nom, bases, contenu)
        if cls.nom:
            masque = cls()
            masques_def[cls.nom] = masque
            module = masque.__module__
            masque.module = module.split(".")[1]

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
    
    D'un point de vue plus technique, les masques sont des objets singleton.
    Il n'en existe qu'un par masque. La méthode 'init' est appelée
    à chaque fois que le masque doit être validé et c'est dans cette méthode
    que vous devez définir vos attributs éventuels à votre masque,
    pas dans le constructeur (celui-ci ne devrait jamais être redéfini par
    une sous-classe).
    
    Exemple :
    >>> class MasquePersonnage(Masque):
    ...     '''Masque attendant un nom de personnage.'''
    ...     nom = "personnage"
    ...     def init(self):
    ...         self.personnage = None
    
    Pour comprendre comment un masque est interprétez, référez-vous à la
    méthode 'interpreter'.
    
    """
    
    importeur = None
    nom = ""
    
    def __init__(self):
        """Crée un nouveau masque"""
        self.nom = type(self).nom
        self.type = None
        self.proprietes = []
    
    def init(self):
        """Méthode à redéfinir pour initialiser des attributs"""
        raise NotImplementedError
    
    def valider(self, personnage, dic_masques, commande):
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
        
        """
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
    
