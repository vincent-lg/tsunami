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


"""Ce fichier définit la classe BaseObj définie plus bas."""

import sys
import traceback
import time

class ObjetsCharges:
    
    """Cette classe possède le comportement d'un dictionnaire.
    Elle permet de stocker les BaseObj récupérés depuis des fichiers.
    
    """
    
    def __init__(self):
        self.__objets = {}
    
    def __contains__(self, item):
        return item in self.__objets
    
    def __getitem__(self, item):
        return self.__objets.get(item)
    
    def __setitem__(self, item, val):
        self.__objets[item] = val
    
    def keys(self):
        return self.__objets.keys()

objets_base = {} # dictionnaire des différents BaseObj {nom_cls:cls}
dict_base_obj = ObjetsCharges()

class MetaBaseObj(type):
    
    """Métaclasse des objets de base.
    Cette métaclasse est là pour gérer les versions des différents objets
    BaseObj :
        Si un objet BaseObj change de structure, pour X raison (par exemple
        un attribut change de nom ou de type), à la récupération l'objet sera
        mis à jour grâce à une fonction définie dans le convertisseur
        (voir BaseObj.update).
        La fonction se trouvera dans un fichier identifiant le nom de la
        classe. On s'assure grâce à cette métaclasse que deux classes
        héritées de BaseObj n'ont pas un nom identique et on attribut
        un numéro de version (0) par défaut aux objets issus de ces
        classes hérités.
    
    """
    
    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        type.__init__(cls, nom, bases, contenu)
        # Si on trouve les attributs _nom et _version,
        # c'est que la classe est versionnée
        if "_nom" in contenu and "_version" in contenu:
            
            cls._version = contenu["_version"]
            cls._nom = contenu["_nom"]
            # Pas de doublons !
            if cls._nom in objets_base:
                if objets_base[cls._nom] == cls:
                    return
                raise RuntimeError("La classe {0} héritée de BaseObj " \
                        "possède le même nom que la classe {1}".format( \
                        str(cls), str(objets_base[cls._nom])))
            objets_base[cls._nom] = cls
            
            # On décore la méthode __init__ de la classe
            ancien_init = cls.__init__
            def new_init(self, *args, **kwargs):
                ancien_init(self, *args, **kwargs)
                self.set_version(cls, cls._version)
            cls.__init__ = new_init
        else:
            cls._version = None
            cls._nom = None

INIT, CONSTRUIT = 0, 1

