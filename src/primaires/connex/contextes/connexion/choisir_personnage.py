# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 DAVY Guillaume
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

from datetime import datetime
import re

from primaires.interpreteur.contexte import Contexte

# Constantes
cmd_creer = "c"
cmd_supprimer = "s"
cmd_quitter = "q"
cmd_chmdp = "m"
cmd_recup_vancia = "v"

class ChoisirPersonnage(Contexte):
    """Contexte du choix de personnage

    """
    nom = "connex:connexion:choix_personnages"

    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)

    def entrer(self):
        """Si aucun personnage n'a été créé, on redirige vers la création d'un
        premier personnage.
        Dans tous les cas, on recopie l'encodage du compte dans le client.

        """
        self.pere.client.encodage = self.pere.compte.encodage

    def get_prompt(self):
        """Message de prompt"""
        return "Votre choix : "

    def accueil(self):
        """Message d'accueil"""
        ret = \
            "\n|tit|------= Choix du personnage =------|ff|\n" \
            "Faites votre |ent|choix|ff| parmi la liste ci-dessous :\n"

        for i, joueur in enumerate(self.pere.compte.joueurs):
            no = " |cmd|" + str(i + 1) + "|ff|"
            ret += "\n" + no + " pour jouer |ent|{0}|ff|".format( \
                joueur.nom)
            if joueur in importeur.connex.bannissements_temporaires:
                mtn = datetime.now()
                date = importeur.connex.bannissements_temporaires[joueur]
                duree = (date - mtn).seconds
                mesure = "seconde"
                if mtn > date:
                    duree = 0
                elif duree >= 86400:
                    duree //= 86400
                    mesure = "jour"
                elif duree >= 3600:
                    duree //= 3600
                    mesure = "heure"
                elif duree > 60:
                    duree //= 60
                    mesure = "minute"

                s = ""
                if duree > 1:
                    s = "s"

                temps = " (|rg|banni pour {} {}{s})".format(duree,
                        mesure, s=s)
                ret += temps
            elif joueur in importeur.connex.joueurs_bannis:
                ret += " (|rg|banni du serveur)|ff|"
            elif joueur.est_connecte():
                ret += " (connecté sur "
                adresse_ip = joueur.instance_connexion.adresse_ip
                if self.pere.adresse_ip == adresse_ip:
                    ret += "la même adresse)"
                else:
                    ret += "l'adresse {})".format(adresse_ip)

        if len(self.pere.compte.joueurs) > 0:
            # on saute deux lignes
            ret += "\n"

        ret += "\n"
        ret += " |cmd|{C}|ff| pour |ent|créer|ff| un nouveau " \
                "personnage\n".format(C = cmd_creer.upper())
        if len(self.pere.compte.joueurs) > 0:
            # on propose de supprimer un des joueurs créé
            ret += " |cmd|{S}|ff| pour |ent|supprimer|ff| un personnage de " \
                "ce compte\n".format(S = cmd_supprimer.upper())

        ret += " |cmd|{M}|ff| pour changer votre |ent|mot de passe|ff|" \
                "\n".format(M = cmd_chmdp.upper())
        ret += " |cmd|{V}|ff| pour importer un |ent|joueur de Vancia|ff|" \
                "\n".format(V=cmd_recup_vancia.upper())

        ret += " |cmd|{Q}|ff| pour |ent|quitter|ff| le jeu".format( \
                Q = cmd_quitter.upper())
        return ret

    def interpreter(self, msg):
        """Méthode d'interprétation"""
        cfg_connex = type(self).importeur.anaconf.get_config("connex")
        nb_perso_max = cfg_connex.nb_perso_max

        msg = msg.lower()
        if msg.isdecimal():
            # On le convertit
            choix = int(msg) - 1
            # On vérifie qu'il est bien dans la liste des comptes
            if choix < 0 or choix >= len(self.pere.compte.joueurs):
                self.pere.envoyer("|err|Aucun personnage ne correspond à ce " \
                        "numéro.|ff|")
            else:
                # On vérifie qu'il n'est pas banni
                joueur = self.pere.compte.joueurs[choix]
                if joueur in importeur.connex.bannissements_temporaires or \
                        joueur in importeur.connex.joueurs_bannis:
                    self.pere << "|err|Ce joueur est banni du serveur.|ff|"
                    return

                # on se connecte sur le joueur
                joueur = self.pere.compte.joueurs[choix]
                joueur.compte = self.pere.compte
                joueur.instance_connexion = self.pere
                self.pere.joueur = joueur
                joueur.connecte = False

                # On log la connexion
                importeur.connex.table_logger.info(
                        "{} se connecte sur {}".format(joueur.nom,
                        self.pere.adresse_ip))

                races = type(self).importeur.perso.races
                if joueur.race is None and len(races) > 0:
                    self.migrer_contexte("personnage:creation:choix_race")
                elif joueur.genre == "aucun" and joueur.race is not None and \
                        len(joueur.race.genres) > 0:
                    self.migrer_contexte("personnage:creation:choix_genre")
                else:
                    joueur.pre_connecter()
                    self.detruire()
        elif msg == cmd_creer:
            if len(self.pere.compte.joueurs) >= nb_perso_max and nb_perso_max != -1:
                self.pere.envoyer("|err|Vous ne pouvez avoir plus de {0} " \
                        "personnages.|ff|".format(nb_perso_max))
            else:
                # On redirige vers la création de compte
                importeur.joueur.migrer_ctx_creation(self)
        elif msg == cmd_supprimer:
            if len(self.pere.compte.joueurs) == 0:
                self.pere.envoyer("|err|Vous ne pouvez pas supprimer de "\
                        "personnage si vous n'en avez pas.|ff|")
            else:
                # On redirige vers la suppression de comptes
                self.migrer_contexte("personnage:suppression:suppression")
        elif msg == cmd_quitter:
            # On déconnecte le joueur
            self.pere.envoyer("\nA bientôt !")
            self.pere.deconnecter("Déconnexion demandée par le client")
        elif msg == cmd_chmdp:
            # On redirige vers la modification de mot de passe
            self.migrer_contexte("connex:connexion:choisir_pass")
        elif msg == cmd_recup_vancia:
            # On redirige vers le contexte de récupération de Vancia
            self.migrer_contexte("personnage:creation:recup_vancia")
        else:
            self.pere.envoyer("|err|Votre choix est invalide.|ff|")
