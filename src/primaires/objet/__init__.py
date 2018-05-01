# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant le module primaire objet."""

from abstraits.module import *
from primaires.affection.personnage import AffectionPersonnage
from primaires.format.fonctions import format_nb, supprimer_accents
from . import types
from . import commandes
from . import editeurs
from . import masques
from . import cherchables
from .editeurs.oedit import EdtOedit
from .types import types as o_types
from .types.base import BaseType
from .objet import Objet
from .potions_vente import PotionsVente
from .nourritures_vente import NourrituresVente

class Module(BaseModule):

    """Cette classe contient les informations du module primaire objet.
    Ce module gère les objets de l'univers.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "objet", "primaire")
        self._prototypes = {}
        self._objets = {}
        self.cherchable_pr = None
        self.logger = importeur.man_logs.creer_logger(
                "objets", "objets")
        type(importeur).espace["prototypes_objets"] = self._prototypes
        type(importeur).espace["objets"] = self._objets

    def config(self):
        """Configuration du module."""
        importeur.commerce.types_services["objet"] = self._prototypes
        importeur.commerce.aides_types["objet"] = \
            "Ce service se contente, à l'achat, de faire apparaître " \
            "l'objet précisé sur\nle sol de la salle."
        importeur.commerce.types_services["potion"] = PotionsVente()
        importeur.commerce.aides_types["potion"] = \
            "Ce service permet de proposer à la vente des potions " \
            "dans des conteneurs.\nPour cela, précisé un couple sous la " \
            "forme |cmd|<conteneur>/<potion>|ff| (par exemple,\n|ent|chope/" \
            "biere|ff| pour une chope de bière."
        importeur.commerce.types_services["nourriture"] = NourrituresVente()
        importeur.commerce.aides_types["nourriture"] = \
            "Ce service permet la vente de nourriture dans des plats, " \
            "dans un restaurant\npar exemple. Pour cela, précisez un " \
            "conteneur de nourriture puis une liste\nd'aliments sous la " \
            "forme |cmd|<conteneur>/<al1>(+<al2>+<al3>...)|ff| (par " \
            "exemple,\n|ent|assiette/patate+tomate+carotte|ff| pour une " \
            "assiette contenant ces trois légumes).\nSi le poids de la liste " \
            "d'aliments que vous proposez est supérieur au poids\nmaximum du " \
            "conteneur, l'ajout du service ne fonctionnera pas."

        # Ajout des hooks
        importeur.hook.ajouter_hook("objet:doit_garder",
                "Hook appelé pour connaître les objets à ne pas détruire")
        importeur.hook.ajouter_hook("objet:peut_boire",
                "Hook appelé quand un personnage demande à boire.")

        # Ajout de l'état repas
        etat = self.importeur.perso.ajouter_etat("repas")
        etat.msg_refus = "Vous êtes en train de manger."
        etat.msg_visible = "mange ici"
        etat.act_autorisees = ["regarder", "bouger"]

        # Ajout des flags d'affection
        AffectionPersonnage.def_flags.ajouter("voit dans le noir", 8)

        BaseModule.config(self)

    def init(self):
        """Initialisation du module"""
        prototypes = self.importeur.supenr.charger_groupe(BaseType)
        for prototype in prototypes:
            self._prototypes[prototype.cle] = prototype

        nb_prototypes = len(prototypes)
        self.logger.info(format_nb(nb_prototypes, "{nb} prototype{s} " \
                "d'objet récupéré{s}"))

        objets = self.importeur.supenr.charger_groupe(Objet)
        for objet in objets:
            if objet.prototype:
                self._objets[objet.identifiant] = objet

        nb_objets = len(objets)
        self.logger.info(format_nb(nb_objets, "{nb} objet{s} récupéré{s}"))

        self.cherchable_pry = cherchables.prototype.CherchablePrototypeObjet

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.allumer.CmdAllumer(),
            commandes.boire.CmdBoire(),
            commandes.donner.CmdDonner(),
            commandes.eteindre.CmdEteindre(),
            commandes.jeter.CmdJeter(),
            commandes.manger.CmdManger(),
            commandes.oedit.CmdOedit(),
            commandes.olist.CmdOlist(),
            commandes.opurge.CmdOpurge(),
            commandes.ospawn.CmdOspawn(),
            commandes.porter.CmdPorter(),
            commandes.poser.CmdPoser(),
            commandes.prendre.CmdPrendre(),
            commandes.puiser.CmdPuiser(),
            commandes.remplir.CmdRemplir(),
            commandes.retirer.CmdRetirer(),
            commandes.vider.CmdVider(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout de l'éditeur 'oedit'
        self.importeur.interpreteur.ajouter_editeur(EdtOedit)

    def preparer(self):
        """Préparation du module."""
        if "cadavre" not in self._prototypes:
            self.creer_prototype("cadavre", "cadavre")
        if "boule_neige" not in self._prototypes:
            self.creer_prototype("boule_neige", "boule de neige")
        if "eau" not in self._prototypes:
            eau = self.creer_prototype("eau", "potion")
            eau.nom_singulier = "eau"
            eau.description.ajouter_paragraphe(
                    "L'eau est claire et semble fraîche.")
            eau.remplissant = 2
            eau.message_boit = "Vous buvez une gorgée d'eau qui vous " \
                    "rafraîchit agréablement le gosier."
            eau.poids_unitaire = 0.1
            eau.prix = 0

        # Nettoyage des objets existants sans lien
        existants = []
        for joueur in importeur.connex.joueurs:
            if joueur.equipement:
                existants.extend(joueur.equipement.objets_uniques)
        for pnj in importeur.pnj.PNJ.values():
            if pnj.equipement:
                existants.extend(pnj.equipement.objets_uniques)
        for salle in importeur.salle.salles.values():
            existants.extend(salle.objets_uniques)
            for decor in salle.decors:
                if hasattr(decor, "elements"):
                    existants.extend(list(decor.elements.values()))

        a_detruire = []
        for objet in importeur.objet.objets.values():
            objet.supprimer_inexistants()
            if objet not in existants:
                a_detruire.append(objet)

        a_detruire = [o for o in a_detruire if o and o.prototype]
        for a_garder in importeur.hook["objet:doit_garder"].executer():
            for objet in a_garder:
                if objet in a_detruire:
                    a_detruire.remove(objet)

        self.logger.info(format_nb(len(a_detruire), "{nb} objet{s} à " \
                "détruire"))
        types = {}
        for objet in a_detruire:
            type = objet.nom_type
            nb = types.get(type, 0)
            nb += 1
            types[type] = nb
            try:
                importeur.objet.supprimer_objet(objet.identifiant)
            except KeyError:
                objet.detruire()

        for nom, nombre in sorted(types.items(), key=lambda c: c[1], \
                reverse=True):
            self.logger.info("  Dont {} de type {}".format(nombre, nom))

        # Opérations de nettoyage cycliques
        importeur.diffact.ajouter_action("net_boule de neige", 60,
                self.nettoyage_cyclique, "boule de neige")
        self.nettoyage_lumieres()

        # Réinitialisation des scripts des prototypes
        for prototype in self._prototypes.values():
            prototype.etendre_script()

    @property
    def prototypes(self):
        return dict(self._prototypes)

    @property
    def objets(self):
        return dict(self._objets)

    @property
    def noms_types(self):
        """Retourne le nom des types d'objets actuels."""
        return [t.nom_type for t in o_types.values()]

    @property
    def types(self):
        """Retourne un dictionnaire des types."""
        return dict(o_types)

    @property
    def types_premier_niveau(self):
        """Retourne un dictionnaire des types du premier niveau."""
        return BaseType.types

    def get_type(self, nom_type):
        """Retourne, si trouvé, le type indiqué ou lève une KeyError.

        La recherche se fait indépendemment des majuscules, minuscules ou des
        accents.

        """
        nom_type = supprimer_accents(nom_type).lower()
        for type in self.types.values():
            if supprimer_accents(type.nom_type) == nom_type:
                return type

        raise KeyError("type {} introuvable".format(nom_type))

    def get_types_herites(self, nom_type):
        """Retourne le nom des types hérités.

        Cette méthode retourne une liste de noms de types hérités
        du type indiqué. Le type parent est également contenu dans
        la liste (le premier élément de la liste). Par exemple,
        un appel à cette méthode avec "nourriture" en paramètre retournera :
            ["nourriture", "fruit", "légume", "gâteau", ...]

        """
        def get_types(classe, types):
            """Fonction récursive appelée pour extraire les types enfants."""
            for nom, sous_classe in classe.types.items():
                types.append(nom)
                get_types(sous_classe, types)

        classe = self.get_type(nom_type)
        types = [classe.nom_type]
        get_types(classe, types)
        return types

    def get_prototypes_de_type(self, nom_type):
        """Retourne les prototypes d'objets de type indiqué ou descendants."""
        type = self.get_type(nom_type)
        return [p for p in self.prototypes.values() if isinstance(
                p, type)]

    def get_objets_de_type(self, nom_type):
        """Retourne les objets de type indiqué ou descendant."""
        type = self.get_type(nom_type)
        return [o for o in self.objets.values() if isinstance(
                o.prototype, type)]

    def creer_prototype(self, cle, nom_type="indéfini"):
        """Crée un prototype et l'ajoute aux prototypes existants"""
        if cle in self._prototypes:
            raise ValueError("la clé {} est déjà utilisée comme " \
                    "prototype".format(cle))

        cls_type = o_types[nom_type]
        prototype = cls_type(cle)
        self.ajouter_prototype(prototype)
        return prototype

    def ajouter_prototype(self, prototype):
        """Ajoute un prototype au dictionnaire des prototypes"""
        if prototype.cle in self._prototypes:
            raise ValueError("la clé {} est déjà utilisée comme " \
                    "prototype".format(prototype.cle))

        self._prototypes[prototype.cle] = prototype

    def supprimer_prototype(self, cle):
        """Supprime le prototype cle"""
        prototype = self._prototypes[cle]
        del self._prototypes[cle]
        prototype.detruire()

    def creer_objet(self, prototype):
        """Crée un objet depuis le prototype prototype.
        L'objet est ensuite ajouté à la liste des objets existants.

        """
        if not prototype.unique:
            return prototype

        objet = Objet(prototype)
        self.ajouter_objet(objet)
        objet.script["créé"].executer(objet=objet)
        return objet

    def ajouter_objet(self, objet):
        """Ajoute l'objet à la liste des objets"""
        if objet.identifiant in self._objets:
            raise ValueError("l'identifiant {} est déjà utilisé comme " \
                    "objet".format(objet.identifiant))

        self._objets[objet.identifiant] = objet

    def supprimer_objet(self, identifiant):
        """Supprime l'objet de la liste des objets"""
        try:
            objet = self._objets[identifiant]
        except KeyError:
            pass
        else:
            del self._objets[identifiant]
            objet.detruire()

    def essayer_supprimer_objet(self, objet):
        """Essaye de supprimer l'objet."""
        if not objet.unique:
            return

        try:
            self.supprimer_objet(objet.identifiant)
        except KeyError:
            objet.detruire()

    def nettoyage_cyclique(self, nom_type):
        """Nettoyage cyclique, appelé toutes les minutes."""
        importeur.diffact.ajouter_action("net_{}".format(nom_type), 60,
                self.nettoyage_cyclique, nom_type)
        boule_neige = o_types["boule de neige"]
        prototypes = [p for p in self.prototypes.values() if \
                isinstance(p, boule_neige)]
        objets = []
        for prototype in prototypes:
            objets.extend(prototype.objets)

        for objet in objets:
            objet.nettoyage_cyclique()

    def nettoyage_lumieres(self):
        """Nettoyage cyclique des lmuières."""
        importeur.diffact.ajouter_action("net_lumieres", 5,
                self.nettoyage_lumieres)
        prototypes = [p for p in self.prototypes.values() if \
                p.est_de_type("lumière")]
        objets = []
        for prototype in prototypes:
            objets.extend(prototype.objets)

        for objet in objets:
            objet.nettoyage_cyclique()