class BaseObj(metaclass=MetaBaseObj):
    
    """Cette classe définit la base d'un objet destiné à être enregistré,
    directement ou indirectement dans un fichier.
    
    Rappelons que :
    *   Les objets destinés à être DIRECTEMENT enregistrés dans des fichiers
        doivent être hérités soit de :
        -   ObjetID (voir abstraits/id/__init__.py)
        -   Unique (voir abstraits/unique/__init__.py)
        
        Ces deux classes héritent de BaseObj et en reprennent donc les
        mécanismes.
    *   Les objets destinés à être INDIRECTEMENT enregistrés dans des fichiers
        doivent être hérités de BaseObj.
        Ces objets sont ceux destinés à être enregistrés dans des fichiers
        sous la forme d'attributs d'autres objets par exemple.
    
    Si vous héritez la classe BaseObj, vous devrez redéfinir une
    méthode __getnewargs__. Cette méthode est appelée
    à la récupération de l'objet depuis un fichier et doit retourner un tuple
    des informations à retourner pour construire l'objet.
    L'intérêt est qu'ainsi, à chaque récupération de votre objet, il est
    reconstruit. Si d'une session à l'autre vous redéfinissez de nouveaux
    attributs, ils seront donc bien présents quand vous aurez récupéré votre
    objet.
    
    Chaque BaseObj possède :
    -   un numéro d'identification > 0
        Celui-ci est créé lors de la construction de BaseObj.
        Vous n'avez pas à vous en soucier, simplement veiller que
        le constructeur de votre objet hérité de BaseObj appelle bien
        le constructeur de BaseObj:
        >>> class HeriteDeBaseObj(BaseObj):
        ...     def __init__(self, ...):
        ...         BaseObj.__init__(self)
        ..          ...
    -   un timestamp mis à jour lors de l'enregistrement de l'objet.
        Voir la méthode __getstate__ de BaseObj.
    
    """
    
    importeur = None
    _id_base_actuel = 1
    
    def __init__(self):
        """Instancie un simple statut"""
        self._statut = INIT
        # On initialise le dictionnaire des versions de l'objet
        self._dict_version = {}
        self._ts = time.time() # le timestamp actuel
        self._id_base = BaseObj._id_base_actuel
        BaseObj._id_base_actuel += 1
        type(self).importeur.supenr.enregistrer_id_base()
    
    def __getnewargs__(self):
        raise NotImplementedError
    
    def version_actuelle(self, classe):
        """Retourne la version actuelle de l'objet.
        Cette version est celle enregistrée dans l'objet. Elle peut
        donc être différence de la classe (c'est le cas au chargement d'un
        objet à mettre à jour).
        
        """
        if classe._nom in self._dict_version:
            return self._dict_version[classe._nom]
        else:
            return 0
    
    def set_version(self, classe, version):
        """Met le numéro de version dans le dictionnaire de version de l'objet.
        
        """
        self._dict_version[classe._nom] = version
    
    def _construire(self):
        """Construit l'objet"""
        self._statut = CONSTRUIT
    
    @property
    def construit(self):
        return hasattr(self, "_statut") and self._statut == CONSTRUIT
    
    def __getstate__(self):
        """Méthode appelée au moment de sérialiser l'objet.
        On met à jour le timestamp contenu dans self._ts.
        Ainsi, au moment de la récupération de plusieurs BaseObj de même
        _base_id, on saura quel a été le dernier enregistré.
        
        """
        self._ts = time.time()
        return self.__dict__
    
    def __setstate__(self, dico_attrs):
        """Méthode appelée lors de la désérialisation de l'objet"""
        # On récupère la classe
        classe = type(self)
        # On appel son constructeur
        classe.__init__(self, *self.__getnewargs__())
        # On met à jour les attributs
        self.__dict__.update(dico_attrs)
        # Si l'objet existe dans le dictionnaire des BaseObj
        if self._id_base in dict_base_obj.keys():
            # Si le temps d'enregistrement de self est supérieur à celui de
            # l'objet dans le dictionnaire, on le remplace
            if self._ts > dict_base_obj[self._id_base]._ts:
                dict_base_obj[self._id_base] = self
        else:
            dict_base_obj[self._id_base] = self
        
        # On ajoute l'objet dans supenr, pour un futur nettoyage
        type(self).importeur.supenr.objets_a_nettoyer.append(self)
        
        # On vérifie maintenant s'il a besoin d'une vraie mis à jour
        self._update(classe)
    
    def _update(self, classe):
        """Méthode appelée pendant la désérialisation de l'objet,
        destinée à vérifier si l'objet doit être mis à jour et, le cas
        échéant, le mettre à jour.
            
        """
        # Mise à jour récursive par rapport aux classes-mères
        for base in classe.__bases__:
            # Inutile d'essayer de mettre à jour 'object'
            if base is not object:
                base._update(self, base)
        if classe._nom in objets_base:
            # On importe le convertisseur dédié à la classe en cours
            try:
                convertisseur = getattr(__import__( \
                        "primaires.supenr.convertisseurs." + classe._nom, \
                        globals(), locals(), ["Convertisseur"]), \
                        "Convertisseur")
            except ImportError as error:
                print("La classe {0} suivie en version ne possède pas de " \
                        "fichier de convertisseurs dans primaires.supenr." \
                        "convertisseurs".format(classe._nom))
                exit()
            except AttributeError as error:
                print("Le fichier {0}.py dans primaires.supenr." \
                        "convertisseurs ne possède pas de classe " \
                        "Convertisseur".format(classe._nom))
                exit()
            
            # On vérifie la version de la classe et celle de l'objet
            # Rappel :
            #   self.version_actuelle() retourne la version enregistrée
            #   classe._version retourne la version de la classe
            while self.version_actuelle(classe) < classe._version:
                try:
                    # On appelle la version de conversion
                    getattr(convertisseur, "depuis_version_" + \
                            str(self.version_actuelle(classe)))(self, classe)
                except AttributeError as error:
                    print("Le fichier {0}.py dans primaires.supenr." \
                            "convertisseurs ne comporte pas de méthode " \
                            "depuis_version_".format(classe._nom) + str( \
                            self.version_actuelle(classe)))
                    print(traceback.format_exc())
                    exit()

    
    def __getattribute__(self, nom_attr):
        """Méthode appelé quand on cherche à récupérer l'attribut nom_attr
        Si l'attribut qu'on cherche à récupérer est un type ID, on retourne
        l'objet correspondant à l'ID.
        Pour ce faire, on demande à parid l'objet correspondant à notre ID.
        
        """
        objet = object.__getattribute__(self, nom_attr)
        if nom_attr != "id" and est_id(objet):
            # On cherche l'objet correspondant à cet ID
            objet = objet.get_objet()
        
        return objet
    
    def __setattr__(self, nom_attr, val_attr):
        """Méthode appelée quand on cherche à écrire l'objet val_attr dans
        l'attribut nom_attr.
        
        Si val_attr est un ObjetID (il possède l'attribut id), on écrit
        dans l'attribut nom_attr non pas val_attr mais l'ID de val_attr.
        
        """
        if nom_attr != "id" and hasattr(val_attr, "est_objet_id"):
            # val_attr est un ObjetID
            val_attr = val_attr.id
        
        object.__setattr__(self, nom_attr, val_attr)

def est_id(objet):
    """Retourne True si objet est un ID"""
    return hasattr(type(objet), "_objetid_")
