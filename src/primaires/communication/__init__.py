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


"""Fichier contenant le module primaire communication."""

import datetime
from random import random

from vector import mag

from abstraits.module import *
from primaires.format.fonctions import *
from primaires.format.tableau import Tableau, CENTRE
from primaires.communication.config import cfg_com
from primaires.communication import masques
from primaires.communication import commandes
from primaires.perso.exceptions.stat import DepassementStat

from .editeurs.chedit import EdtChedit
from .editeurs.socedit import EdtSocedit
from .editeurs.medit import EdtMedit
from .editeurs.messagerie import EdtMessagerie

from .conversations import Conversations
from .orbes import Orbes
from .attitudes import Attitudes
from .attitude import INACHEVEE
from .canaux import Canaux
from .canal import *
from .boite_mail import BoiteMail
from .mudmail import *

class Module(BaseModule):

    """Classe représentant le module primaire 'communication'.

    Ce module gère toutes les communications entre clients (entre joueurs
    la plupart du temps). Il s'occupe également des canaux de communication,
    du mudmail et d'autres systèmes anodins.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "communication", "primaire")
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "communication", "communication")
        self.conv_logger = type(self.importeur).man_logs.creer_logger(
                "communication", "conversation")
        self.masques = []
        self.commandes = []
        self.conversations = None
        self.orbes = None
        self.attitudes = None
        self._canaux = None
        self.derniers_canaux = {}
        self.mails = None
        self.messages = {}
        self.orbes_choisis = {}

    def config(self):
        """Configuration du module"""
        self.cfg_com = type(self.importeur).anaconf.get_config("config_com", \
            "communication/config.cfg", "config communication", cfg_com)
        self.cfg_com._set_globales({
            "PRIVE": PRIVE,
            "MUET": MUET,
            "INVISIBLE": INVISIBLE,
            "IMM_AUTOCONNECT": IMM_AUTOCONNECT,
            "PERSO_AUTOCONNECT": PERSO_AUTOCONNECT,
            "BLOQUE": BLOQUE,
        })

        BaseModule.config(self)

    def init(self):
        """Initialisation du module"""
        self.conversations = self.importeur.supenr.charger_unique(Conversations)
        if self.conversations is None:
            self.conversations = Conversations()

        self.orbes = self.importeur.supenr.charger_unique(Orbes)
        if self.orbes is None:
            self.orbes = Orbes()

        # On récupère les attitudes
        attitudes = self.importeur.supenr.charger_unique(Attitudes)
        if attitudes is None:
            attitudes = Attitudes()
        self.attitudes = attitudes

        # On récupère les canaux
        canaux = self.importeur.supenr.charger_unique(Canaux)
        if canaux is None:
            canaux = Canaux()
        else:
            self.logger.info(format_nb(len(canaux),
                    "{nb} cana{x} de communication récupéré{s}"))
        self._canaux = canaux

        # On crée les canaux par défaut
        cfg_com = self.cfg_com
        for ligne in cfg_com.liste_canaux:
            nom_c = ligne[0]
            if not nom_c in self.canaux:
                self.ajouter_canal(nom_c, None)
                self.logger.info("Création du canal '{}'".format(nom_c))
                self.canaux[nom_c].clr = ligne[1]
                self.canaux[nom_c].flags = ligne[2]
        # Ajout du canal 'info'
        if not "info" in self.canaux:
            chan_info = self.ajouter_canal("info", None)
            self.logger.info("Création du canal 'info'")
            chan_info.clr = cfg_com.couleur_info
            chan_info.flags = MUET | PERSO_AUTOCONNECT
            chan_info.resume = cfg_com.resume_info

        # On récupère les mails
        mails = None
        mails = self.importeur.supenr.charger_unique(BoiteMail)
        if mails is None:
            mails = BoiteMail()
        else:
            self.logger.info(format_nb(len(mails),
                    "{nb} mudmail{s} récupéré{s}"))
        self.mails = mails

        # On lie la méthode joueur_connecte avec l'hook joueur_connecte
        # La méthode joueur_connecte sera ainsi appelée quand un joueur
        # se connecte
        self.importeur.hook["joueur:connecte"].ajouter_evenement(
                self.joueur_connecte)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes"""
        self.commandes = [
            commandes.attitudes.CmdAttitudes(),
            commandes.canaux.CmdCanaux(),
            commandes.chuchoter.CmdChuchoter(),
            commandes.cnvlog.CmdCnvlog(),
            commandes.crier.CmdCrier(),
            commandes.dire.CmdDire(),
            commandes.discuter.CmdDiscuter(),
            commandes.emote.CmdEmote(),
            commandes.historique.CmdHistorique(),
            commandes.messages.CmdMessages(),
            commandes.orbe.CmdOrbe(),
            commandes.parler.CmdParler(),
            commandes.repondre.CmdRepondre(),
            commandes.socedit.CmdSocedit(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(EdtChedit)
        self.importeur.interpreteur.ajouter_editeur(EdtSocedit)
        self.importeur.interpreteur.ajouter_editeur(EdtMedit)
        self.importeur.interpreteur.ajouter_editeur(EdtMessagerie)

    def preparer(self):
        """Préparation du module.

        Les actions suivantes sont effectuées au lancement du module :
            Nettoyage des orbes

        """
        self.orbes.nettoyer()

    @property
    def canaux(self):
        """Retourne les canaux existants"""
        return self._canaux

    @property
    def attitudes_jouables(self):
        """Retourne une liste les attitudes jouables"""
        try:
            cles = sorted([att for att in self.attitudes.keys()])
            ret = []
            for cle in cles:
                if self.attitudes[cle].statut != INACHEVEE:
                    ret.append(self.attitudes[cle])
        except KeyError:
            ret = []
        return ret

    def ajouter_canal(self, nom, auteur):
        """Ajoute un canal à la liste des canaux existants
        Retourne le canal créé.

        """
        self._canaux[nom] = Canal(nom, auteur, self._canaux)
        return self._canaux[nom]

    def supprimer_canal(self, nom):
        """Supprime le canal de la liste des canaux"""
        del self._canaux[nom]

    def rejoindre_ou_creer(self, personnage, arguments):
        """Connecte le joueur au canal passé en argument, ou le crée s'il
        n'existe pas.

        """
        if not arguments or arguments.isspace():
            personnage << "|err|Vous devez préciser un canal.|ff|"
            return
        nom_canal = arguments.split(" ")[0]
        if nom_canal in self.canaux:
            if personnage in self.canaux[nom_canal].connectes:
                personnage << "|err|Vous êtes déjà connecté à ce canal.|ff|"
                return
            self.canaux[nom_canal].rejoindre_ou_quitter(personnage)
        else:
            if not personnage.est_immortel():
                personnage << "|err|Ce canal n'existe pas.|ff|"
                return

            canal = self.ajouter_canal(nom_canal, personnage)
            personnage << "|att|Le canal {} a été créé.|ff|".format(nom_canal)
            canal.rejoindre_ou_quitter(personnage)

    def quitter_ou_detruire(self, personnage, arguments):
        """Déconnecte le joueur et détruit le canal s'il est vide"""
        if not arguments or arguments.isspace():
            personnage << "|err|Vous devez préciser un canal.|ff|"
            return
        nom_canal = arguments.split(" ")[0]
        if nom_canal not in self.canaux:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            return
        canal = self.canaux[nom_canal]
        if personnage not in canal.connectes:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            return
        if canal.flags & BLOQUE:
            personnage << "|err|Vous ne pouvez quitter ce canal.|ff|"
            return
        self.canaux[nom_canal].rejoindre_ou_quitter(personnage)
        res = "Vous avez bien quitté le canal {}.".format(nom_canal)
        if not self.canaux[nom_canal].connectes:
            del self.canaux[nom_canal]
            res += " Vide, il a été détruit."
        personnage << "|att|" + res + "|ff|"

    def immerger(self, personnage, arguments):
        """Immerge le personnage dans le canal choisi"""
        if not arguments or arguments.isspace():
            personnage << "|err|Vous devez préciser un canal.|ff|"
            return
        nom_canal = arguments.split(" ")[0]
        if nom_canal not in self.canaux:
            personnage << "|err|Le canal {} n'existe pas.|ff|".format(nom_canal)
            return
        canal = self.canaux[nom_canal]
        if personnage not in canal.connectes:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            return
        canal.immerger_ou_sortir(personnage)

    def dire_dernier_canal(self, personnage, arguments):
        """Envoie un message au dernier canal utilisé par personnage"""
        if not arguments or arguments.isspace():
            personnage << "Que voulez-vous dire ?"
            return
        if not personnage.nom in self.derniers_canaux:
            personnage << "|err|Vous n'avez utilisé aucun canal.|ff|"
            return
        dernier_canal = self.derniers_canaux[personnage.nom]
        if dernier_canal not in self.canaux:
            personnage << "|err|Le canal {} n'existe pas.|ff|".format(
                    dernier_canal)
            del self.derniers_canaux[personnage.nom]
            return
        canal = self.canaux[dernier_canal]
        if not personnage in canal.connectes:
            personnage << "|err|Vous n'êtes pas connecté au canal " \
                    "{}.|ff|".format(dernier_canal)
            return
        canal.envoyer(personnage, arguments)

    def dire_canal(self, personnage, arguments):
        """Envoie un message à un canal, de la part de personnage"""
        nom_canal = arguments.split(" ")[0]
        message = " ".join(arguments.split(" ")[1:])
        canal = self.canaux[nom_canal]
        if personnage not in canal.connectes:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            return
        if not message or message.isspace():
            personnage << "Que voulez-vous dire ?"
            return
        canal.envoyer(personnage, message)

    def traiter_commande(self, personnage, commande):
        """Traite les commandes au premier niveau"""
        res = False
        canaux_connectes = self.canaux.canaux_connectes(personnage)
        noms_canaux_connectes = [canal.nom for canal in canaux_connectes]
        if commande.startswith("+"):
            res = True
            self.rejoindre_ou_creer(personnage, commande[1:])
        elif commande.startswith("-"):
            res = True
            self.quitter_ou_detruire(personnage, commande[1:])
        elif commande.startswith(":"):
            res = True
            self.immerger(personnage, commande[1:])
        elif commande.startswith(". "):
            res = True
            self.dire_dernier_canal(personnage, commande[2:])
        elif commande.startswith("* "):
            res = True
            self.dire_tous_orbe(personnage, commande[2:])
        elif commande.startswith("!") and len(commande) > 1:
            res = True
            self.dire_orbe(personnage, commande[1:])
        elif commande.split(" ")[0] in noms_canaux_connectes:
            res = True
            self.dire_canal(personnage, commande)

        for att in self.attitudes_jouables:
            if contient(att.cle, commande.split(" ")[0]):
                res = True
                self.attitudes[att.cle].jouer(personnage, commande)
                break

        return res

    def joueur_connecte(self, joueur):
        """On avertit le joueur s'il a des messages non lus."""
        mails = self.mails.get_mails_pour(joueur, RECU)
        mails = [mail for mail in mails if not mail.lu]
        if len(mails) == 1:
            joueur << "|jn|Vous avez un message non lu.|ff|"
        elif len(mails) > 1:
            joueur << "|jn|Vous avez {} messages non lus.|ff|".format(
                    len(mails))

    def rapporter_conversation(self, canal, auteur, message):
        """Rapporte une conversation."""
        self.conv_logger.debug("<{}.{}> {}".format(canal, auteur.nom, message))

    def enregistrer_conversation(self, canal, cible, auteur, message):
        """Enregistre une conversation pour la cible du message."""
        if not hasattr(cible, "prototype"):
            conversations = self.messages.get(cible, [])
            conversations.append((datetime.datetime.now(), auteur, canal,
                    message))
            self.messages[cible] = conversations

    def extraire_historique(self, personnage, lignes=10, titre=None):
        """Extrait l'historique pour le joueur."""
        titre = titre or "Vos dernières conversations"
        messages = self.messages.get(personnage, [])
        if len(messages) == 0:
            raise ValueError("Il n'y a aucun message pour {}".format(
                    personnage))

        messages = messages[-lignes:]
        tableau = Tableau("|tit|" + titre + "|ff|", CENTRE)
        tableau.ajouter_colonne("|tit|Il y a|ff|")
        tableau.ajouter_colonne("|tit|Canal|ff|")
        tableau.ajouter_colonne("|tit|Nom|ff|")
        tableau.ajouter_colonne("|tit|Message|ff|")
        for date, auteur, canal, message in messages:
            delta = datetime.datetime.now() - date
            secondes = delta.total_seconds()
            duree = 0
            unite = "seconde"
            msg_duree = None
            if secondes < 5:
                msg_duree = "quelques secondes"
            elif secondes < 60:
                duree = secondes // 5 * 5
            elif secondes < 300:
                duree = secondes // 60
                unite = "minute"
            elif secondes < 3600:
                duree = secondes / 60 // 5 * 5
                unite = "minute"
            elif secondes < 86400:
                duree = secondes // 3600
                unite = "heure"
            else:
                duree = secondes // 86400
                unite = "jour"

            s = "s" if duree > 1 else ""
            if msg_duree is None:
                msg_duree = "{} {}{s}".format(int(duree), unite, s=s)

            tableau.ajouter_ligne(msg_duree, canal, auteur.nom, message)

        return tableau

    def dire_tous_orbe(self, personnage, message):
        """Dit le message à tous les orbes."""
        # On vérifie que le message n'est pas vide
        if not message:
            personnage << "|err|Que voulez-vous dire ?|ff|"
            return

        # On sélectionne les orbes du personnage
        orbes = personnage.equipement.inventaire.get_objets_type("orbe")
        if len(orbes) == 0:
            personnage << "|err|Vous ne possédez pas d'orbe.|ff|"
            return

        if len(orbes) > 1:
            orbe = importeur.communication.orbes.defauts.get(personnage)
            if orbe is None:
                personnage << "|err|Quel orbe souhaitez-vous utiliser ?|ff|"
                personnage.envoyer_tip("Utilisez la commande %orbe% " \
                        "%orbe:choisir% pour choisir votre orbe préféré.")
                return
            elif orbe.grand_parent is not personnage:
                personnage << "|err|Vous ne possédez pas cet orbe.|ff|"
                return
        else:
            orbe = orbes[0]

        if not orbe.nom_orbe:
            personnage << "|err|Cet orbe n'a pas de nom.|ff|"
            personnage.envoyer_tip("Utilisez la commande %orbe% " \
                        "%orbe:renommer% pour renommer un orbe.")
            return

        # On cherche les connectés qui ont le même type d'orbe
        joueurs = []
        for joueur in importeur.connex.joueurs_connectes:
            if joueur is not personnage and \
                    joueur.equipement.inventaire.get_objets_cle(orbe.cle):
                joueurs.append(joueur)

        # Envoie à chaque joueur du message
        personnage << "|jn|[{}] Vous dites : {}|ff|".format(orbe.get_nom(),
                message)
        for joueur in joueurs:
            self.envoyer_orbe(personnage, joueur, orbe, message)

    def dire_orbe(self, personnage, message):
        """Dit le message à un orbes."""
        # On vérifie que le message n'est pas vide
        if not message:
            personnage << "|err|Que voulez-vous dire ?|ff|"
            return

        # On sélectionne les orbes du personnage
        orbes = personnage.equipement.inventaire.get_objets_type("orbe")
        if len(orbes) == 0:
            personnage << "|err|Vous ne possédez pas d'orbe.|ff|"
            return

        if len(orbes) > 1:
            orbe = importeur.communication.orbes.defauts.get(personnage)
            if orbe is None:
                personnage << "|err|Quel orbe souhaitez-vous utiliser ?|ff|"
                personnage.envoyer_tip("Utilisez la commande %orbe% " \
                        "%orbe:choisir% pour choisir votre orbe préféré.")
                return
            elif orbe.grand_parent is not personnage:
                personnage << "|err|Vous ne possédez pas cet orbe.|ff|"
                return
        else:
            orbe = orbes[0]

        if not orbe.nom_orbe:
            personnage << "|err|Cet orbe n'a pas de nom.|ff|"
            personnage.envoyer_tip("Utilisez la commande %orbe% " \
                        "%orbe:renommer% pour renommer un orbe.")
            return

        # On cherche l'orbe
        nom = supprimer_accents(message.split(" ")[0]).lower()
        message = " ".join(message.split(" ")[1:])

        orbe_destinataire = None
        orbes = importeur.objet.get_objets_de_type("orbe")
        for autre_orbe in orbes:
            if autre_orbe.nom_orbe == nom:
                orbe_destinataire = autre_orbe
                break

        if orbe_destinataire is None:
            personnage << "|err|Vous ne pouvez trouver cet orbe.|ff|"
            return

        destinataire = orbe_destinataire.grand_parent
        personnage << "|jn|[{}] Vous dites à l'orbe {} : {}|ff|".format(
                orbe.get_nom(), orbe_destinataire.nom_orbe, message)
        self.envoyer_orbe(personnage, destinataire, orbe,
                message, "secrètement ")

    def envoyer_orbe(self, auteur, destinataire, orbe, message, ajout=""):
        """Envoie et brouille le message en fonction de la distance."""
        s_auteur = auteur.salle
        s_destinataire = getattr(destinataire, "salle", destinataire)
        if s_auteur.coords.valide and s_destinataire.coords.valide:
            distance = mag(s_auteur.coords.x, s_auteur.coords.y,
                    s_auteur.coords.z, s_destinataire.coords.x,
                    s_destinataire.coords.y, s_destinataire.coords.z)
        else:
            distance = 20

        # En fonction de la distance, essaye de prélever de la mana
        mana = int(round(distance / 2))
        if mana < 10:
            mana = 10
        elif mana > 100:
            mana = 100

        try:
            auteur.stats.mana -= mana
        except DepassementStat:
            # Brouille le message
            taux = distance / 400
            if taux < 0.02:
                taux = 0.02
            elif taux > 0.3:
                taux = 0.3

            for i, car in enumerate(message):
                if random() < taux:
                    message = message[:i] + "?" + message[i + 1:]

        # Enfin, on fait attendre le message en fonction de la distance
        temps = distance / 100
        if temps < 1:
            temps = 1

        importeur.communication.enregistrer_conversation("|jn|orbe|ff|",
                destinataire, auteur, message)
        message = "|jn|[Orbe {}] dit {}: {}|ff|".format(orbe.nom_orbe,
                ajout, message)
        importeur.diffact.ajouter_action("orbe_{}".format(str(id(message))),
                temps, destinataire.envoyer, message)
