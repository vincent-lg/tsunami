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


"""Fichier contenant le module primaire scripting."""

import inspect
import os
import re
from collections import OrderedDict
from datetime import datetime

from abstraits.module import *
from primaires.format.fonctions import format_nb, supprimer_accents
from .instruction import Instruction
from .boucle import Boucle
from .condition import Condition
from .affectation import Affectation
from .commentaire import Commentaire
from .action import Action, actions as lst_actions
from . import parser
from . import commandes
from . import masques
from .quete.quete import Quete
from .quete.etape import Etape
from .test import Test
from .editeurs.qedit import EdtQedit
from .editeurs.cmdedit import EdtCmdedit
from .editeurs.personnalise.presentation import EdtPresentation
from .config import *
from .constantes.aide import *
from .script import scripts
from .alerte import Alerte
from .commande_dynamique import CommandeDynamique
from .memoires import Memoires
from .structure import StructureComplete
from .editeur_personnalise import EditeurPersonnalise

class Module(BaseModule):

    """Cette classe contient les informations du module primaire scripting.

    Ce module gère le langage de script utilisé pour écrire des quêtes et
    personnaliser certains objets de l'univers. Il regroupe également les
    éditeurs et les objets gérant les quêtes.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "scripting", "primaire")
        self.logger = importeur.man_logs.creer_logger("scripting",
                "scripting")
        self.cfg_exportation = None
        self.memoires = None
        self.a_charger = []
        self.fonctions = {}
        self.actions = {}
        self.commandes = {}
        self.quetes = {}
        self.alertes = {}
        self.commandes_dynamiques = {}
        self.sujets_aides = {
            "syntaxe": syntaxe,
        }
        self.execute_test = []
        self.alarmes = {}
        self.structures = {}
        self.editeurs = {}

        # Statistiques
        self.tps_actions = 0.003
        self.tps_fonctions = 0.002
        self.exc_actions = {}
        self.exc_fonctions = {}
        self.nb_exc_actions = 0
        self.nb_exc_fonctions = 0
        self.moy_actions = 0
        self.nb_moy_actions = 0
        self.moy_fonctions = 0
        self.nb_moy_fonctions = 0
        self.tps_script = 0.15
        self.scripts_gourmands = {}

        # Scriptables
        self.valeurs = {}

        # Paramètres te;poraires
        self.presse_papier = {}

    @property
    def commandes_dynamiques_sa(self):
        """Retourne les commandes dynamiques {cle_sans_accent: commande}."""
        cmds = {}
        for cmd in self.commandes_dynamiques.values():
            cmds[supprimer_accents(cmd.nom_francais)] = cmd

        return cmds

    def config(self):
        """Configuration du module."""
        self.a_charger.append(self)
        self.cfg_exportation = importeur.anaconf.get_config("exportation", \
                "scripting/exportation.cfg", "config exportation",
                cfg_exportation)

        # Création des hooks
        importeur.hook.ajouter_hook("scripting:changer_nom_objet",
                "Hook appelé quand l'action changer_nom est exécutée.")
        importeur.hook.ajouter_hook("scripting:deplacer_alea_personnage",
                "Hook appelé quand l'action deplacer_alea est exécutée.")
        BaseModule.config(self)

    def init(self):
        """Initialisation"""
        # Récupération de la mémoire du scripting
        self.memoires = self.importeur.supenr.charger_unique(Memoires)
        if self.memoires is None:
            self.memoires = Memoires()

        # Chargement des actions
        self.charger_actions()
        self.charger_fonctions()
        if self.cfg_exportation.active:
            self.ecrire_documentation()

        # Chargement des quêtes
        quetes = self.importeur.supenr.charger_groupe(Quete)
        for quete in quetes:
            if quete.parent is None:
                self.quetes[quete.cle] = quete

        # Chargement des étapes et tests
        etapes = self.importeur.supenr.charger_groupe(Etape)
        tests = self.importeur.supenr.charger_groupe(Test)

        # Chargement des alertes
        alertes = self.importeur.supenr.charger_groupe(Alerte)
        for alerte in alertes:
            self.alertes[alerte.no] = alerte

        # Chargement des commandes dynamiques
        commandes_dynamiques = importeur.supenr.charger_groupe(
                CommandeDynamique)
        for cmd in commandes_dynamiques:
            self.commandes_dynamiques[cmd.nom_francais] = cmd
            cmd.ajouter()

        # Chargement des structures
        structures = self.importeur.supenr.charger_groupe(StructureComplete)
        for structure in structures:
            self.ajouter_structure(structure)

        # Chargement des eurs
        editeurs = self.importeur.supenr.charger_groupe(EditeurPersonnalise)
        for editeur in editeurs:
            self.ajouter_editeur(editeur)

        if alertes:
            Alerte.no_actuel = max(a.no for a in alertes)

        # On lie la méthode informer_alertes avec l'hook joueur_connecte
        # La méthode informer_alertes sera ainsi appelée quand un joueur
        # se connecte
        self.importeur.hook["joueur:connecte"].ajouter_evenement(
                self.informer_alertes)

        # Création de l'action différée pour nettoyer les mémoires
        importeur.diffact.ajouter_action("eff_memoires", 90,
                self.nettoyer_memoires)

        # Hooks
        self.importeur.hook["stats:infos"].ajouter_evenement(
                self.stats_scripting)


        # Valeurs
        self.valeurs.update({
                "etendue": importeur.salle.etendues,
                "objet": importeur.objet._objets,
                "prototype d'objet": importeur.objet._prototypes,
                "pnj": importeur.pnj._PNJ,
                "prototype de pnj": importeur.pnj._prototypes,
                "salle": importeur.salle._salles,
                "zone": importeur.salle._zones,
        })

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.dyncom.CmdDyncom(),
            commandes.editeur.CmdEditeur(),
            commandes.qedit.CmdQedit(),
            commandes.scripting.CmdScripting(),
            commandes.structure.CmdStructure(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs 'qedit' et 'cmdedit'
        self.importeur.interpreteur.ajouter_editeur(EdtQedit)
        self.importeur.interpreteur.ajouter_editeur(EdtCmdedit)
        self.importeur.interpreteur.ajouter_editeur(EdtPresentation)

    def preparer(self):
        """Préparation du module.

        * On initialise les scripts.
        * On ajoute les commandes dynamiques.

        """
        for script in scripts:
            script.init()

    def charger_actions(self):
        """Chargement automatique des actions.

        On parcourt tous les modules dans self.a_charger.

        """
        for module in self.a_charger:
            # Elles se trouvent dans le sous-répertoire actions
            chemin = module.chemin + os.sep + "actions"
            chemin_py = module.chemin_py + ".actions"
            for nom_fichier in os.listdir(chemin):
                if not nom_fichier.startswith("_") and \
                        nom_fichier.endswith(".py"):
                    nom_module = nom_fichier[:-3]
                    chemin_py_mod = chemin_py + ".{}".format(nom_module)
                    action = __import__(chemin_py_mod)
                    action = getattr(getattr(getattr(getattr(action,
                            module.nom), "actions"), nom_module),
                            "ClasseAction")
                    action.nom = nom_module
                    action._parametres_possibles = OrderedDict()
                    action.init_types()
                    action.convertir_types()
                    lst_actions[nom_module] = action
                    self.actions[nom_module] = action

    def charger_fonctions(self):
        """Chargement automatique des fonctions.

        On charge les modules dans self.a_charger.

        """
        for module in self.a_charger:
            # Elles se trouvent dans le sous-répertoire fonctions
            chemin = module.chemin + os.sep + "fonctions"
            chemin_py = module.chemin_py + ".fonctions"
            for nom_fichier in os.listdir(chemin):
                if not nom_fichier.startswith("_") and \
                        nom_fichier.endswith(".py"):
                    nom_module = nom_fichier[:-3]
                    chemin_py_mod = chemin_py + ".{}".format(nom_module)
                    fonction = __import__(chemin_py_mod)
                    fonction = getattr(getattr(getattr(getattr(fonction,
                            module.nom), "fonctions"), nom_module),
                            "ClasseFonction")
                    fonction.nom = nom_module
                    fonction._parametres_possibles = OrderedDict()
                    fonction.init_types()
                    fonction.convertir_types()
                    self.fonctions[nom_module] = fonction

    def informer_alertes(self, personnage):
        """Informe le personnage si des alertes non résolues sont à lire.

        Ce message n'est envoyé que si le personnage est immortel.

        """
        if personnage.est_immortel() and self.alertes:
            msg = format_nb(len(self.alertes),
                    "|rg|{nb} alerte{s} non résolue{s}.|ff|", fem=True)
            personnage << msg

    def get_objet(self, identifiant):
        """Récupère l'objet depuis son identifiant.

        Sont successivement testées :
        -   les salles

        """
        return self.importeur.salle[identifiant]

    def get_commande_dynamique(self, nom):
        """Retourne la commande dynamique correspondante au nom.

        Le nom peut être avec ou sans accent.

        Si la commande dynamique n'est pas trouvée, lève une exception
        KeyError.

        """
        return self.commandes_dynamiques_sa[nom]

    def creer_commande_dynamique(self, nom_francais, nom_anglais):
        """Crée et ajoute une commande dynamique."""
        commande = CommandeDynamique(nom_francais, nom_anglais)
        commande.ajouter()
        self.commandes_dynamiques[nom_francais] = commande
        return commande

    def creer_structure(self, nom):
        """Crée une structure complète, c'est-à-dire enregistrable."""
        structure = StructureComplete(nom)
        return self.ajouter_structure(structure)

    def ajouter_structure(self, structure):
        """Ajout d'une structure complète.

        On en profite pour vérifier si la sstructure à un ID valide,
        et sinon, on en cherche un.

        """
        nom = structure.structure
        groupe = self.structures.get(nom, {})
        if groupe:
            id_libre = max(s.id for s in groupe.values()) + 1
        else:
            id_libre = 1

        if structure.id == 0:
            structure.id = id_libre

        if structure.id in groupe:
            print(groupe)
            raise ValueError("La structure {} d'ID {} existe déjà".format(
                    nom, structure.id))

        groupe[structure.id] = structure
        if nom not in self.structures:
            self.structures[nom] = groupe

        return structure

    def supprimer_structure(self, structure):
        """Supprime la structure indiquée."""
        groupe = self.structures[structure.structure]
        del groupe[structure.id]
        structure.detruire()

    def creer_editeur(self, structure):
        """Crée un éditeur sur le nom de la structure."""
        if structure in self.editeurs:
            raise ValueError("L'éditeur pour la structure {} existe " \
                    "déjà".format(repr(structure)))

        editeur = EditeurPersonnalise(structure)
        self.ajouter_editeur(editeur)
        return editeur

    def ajouter_editeur(self, editeur):
        """Ajoute un éditeur personnalisé."""
        structure = editeur.structure
        if structure in self.editeurs:
            raise ValueError("L'éditeur pour la structure {} existe " \
                    "déjà".format(repr(structure)))

        self.editeurs[structure] = editeur

    def supprimer_editeur(self, structure):
        """Supprime l'éditeur personnalisé indiqué."""
        self.editeurs.pop(structure).detruire()

    def ecrire_documentation(self):
        """Écrit la documentation disponible au format Dokuwiki.

        Deux fichiers de documentation sont écrits :
            La documentation des actions
            La documentation des fonctions

        """
        msg = "====== Liste des actions disponibles :======\n\n" \
                "Ce document, __automatiquement généré__, " \
                "décrit la liste des actions disponibles dans le " \
                "scripting du moteur **Tsunami**.\n"
        for action in sorted(self.actions.values(), key=lambda a: a.nom):
            nom = action.nom
            msg += "\n===== " + action.nom + " =====\n\n"
            msg += inspect.getdoc(action) + "\n"
            for methode in action._parametres_possibles.values():
                try:
                    args = " ".join(inspect.getargspec(methode).args)
                except ValueError:
                    args = ""
                args = args.replace(", variables)", ")")
                msg += "\n==== " + action.nom + " " + args + " ====\n\n"
                msg += inspect.getdoc(methode) + "\n"

        chemin_actions = self.cfg_exportation.chemin_doc_actions
        if os.path.exists(chemin_actions) and not os.access(chemin_actions,
                os.W_OK):
            print("Droits d'écriture refusés sur le chemin {}".format(
                    chemin_actions))
        else:
            fichier = open(chemin_actions, 'w')
            fichier.write(msg)
            fichier.close()

        msg = "====== Liste des fonctions disponibles :======\n\n" \
                "Ce document, __automatiquement généré__, " \
                "décrit la liste des fonctions disponibles dans le " \
                "scripting du moteur **Tsunami**.\n"
        for fonction in sorted(self.fonctions.values(), key=lambda f: f.nom):
            nom = fonction.nom
            msg += "\n===== " + nom + " =====\n\n"
            msg += inspect.getdoc(fonction) + "\n"
            for methode in fonction._parametres_possibles.values():
                args = ", ".join(inspect.getargspec(methode).args)
                args = args.replace(", variables)", ")")
                msg += "\n==== " + nom + "(" + args + ") ====\n\n"
                msg += inspect.getdoc(methode) + "\n"

        chemin_fonctions = self.cfg_exportation.chemin_doc_fonctions
        if os.path.exists(chemin_fonctions) and not os.access(chemin_fonctions,
                os.W_OK):
            print("Droits d'écriture refusés sur le chemin {}".format(
                    chemin_fonctions))
        else:
            fichier = open(chemin_fonctions, 'w')
            fichier.write(msg)
            fichier.close()

    def aide_action(self, arguments):
        """Retourne l'aide de l'action."""
        arguments = arguments.strip()
        nom_action = action = no = methode = None
        if arguments:
            arguments = arguments.split(" ")
            nom_action = arguments[0]
            if len(arguments) >= 2:
                no = arguments[1]
                try:
                    no = int(no)
                    assert no >= 1
                except (ValueError, AssertionError):
                    return "|err|Ce numéro est invalide.|ff|"
                    return

        if nom_action:
            # On cherche l'action
            try:
                action = self.actions[nom_action]
            except KeyError:
                return "|err|L'action {} est inconnue.|ff|".format(
                        nom_action)

            if no:
                try:
                    methode = action.get_methode(no - 1)
                except IndexError:
                    return "|err|Ce numéro est invalide.|ff|"

        # Affichage
        if methode:
            # On affiche l'aide de la méthode
            nom = action.nom
            try:
                args = " ".join(inspect.getargspec(methode).args)
            except ValueError:
                args = ""
            args = args.replace(" variables", "")
            doc = inspect.getdoc(methode)
            return "Action {} |vr|{}|ff| :\n{}".format(nom, args, doc)
        elif action:
            # Une action est précisée mais pas de méthode
            nom = action.nom
            doc = inspect.getdoc(action).split("\n")
            resume = doc[0]
            description = "\n".join(doc[1:])
            doc_methodes = []
            for i, methode in enumerate(action._parametres_possibles.values()):
                try:
                    args = " ".join(inspect.getargspec(methode).args)
                except ValueError:
                    args = ""
                args = args.replace(" variables", "")
                doc_methodes.append("{}. |vr|{}|ff|".format(i + 1, args))

            doc = "\n".join(doc_methodes)
            return "Action |ent|{}|ff| ({}){}\nUsages :\n{}".format(
                    nom, resume[0].lower() + resume[1:-1], description, doc)
        else:
            # Aucune action n'est précisée, on affiche la liste
            actions = sorted(self.actions.values(),
                    key=lambda a: a.nom.lower())
            lignes = []
            for action in actions:
                nom = action.nom
                doc = inspect.getdoc(action).split("\n")
                resume = doc[0]
                lignes.append("|ent|{}|ff| : {}".format(nom,
                        resume[0].lower() + resume[1:-1]))

            lignes = "  " + "\n  ".join(lignes)
            return \
                "Ci-dessous se trouve la liste des actions existantes.\n" \
                "Pour obtenir de l'aide sur une action, entrez " \
                "|cmd|/?a action|ff| ; pour obtenir de\n" \
                "l'aide sur un des usages possibles " \
                "de l'action, entrez |cmd|/?a action numero|ff|.\n\n" \
                "{}".format(lignes)

    def aide_fonction(self, arguments):
        """Affiche l'aide de la fonction."""
        arguments = arguments.strip()
        nom_fonction = fonction = no = methode = None
        if arguments:
            arguments = arguments.split(" ")
            nom_fonction = arguments[0]
            if len(arguments) >= 2:
                no = arguments[1]
                try:
                    no = int(no)
                    assert no >= 1
                except (ValueError, AssertionError):
                    return "|err|Ce numéro est invalide.|ff|"

        if nom_fonction:
            # On cherche la fonction
            try:
                fonction = self.fonctions[nom_fonction]
            except KeyError:
                return "|err|La fonction {} est inconnue.|ff|".format(
                        nom_fonction)

            if no:
                try:
                    methode = fonction.get_methode(no - 1)
                except IndexError:
                    return "|err|Ce numéro est invalide.|ff|"

        # Affichage
        if methode:
            # On affiche l'aide de la méthode
            nom = fonction.nom
            t_args = inspect.getargspec(methode)
            args = "|ff|, |vr|".join(t_args.args)
            doc = inspect.getdoc(methode)
            return "Fonction {}(|vr|{}|ff|) :\n{}".format(nom,
                    args, doc)
        elif fonction:
            # Une fonction est précisée mais pas de méthode
            nom = fonction.nom
            doc = inspect.getdoc(fonction).split("\n")
            resume = doc[0]
            description = "\n".join(doc[1:])
            doc_methodes = []
            for i, methode in enumerate(fonction._parametres_possibles.values()):
                args = "|ff|, |vr|".join(inspect.getargspec(methode).args)
                doc_methodes.append("{:>2}. (|vr|{}|ff|)".format(i + 1, args))

            doc = "\n".join(doc_methodes)
            return "Fonction |ent|{}|ff| ({}){}\nUsages :\n{}".format(
                    nom, resume[0].lower() + resume[1:-1], description, doc)
        else:
            # Aucune fonction n'est précisée, on affiche la liste
            fonctions = \
                    sorted(self.fonctions.values(),
                    key=lambda f: f.nom.lower())
            lignes = []
            for fonction in fonctions:
                nom = fonction.nom
                doc = inspect.getdoc(fonction).split("\n")
                resume = doc[0]
                lignes.append("|ent|{}|ff| : {}".format(nom,
                        resume[0].lower() + resume[1:-1]))

            lignes = "  " + "\n  ".join(lignes)
            return \
                "Ci-dessous se trouve la liste des fonctions existantes.\n" \
                "Pour obtenir de l'aide sur une fonction, entrez " \
                "|cmd|/?f fonction|ff| ; pour obtenir de\nl'aide sur un des " \
                "usages possibles " \
                "de la fonction, entrez |cmd|/?f fonction numero|ff|.\n\n" \
                "{}".format(lignes)

    def nettoyer_memoires(self):
        """Nettoie périodiquement les mémoires."""
        importeur.diffact.ajouter_action("eff_memoires", 60,
                self.nettoyer_memoires)
        mtn = datetime.now()
        for cle, entrees in list(self.memoires._a_detruire.items()):
            script = getattr(cle, "script", None)
            evenement = script.evenements.get("effacer_memoire") if \
                    script else None

            for valeur, moment in list(entrees.items()):
                if moment <= mtn:
                    del self.memoires._a_detruire[cle][valeur]
                    if cle in self.memoires and valeur in self.memoires[cle]:
                        valeur_memoire = self.memoires[cle][valeur]
                        del self.memoires[cle][valeur]
                        if evenement:
                            variables = evenement.deduire_variables(
                                    cle, nom=valeur, valeur=valeur_memoire)
                            evenement.executer(**variables)

            if not self.memoires._a_detruire[cle]:
                del self.memoires._a_detruire[cle]
            if not self.memoires[cle]:
                del self.memoires[cle]

    # Méthodes statistiques
    def cb_joueurs(self):
        """Retourne le nombre de joueurs enregistrés."""
        return len(importeur.connex.joueurs)

    def cb_joueurs_quete(self, cle_quete):
        """Retourne le nombre de joueurs ayant fait la quête."""
        joueurs = [j for j in importeur.connex.joueurs \
                if cle_quete in j.quetes and j.quetes[cle_quete].niveaux]
        return len(joueurs)

    def cb_joueurs_etape(self, cle_quete, etape):
        """Retourne le nombre de joueurs ayant fait la quête à ce niveau.

        La quête doit être précisée sous la forme d'une clé de
        quête et le niveau sous la forme d'un tuple ((1, 1, 2)
        par exemple).

        """
        joueurs = [j for j in importeur.connex.joueurs \
                if cle_quete in j.quetes and etape in \
                j.quetes[cle_quete].niveaux]
        return len(joueurs)

    def alarme_existe(self, personnage, alarme):
        """Retourne True si l'alarme existe."""
        alarmes = self.alarmes.get(personnage, [])
        return alarme in alarmes

    def ecrire_alarme(self, personnage, alarme):
        """Écrit l'alarme."""
        if personnage not in self.alarmes:
            self.alarmes[personnage] = []

        if alarme not in self.alarmes[personnage]:
            self.alarmes[personnage].append(alarme)

    def supprimer_alarme(self, personnage, alarme):
        """Supprime l'alarme."""
        if personnage not in self.alarmes:
            return

        while alarme in self.alarmes[personnage]:
            self.alarmes[personnage].remove(alarme)

    def stats_scripting(self, infos):
        """Ajoute les stats concernant le scripting."""
        moy_actions = str(round(self.moy_actions, 3)).replace(".", ",")
        moy_fonctions = str(round(self.moy_fonctions, 3)).replace(".", ",")
        tps_actions = str(round(self.tps_actions, 3)).replace(".", ",")
        tps_fonctions = str(round(self.tps_fonctions, 3)).replace(".", ",")
        tps_script = str(round(self.tps_script, 3)).replace(".", ",")
        msg = "|tit|Scripting :|ff|"
        msg += "\n  Actions exécutées : {} en {} " \
                "secondes".format(self.nb_moy_actions, moy_actions)
        msg += "\n  Actions ayant mis plus de {} secondes " \
                "pour s'exécuter : {}".format(tps_actions, self.nb_exc_actions)
        if self.exc_actions:
            msg += "\n  "
            i = 0
            for nom, tps in sorted(self.exc_actions.items(), \
                    key=lambda c: c[1], reverse=True):
                tps = str(round(tps, 5)).replace(".", ",")
                msg += "  {} ({}s)".format(nom, tps)
                i += 1
                if i >= 5:
                    break
        msg += "\n  Fonctions exécutées : {} en {} " \
                "secondes".format(self.nb_moy_fonctions, moy_fonctions)
        msg += "\n  Fonctions ayant mis plus de {} secondes " \
                "pour s'exécuter : {}".format(tps_fonctions,
                self.nb_exc_fonctions)
        if self.exc_fonctions:
            msg += "\n  "
            i = 0
            for nom, tps in sorted(self.exc_fonctions.items(), \
                    key=lambda c: c[1], reverse=True):
                tps = str(round(tps, 5)).replace(".", ",")
                msg += "  {} ({}s)".format(nom, tps)
                i += 1
                if i >= 5:
                    break

        msg += "\n  Scripts ayant mis plus de {} secondes pour " \
                "s'exécuter : {}".format(tps_script,
                len(self.scripts_gourmands))
        i = 0
        for ligne, tps in sorted(self.scripts_gourmands.items(),
                key=lambda c: c[1], reverse=True):
            tps = str(round(tps, 3)).replace(".", ",")
            msg += "\n    {}s : {}".format(tps, ligne)
            i += 1
            if i >= 5:
                break

        infos.append(msg)
