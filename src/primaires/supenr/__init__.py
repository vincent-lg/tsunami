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


"""Ce fichier contient le module primaire supenr."""

from ast import literal_eval
import copy
import os
import pickle
import sys
import time
from yaml import dump, load

transforms = []

try:
    from bson.errors import InvalidDocument
    from bson.objectid import ObjectId
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    from primaires.supenr.fraction import TransformFraction
    from primaires.supenr.ordered import TransformOrderedDict
    transforms.append(TransformFraction())
    transforms.append(TransformOrderedDict())
except ImportError:
    MongoClient = None

from abstraits.module import *
from abstraits.obase import *
from primaires.supenr import commandes
from primaires.supenr.config import cfg_supenr

# Dossier d'enregistrement des fichiers-données
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
REP_ENRS = os.path.expanduser("~") + os.sep + "kassie"

class Module(BaseModule):

    """Classe du module 'supenr'.

    Ce module gère l'enregistrement des données et leur récupération.
    Les objets enregistrés doivent dériver indirectement de
    abstraits.obase.BaseObj (voir abstraits/obase/__init__.py pour plus
    d'informations).

    Habituellement, il n'est pas nécessaire de manipuler directement
    ce module.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "supenr", "primaire")
        self.cfg = None
        self.mode = ""
        self.logger = type(self.importeur).man_logs.creer_logger("supenr", \
                "supenr")
        self.enregistre_actuellement = False
        self.fichiers = {}
        self.pret = False
        self.met_preparer = []

        # Objets utiles pour MongoDB
        self.mongo_db = None
        self.initial = True
        self.mongo_temporaire = {}
        self.mongo_file = {}
        self.mongo_collections = {}
        self.mongo_objets = {}
        self.mongo_table = []
        self.mongo_debug = False
        self.mongo_differe = {}
        self.mongo_complets = []
        self.mongo_nb_requetes = 0

    def config(self):
        """Configuration du module.

        On se base sur parser_cmd pour savoir si un dossier d'enregistrement
        des fichiers-données a été défini.
        Cette donnée peut également se trouver dans les données globales de
        configuration.

        Une fois qu'on a obtenu cette donnée, on charge les fichiers
        yml qui servent de complément à l'enregistrement.

        """
        global REP_ENRS
        self.cfg = importeur.anaconf.get_config("supenr",
            "supenr/supenr.cfg", "module d'enregistrement", cfg_supenr)
        if not self.mode:
            self.mode = self.cfg.mode

        parser_cmd = type(self.importeur).parser_cmd
        config_globale = type(self.importeur).anaconf.get_config("globale")

        # Si le mode d'enregistrement est mongo
        if self.mode == "mongo":
            self.config_mongo()

        # Si le mode d'enregistrement est pickle
        if self.mode == "pickle":
            if config_globale.chemin_enregistrement:
                REP_ENRS = config_globale.chemin_enregistrement

            if "chemin-enregistrement" in parser_cmd.keys():
                REP_ENRS = parser_cmd["chemin-enregistrement"]

            # On construit le répertoire s'il n'existe pas
            if not os.path.exists(REP_ENRS):
                os.makedirs(REP_ENRS)
        elif self.mode != "mongo":
            self.logger.fatal("Mode d'enregistrement {} inconnu.".format(
                    repr(mode)))
            sys.exit(1)

        # On augmente la limite de récursion
        sys.setrecursionlimit(12000)

        self.pret = True

        # Chargement des fichiers yml
        if importeur.sauvegarde:
            for nom_fichier in os.listdir(REP_ENRS):
                if nom_fichier.endswith(".yml"):
                    fichier = open(REP_ENRS + os.sep + nom_fichier, "r")
                    contenu = fichier.read()
                    donnees = load(contenu)
                    nom = nom_fichier[:-4]
                    self.fichiers[nom] = donnees
                    self.logger.info("Chargement du fichier YML {}".format(
                            repr(nom)))

        BaseModule.config(self)

    def config_mongo(self):
        """Configuration spécifique de MongoDB."""
        if MongoClient is None:
            self.logger.warning("Impossible de charger pymongo, " \
                    "retour au mode d'enregistrement 'pickle'")
            self.mode = "pickle"
        else:
            # On essaye de se connecter
            try:
                connexion = MongoClient()
            except ConnectionFailure:
                self.logger.warning("Impossible de se connecter au " \
                        "serveur MongoDB. Retour sur le mode 'pickle'")
                self.mode = "pickle"
            else:
                self.mongo_db = connexion[self.cfg.nom_mongodb]

    def init(self):
        """Chargement de tous les objets (pickle)."""
        if self.mode == "pickle":
            self.charger()

            # Création de l'action différée pour enregistrer périodiquement
            importeur.diffact.ajouter_action("enregistrement", 60 * 60,
                    self.enregistrer_periodiquement)
        else: # Mongo
            self.mongo_tout_charger()
            importeur.diffact.ajouter_action("enregistrement", 1,
                    self.mongo_premier_enregistrement)
        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajoute les commandes à l'interpréteur."""
        self.commandes = [
            commandes.mongo.CmdMongo(),
        ]

        for cmd in self.commandes:
            importeur.interpreteur.ajouter_commande(cmd)

    def preparer(self):
        """Appel des méthodes différées."""
        for liste in self.met_preparer:
            callback = liste[0]
            arguments = liste[1:]
            callback(*arguments)

    def detruire(self):
        """Destruction du module"""
        if self.mode == "pickle":
            self.enregistrer()
        else:
            self.mongo_enregistrer_file(False)

        BaseModule.detruire(self)

    def sauver_fichier(self, nom, donnees):
        """Sauvegarde le fichier XML précisé.

        Le fichier sera le nom avec l'extension '.yml'. Les
        données doivent être transmises dans un dictionnaire.

        """
        if not importeur.sauvegarde:
            return

        chemin = REP_ENRS + os.sep + nom + ".yml"
        contenu = dump(donnees, default_flow_style=False)
        fichier = open(chemin, "w")
        fichier.write(contenu)
        fichier.close()

    def enregistrer(self):
        """Méthode appelée pour enregistrer TOUS les objets par pickle."""
        if not importeur.sauvegarde:
            return

        global REP_ENRS
        if not self.pret:
            raise RuntimeError("le supenr n'est pas prêt à enregistrer")

        if self.enregistre_actuellement:
            return

        a_enregistrer = [o for o in objets.values() if o.e_existe]
        self.logger.info("{} objets, dans {}o sont prêts à être " \
                "enregistrés.".format(str(len(a_enregistrer)),
                str(len(pickle.dumps(a_enregistrer)))))
        self.enregistre_actuellement = True
        chemin_dest = REP_ENRS + os.sep + "enregistrements.bin"

        # On essaye d'ouvrir le fichier
        try:
            fichier_enr = open(chemin_dest, 'wb')
        except IOError as io_err:
            self.logger.warning("Le fichier {} destiné à enregistrer " \
                    "les objets de Kassie n'a pas pu être ouvert : {}".format(
                    chemin_dest, io_err))
        else:
            pickler = pickle.Pickler(fichier_enr)
            pickler.dump(a_enregistrer)
        finally:
            if "fichier_enr" in locals():
                fichier_enr.close()
            self.enregistre_actuellement = False
            for classe, liste in objets_par_type.items():
                liste = [o for o in liste if o.e_existe]

    def enregistrer_periodiquement(self):
        """Cette méthode est appelée périodiquement pour enregistrer (pickle).

        On enregistre tous les objets dans la sauvegarde pickle.

        """
        importeur.diffact.ajouter_action("enregistrement", 60 * 60,
                self.enregistrer_periodiquement)
        if self.enregistre_actuellement:
            return

        t1 = time.time()
        self.enregistrer()
        t2 = time.time()
        print("Enregistrement fait en", t2 - t1)

    def charger(self):
        """Charge le fichier indiqué et retourne l'objet dépicklé"""
        if not importeur.sauvegarde:
            return

        global REP_ENRS
        chemin_dest = REP_ENRS + os.sep + "enregistrements.bin"
        try:
            fichier_enr = open(chemin_dest, 'rb')
        except IOError as io_err:
            self.logger.warning("Le fichier {} n'a pas pu être ouvert " \
                    ": {}".format(chemin_dest, io_err))
        else:
            unpickler = pickle.Unpickler(fichier_enr)
            try:
                rec = unpickler.load()
            except (EOFError, pickle.UnpicklingError):
                self.logger.warning("Le fichier {} n'a pas pu être " \
                        "chargé ".format(chemin_dest))
        finally:
            if "fichier_enr" in locals():
                fichier_enr.close()
            self.logger.info("{} objets récupérés".format(len(objets)))

    def ajouter_objet(self, objet):
        """Ajoute les objets à la file des enregistrements."""
        if self.mode == "mongo":
            self.mongo_file[id(objet)] = objet

    def detruire_objet(self, objet):
        """Détruit l'objet."""
        if self.mode == "mongo":
            nom = self.qualname(type(objet))
            if "_id" in objet.__dict__:
                _id = objet._id
                self.mongo_db[nom].remove(_id)
                if nom in self.mongo_objets:
                    enr = self.mongo_objets[nom]
                    if str(_id) in enr:
                        del enr[str(_id)]

    def charger_groupe(self, groupe):
        """Cette fonction retourne les objets d'un groupe.

        Le mode 'pickle' se base sur objets_par_type. Le mode 'mongo'
        récupère les collections et les fusionne (il peut y avoir
        plusieurs collections pour un seul groupe. Un groupe étant
        une classe, ses classes héritées sont également chargées.

        """
        if not importeur.sauvegarde:
            return []

        if not self.pret:
            raise RuntimeError("le supenr n'est pas prêt à charger un groupe")

        objets = []
        if self.mode == "pickle":
            for cls in objets_par_type.keys():
                if issubclass(cls, groupe):
                    objets.extend(objets_par_type[cls])
        else:
            for cls in classes_base.values():
                if issubclass(cls, groupe):
                    objets.extend(self.mongo_charger_collection(cls))

        return objets

    def charger_unique(self, groupe):
        """Cette fonction retourne l'objet unique correspondant.

        Si plusieurs objets uniques semblent exister du même type, retourne
        le premier à avoir été chargé.

        """
        if not importeur.sauvegarde:
            return None

        if not self.pret:
            raise RuntimeError("le supenr n'est pas prêt à charger un groupe")

        if self.mode == "pickle":
            return objets_par_type.get(groupe, [None])[0]
        else:
            objets = self.charger_groupe(groupe)
            if len(objets) == 0:
                return None
            elif len(objets) > 1:
                print("Plus d'un objet unique du même type: {}".format(objets))

            return objets[0]

    def mongo_charger_collection(self, classe):
        """Charge la collection correspondante.

        Les objets chargés sont retournés sous la forme d'une liste.
        Les objets None (qui n'ont pas pu être chargés) ne sont pas ajoutés.

        """
        nom = self.qualname(classe)
        objets = []
        valeurs = list(self.mongo_db[nom].find())
        self.mongo_nb_requetes += 1
        self.logger.debug("  o({}) r({}) col({}) l({})".format(
                sum(len(objets) for objets in self.mongo_objets.values()),
                self.mongo_nb_requetes, nom, len(valeurs)))
        for attributs in valeurs:
            _id = attributs["_id"]
            objet = self.mongo_charger_objet(classe, _id, attributs=attributs)
            if objet is not None:
                objets.append(objet)

        return objets

    def finir_charger(self):
        """Cette méthode finit de charger les objets différés.

        À ce stade, tous les objets devraient avoir été récupérés, mais
        pas nécessairement construits. Cette méthode permet de finir
        l'enregistrement.

        """
        if self.mode == "mongo":
            i = 1
            while self.mongo_differe:
                self.logger.info("Passage {}, {} / {} objets finis".format(
                        len(self.mongo_differe), sum(len(objets) for \
                        objets in self.mongo_objets.values())))
                self.mongo_charger_differe()
                i += 1

    def mongo_charger_objet(self, classe, _id, differer=False,
            attributs=None):
        """Récupère un objet individuel.

        Cette méthode va :
            Interroger les objets déjà chargés
            Ou charger l'objet depuis MongoDB

        """
        nom = self.qualname(classe)
        sid = str(_id)
        charges = self.mongo_objets.get(nom, {})
        objet = charges.get(sid)
        if objet is not None and objet._statut:
            return objet

        collection = self.mongo_db[nom]
        if objet is None:
            try:
                objet = classe(*classe.__getnewargs__(classe))
            except TypeError as err:
                self.logger.fatal("Erreur lors du chargement de {} : " \
                        "{}".format(nom, str(err)))
                sys.exit(1)

            object.__setattr__(objet, "_statut", 0)
            enr = self.mongo_objets.get(nom, {})
            enr[sid] = objet
            self.mongo_objets[nom] = enr

        # Traitement des attributs
        if differer:
            self.mongo_differe[sid] = objet
            return objet

        if attributs is None:
            attributs = collection.find_one(_id)
            self.mongo_nb_requetes += 1

        if attributs is None:
            del enr[sid]
            return None

        self.mongo_charger_dictionnaire(attributs, nom, sid)

        for transform in transforms:
            transform.transform_outgoing(attributs, collection)

        # On retire les attributs directs référençant des objets
        # qui seront remplacés. Ce code évite les filtres de mémoire,
        # sans les empêcher complètement.
        for cle, valeur in tuple(attributs.items()):
            if isinstance(valeur, BaseObj) \
                    and isinstance(getattr(objet, cle, None), BaseObj):
                getattr(objet, cle).detruire()

        objet.__setstate__(attributs)
        objet._construire()
        if self.initial:
            self.mongo_temporaire[id(objet)] = (objet, objet.__dict__.copy())

        return objet

    def mongo_tout_charger(self):
        """On charge toutes les collections."""
        self.logger.info("MongoDB : récupération de tous les objets...")
        i = 0
        taille = len(classes_base)
        pct = 0
        for nom, classe in classes_base.items():
            i += 1
            t_pct = round(i * 100 / taille)
            if t_pct != pct:
                pct = t_pct
                if pct % 5 == 0:
                    self.logger.info("{:> 3}% des collections chargées".format(
                            pct))

            self.mongo_charger_collection(classe)

        self.logger.info("MongoDB : ... fin de la récupération")

    def mongo_charger_dictionnaire(self, dictionnaire, col, sid, attr=""):
        """Charge les informations d'un dictionnaire."""
        for cle, valeur in tuple(dictionnaire.items()):
            tattr = attr
            if tattr:
                tattr += "."
            tattr += cle

            if "*DLS*" in cle:
                del dictionnaire[cle]
                cle = cle.replace("*DLS*", "$")
                dictionnaire[cle] = valeur
            elif cle.startswith("ObjectId("):
                del dictionnaire[cle]
                cle = cle[9:-1]
                nom, _id = cle.split(",")
                classe = classes_base[nom.replace("-", ".")]
                cle = self.mongo_charger_objet(classe, ObjectId(_id),
                        differer=True)
                if cle is None:
                    self.logger.warning("Erreur de linkage {}-{}.{}={}-" \
                            "{}".format(col, sid, tattr, nom, str(_id)))

                dictionnaire[cle] = valeur
            elif cle.startswith("(") or cle.startswith("["):
                del dictionnaire[cle]
                cle = literal_eval(cle)
                dictionnaire[cle] = valeur

            if isinstance(valeur, list) and len(valeur) == 2 and \
                    isinstance(valeur[0], str) and isinstance(valeur[1],
                    ObjectId):
                nom, _id = valeur
                classe = classes_base[valeur[0]]
                objet = self.mongo_charger_objet(classe, _id, differer=True)
                dictionnaire[cle] = objet
                if valeur is None:
                    self.logger.warning("Erreur de linkage {}-{}.{}={}-" \
                            "{}".format(col, sid, tattr, nom, str(_id)))

            elif isinstance(valeur, list):
                self.mongo_charger_liste(valeur, col, sid, tattr)
            elif isinstance(valeur, dict):
                self.mongo_charger_dictionnaire(valeur, col, sid, tattr)

    def mongo_charger_liste(self, liste, col, sid, attr):
        """Charge la liste."""
        copie = []
        for valeur in liste:
            if isinstance(valeur, str) and valeur.startswith("ObjectId("):
                valeur = valeur[9:-1]
                nom, _id = valeur.split(",")
                classe = classes_base[nom.replace("-", ".")]
                valeur = self.mongo_charger_objet(classe, ObjectId(_id),
                        differer=True)
                if valeur is None:
                    self.logger.warning("Erreur de linkage {}-{}.{}={}-" \
                            "{}".format(col, sid, tattr, nom, str(_id)))

                copie.append(valeur)
            elif isinstance(valeur, list) and len(valeur) == 2 and \
                    isinstance(valeur[0], str) and isinstance(valeur[1],
                    ObjectId):
                nom, _id = valeur
                classe = classes_base[valeur[0]]
                objet = self.mongo_charger_objet(classe, _id, differer=True)
                if objet is None:
                    self.logger.warning("Erreur de linkage {}-{}.{}={}-" \
                            "{}".format(col, sid, attr, nom, str(_id)))

                copie.append(objet)
            elif isinstance(valeur, list):
                self.mongo_charger_liste(valeur, col, sid, attr)
                copie.append(valeur)
            elif isinstance(valeur, dict):
                self.mongo_charger_dictionnaire(valeur, col, sid, attr)
                copie.append(valeur)
            else:
                copie.append(valeur)

        liste[:] = copie

    def mongo_charger_differe(self):
        """Charge tous les objets différés."""
        self.logger.debug("{} objets chargés contre {} différés".format(
                sum(len(objets) for objets in self.mongo_objets.values()),
                len(self.mongo_differe)))

        for sid, objet in tuple(self.mongo_differe.items()):
            _id = ObjectId(sid)
            if not sid in self.mongo_complets:
                classe = self.qualname(type(objet))
                self.mongo_charger_objet(type(objet), _id)
            del self.mongo_differe[sid]

    def mongo_premier_enregistrement(self):
        """Premier enregistrement des objets en MongoDB.

        Cet enregistrement est un peu particulier car on n'enregistre
        que les objets modifiés. Un objet récupéré en mémoire, en
        effet, se reconstruit et veut se réenregistrer aussitôt, malgré
        plusieurs verrous de sécurité. Il n'est pas nécessaire
        d'enregistrer tout l'univers une seconde après l'avoir chargé,
        bien que certains objets soient effectivement à jour. Il devient
        ainsi nécessaire d'enregistrer les objets qui ont été modifiés
        depuis leur chargement.

        """
        avant = len(self.mongo_file)
        self.initial = False
        for ident, (objet, attributs) in tuple(self.mongo_temporaire.items()):
            if objet.__dict__ == attributs:
                if ident in self.mongo_file:
                    del self.mongo_file[ident]

        # On retire les objets créés mais à détruire tout de suite
        for ident, objet in tuple(self.mongo_file.items()):
            if not objet._statut or not objet.e_existe:
                del self.mongo_file[ident]

        self.logger.info("Enregistrement MongoDB initial : {} objets " \
                "à enregistrer contre {} prévus".format(len(
                self.mongo_file), avant))

        self.mongo_enregistrer_file()
        self.logger.info("Fin de l'enregistrement initial.")
        if hasattr(importeur, "stat"):
            importeur.stat.stats.reset_watch_dog()

    def mongo_enregistrer_file(self, rappel=True, debug=False):
        """Enregistre la file des objets (mongo).

        Les objets à enregistrer sont soit à insérer, soit à
        modifier.

        """
        logger = self.logger
        if not debug:
            debug = self.mongo_debug

        if rappel:
            importeur.diffact.ajouter_action("enregistrement", 5,
                    self.mongo_enregistrer_file)


        t1 = time.time()
        reste = []
        for objet in self.mongo_file.values():
            if not objet._statut:
                continue

            if debug:
                nom = self.qualname(type(objet))
                self.logger.debug("  Enregistrement de {}".format(nom))

            second, attributs = self.extraire_attributs(objet)
            self.mongo_enregistrer_objet(objet, attributs)
            if second:
                reste.append(objet)

        for objet in reste:
            second, attributs = self.extraire_attributs(objet)
            self.mongo_enregistrer_objet(objet, attributs)

        self.mongo_file.clear()
        t2 = time.time()
        self.mongo_debug = False
        return t2 - t1

    def mongo_enregistrer_objet(self, objet, attributs):
        """Enregistre l'objet dans une base MongoDB.

        Si l'objet n'existe pas, l'insert. Sinon le met à jour.

        """
        if not importeur.sauvegarde:
            return

        nom = self.qualname(type(objet))
        collection = self.mongo_db[nom]
        for transform in transforms:
            transform.transform_incoming(attributs, collection)

        if "_id" in attributs: # L'objet existe
            _id = attributs.pop("_id")
            if not attributs.get("e_existe"):
                self.mongo_db[nom].remove(objet._id)
            else:
                try:
                    collection.update({"_id": _id}, attributs)
                except InvalidDocument as err:
                    print(err, objet, type(objet), attributs)
                    sys.exit(1)
                else:
                    self.mongo_table.append((time.time(), nom, str(_id)))
        else:
            if not attributs.get("e_existe"):
                return

            try:
                _id = collection.insert(attributs)
            except InvalidDocument as err:
                print(err, objet, type(objet), attributs)
                sys.exit(1)
            else:
                self.mongo_table.append((time.time(), nom, str(_id)))

            objet._id = _id
            enr = self.mongo_objets.get(nom, {})
            enr[str(_id)] = objet
            self.mongo_objets[nom] = enr

    def extraire_attributs(self, objet):
        """Méthode utilisée par MongoDB pour extraire les attributs d'un objet.

        On s'inspire de objet.__dict__ pour lister les attributs
        et leur valeur respective. Cependant, on retourne second.

        Le booléen second est utilisé quand l'un des attributs de
        l'objet fait référence à un autre objet BaseObj. Dans ce cas,
        on enregistre le nom de sa collection et son ObjetID.
        Cependant, si l'objet cible n'a pas encore été enregistré,
        il n'a pas d'_id. Il faut donc enregistrer le premier objet
        sans cet attribut, puis enregistrer le second, puis réenregistrer
        le premier qui cette fois peut référencer le second en attribut.

        """
        if isinstance(objet, dict):
            attributs = objet
        else:
            attributs = dict(objet.__getstate__())

        second = False
        for cle, valeur in tuple(attributs.items()):
            # Transformation des clés
            if isinstance(cle, BaseObj):
                del attributs[cle]
                if not "_id" in cle.__dict__:
                    second = True
                    continue

                nom = self.qualname(type(cle)).replace(".", "-")
                cle = cle._id
                cle = "ObjectId({},{})".format(nom, str(cle))
                attributs[cle] = valeur
            elif isinstance(cle, (tuple, list)):
                del attributs[cle]
                cle = str(cle)
                attributs[cle] = valeur
            elif isinstance(cle, (int, float)):
                del attributs[cle]
                cle = "(" + str(cle) + ")"
                attributs[cle] = valeur
            elif isinstance(cle, str):
                del attributs[cle]
                cle = cle.replace("$", "*DLS*")
                attributs[cle] = valeur

            if isinstance(valeur, BaseObj):
                if "_id" in valeur.__dict__:
                    attributs[cle] = (self.qualname(type(valeur)),
                    valeur._id)
                else:
                    del attributs[cle]
                    second = True
            elif isinstance(valeur, (list, tuple)):
                attributs[cle] = valeur = list(valeur)
                sous = self.extraire_liste(valeur)
                if sous:
                    second = True
            elif isinstance(valeur, dict):
                attributs[cle] = valeur = valeur.copy()
                sous, r = self.extraire_attributs(valeur)
                if sous:
                    second = True

        return second, attributs

    def extraire_liste(self, liste):
        """Extrait les valeurs de la liste."""
        copie = []
        second = False
        for valeur in liste:
            if isinstance(valeur, BaseObj):
                if "_id" in valeur.__dict__:
                    valeur = (self.qualname(type(valeur)), valeur._id)
                else:
                    second = True
                    continue
            elif isinstance(valeur, (list, tuple)):
                valeur = list(valeur)
                sous = self.extraire_liste(valeur)
                if sous:
                    second = True
                    continue
            elif isinstance(valeur, dict):
                valeur = dict(valeur)
                sous = self.extraire_attributs(valeur)
                if sous:
                    second = True
                    continue

            copie.append(valeur)

        liste[:] = copie
        return second

    @staticmethod
    def qualname(classe):
        return classe.__module__ + "." + classe.__name__
