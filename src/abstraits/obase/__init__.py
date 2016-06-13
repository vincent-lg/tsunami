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


"""Ce fichier définit la classe BaseObj définie plus bas."""

import sys
import traceback
import time
from collections import OrderedDict

from bases.collections.dictionnaire import *
from bases.collections.liste import Liste

objets_base = {} # dictionnaire des différents BaseObj {nom_cls:cls}


# Objets chargés
objets = {}
objets_par_type = {}
ids = {}
statut_gen = 0 # 0 => OK, 1 => en cours
classes_base = {}

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
        classes_base[cls.__module__ + "." + cls.__name__] = cls
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

    """Classe devant être héritée de la grande majorité des classes de Kassie.

    Le test est simple : si l'objet issu de la classe doit être enregistré,
    l'hériter de BaseObj.

    """

    importeur = None
    enregistrer = False
    _nom = "base_obj"
    _version = 1
    def __init__(self):
        """Instancie un simple statut"""
        self._statut = INIT
        # On initialise le dictionnaire des versions de l'objet
        self._dict_version = {}
        self.e_existe = True
        self.ajouter_enr()

    def __getnewargs__(self):
        raise NotImplementedError(
                "la classe " + str(type(self)) + " n'a pas de méthode " \
                "__getnewargs__")

    def ajouter_enr(self):
        if self.e_existe and type(self).enregistrer and statut_gen == 0 and \
                id(self) not in objets:
            objets[id(self)] = self
            liste = objets_par_type.get(type(self), [])
            liste.append(self)
            objets_par_type[type(self)] = liste

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
        """Met le numéro de version dans le dictionnaire de version."""
        self._dict_version[classe._nom] = version

    def _construire(self):
        """Construit l'objet"""
        object.__setattr__(self, "_statut", CONSTRUIT)

    def detruire(self):
        """Marque l'objet comme détruit."""
        self.e_existe = False
        importeur.supenr.detruire_objet(self)
        if id(self) in objets:
            del objets[id(self)]

    @property
    def construit(self):
        return hasattr(self, "_statut") and self._statut == CONSTRUIT

    def __setstate__(self, dico_attrs):
        """Méthode appelée lors de la désérialisation de l'objet"""
        global statut_gen
        statut_gen = 1
        # On récupère la classe
        classe = type(self)
        # On appel son constructeur
        try:
            classe.__init__(self, *self.__getnewargs__())
        except NotImplementedError:
            print("Méthode __getnewargs__ non définie pour", classe)
            sys.exit(1)
        except TypeError as err:
            print("Erreur lors de l'appel au constructeur de", classe, err)
            print(traceback.format_exc())
            sys.exit(1)
        self.__dict__.update(dico_attrs)

        # On vérifie s'il a besoin d'une vraie mis à jour
        self._update(classe)
        statut_gen = 0
        self.ajouter_enr()

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

        Si l'attribut n'existe plus, on retourne None.

        """
        objet = object.__getattribute__(self, nom_attr)
        if hasattr(objet, "e_existe") and not objet.e_existe:
            return None

        return objet

    def __getstate__(self):
        return dict(self.__dict__)

    def __setattr__(self, attr, valeur):
        """L'objet est modifié."""
        object.__setattr__(self, attr, valeur)
        if self.construit:
            importeur.supenr.ajouter_objet(self)

    def _enregistrer(self):
        """Force l'enregistrement de l'objet."""
        importeur.supenr.mongo_debug = True
        if self.construit:
            importeur.supenr.ajouter_objet(self)
