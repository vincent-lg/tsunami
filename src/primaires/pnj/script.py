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


"""Fichier contenant la classe ScriptPNJ détaillée plus bas."""

from primaires.scripting.script import Script

class ScriptPNJ(Script):

    """Script et évènements propre aux PNJ.

    C'est dans cette classe que sont construits les évènements du scripting
    des PNJ. Il est ainsi plus facile à modifier si vous souhaitez
    rajouter un évènement.

    """

    def init(self):
        """Initialisation du script"""
        # Evénement entre
        evt_entre = self.creer_evenement("entre")
        evt_entre.aide_courte = "le PNJ entre quelque part"
        evt_entre.aide_longue = \
            "Cet évènement est appelé quand le PNJ entre dans une salle, " \
            "quelque soit sa salle de provenance et " \
            "de destination."

        # Configuration des variables de l'évènement entre
        var_depuis = evt_entre.ajouter_variable("depuis", "str")
        var_depuis.aide = "la direction d'où vient le PNJ"
        var_salle = evt_entre.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle actuelle du PNJ"

        # Evénement sort
        evt_sort = self.creer_evenement("sort")
        evt_sort.aide_courte = "le PNJ quitte une salle"
        evt_sort.aide_longue = \
            "Cet évènement est appelé quand le PNJ quitte une " \
            "salle via un déplacement standard (en entrant un nom de " \
            "sortie). Le déplacement par |cmd|goto|ff| n'appelle " \
            "pas cet évènement. Cependant, un déplacement par script " \
            "l'appelle (faire attention aux boucles infinies potentielles)."

        # Configuration des variables de l'évènement sort
        var_vers = evt_sort.ajouter_variable("vers", "str")
        var_vers.aide = "la direction empruntée par le PNJ"
        var_salle = evt_sort.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle quittée par le PNJ"
        var_destination = evt_sort.ajouter_variable("destination", "Salle")
        var_destination.aide = "la salle où se rend le PNJ"

        # Evénement arrive
        evt_arrive = self.creer_evenement("arrive")
        evt_arrive.aide_courte = "un personnage arrive dans la salle du PNJ"
        evt_arrive.aide_longue = \
            "Cet évènement est appelé quand un personnage arrive dans la " \
            "salle où se trouve le PNJ."

        # Configuration des variables de l'évènement arrive
        var_depuis = evt_arrive.ajouter_variable("depuis", "str")
        var_depuis.aide = "la direction d'où vient le personnage"
        var_personnage = evt_arrive.ajouter_variable("personnage",
                "Personnage")
        var_personnage.aide = "le personnage qui arrive"
        var_salle = evt_arrive.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle d'où vient le personnage"

        # Evénement part
        evt_part = self.creer_evenement("part")
        evt_part.aide_courte = "un personnage part de la salle du PNJ"
        evt_part.aide_longue = \
            "Cet évènement est appelé quand un personnage quitte la salle " \
            "où se trouve le PNJ."

        # Configuration des variables de l'évènement part
        var_vers = evt_part.ajouter_variable("vers", "str")
        var_vers.aide = "la direction empruntée par le personnage"
        var_destination = evt_part.ajouter_variable("destination", "Salle")
        var_destination.aide = "la salle où se rend le personnage"
        var_personnage = evt_part.ajouter_variable("personnage", "Personnage")
        var_personnage.aide = "le personnage qui arrive"

        # Evénement regarde
        evt_regarde = self.creer_evenement("regarde")
        evt_reg_avant = evt_regarde.creer_evenement("avant")
        evt_reg_apres = evt_regarde.creer_evenement("après")
        evt_regarde.aide_courte = "un personnage regarde le PNJ"
        evt_reg_avant.aide_courte = "avant la description du PNJ"
        evt_reg_apres.aide_courte = "après la description du PNJ"
        evt_regarde.aide_longue = \
            "Cet évènement est appelé quand un personnage regarde le PNJ."
        evt_reg_avant.aide_longue = \
            "Cet évènement est appelé avant que la description du PNJ " \
            "ne soit envoyée au personnage le regardant."
        evt_reg_apres.aide_longue = \
            "Cet évènement est appelé après que la description du PNJ " \
            "ait été envoyée au personnage le regardant."

        # Configuration des variables de l'évènement regarde
        var_perso = evt_regarde.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage regardant le PNJ"

        # Evénement discute
        evt_discute = self.creer_evenement("discute")
        evt_discute.aide_courte = "un personnage engage une discussion avec " \
                "le PNJ"
        evt_discute.aide_longue = \
            "Cet évènement est appelé quand un personnage engage une " \
            "discussion avec le PNJ à propos d'un sujet quelconque."

        # Configuration des variables de l'évènement discute
        var_sujet = evt_discute.ajouter_variable("sujet", "str")
        var_sujet.aide = "le sujet de la discussion"
        var_perso = evt_discute.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage regardant le PNJ"

        # Evénement attaque
        evt_attaque = self.creer_evenement("attaqué")
        evt_attaque.aide_courte = "le PNJ est attaqué par un personnage"
        evt_attaque.aide_longue = \
            "Cet évènement est appelé quand le PNJ est attaqué en " \
            "corps-à-corps. Le personnage l'attaquant est stocké dans " \
            "la variable |ent|personnage|ff|."

        # Configuration des variables de l'évènement attaque
        var_perso = evt_attaque.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage attaquant le PNJ"

        # Evénement donne
        evt_donne = self.creer_evenement("donne")
        evt_donne.aide_courte = "un personnage donne un objet au PNJ"
        evt_donne.aide_longue = \
            "Cet évènement est appelé quand un personnage donne un ou " \
            "plusieurs objet(s) au PNJ, à condition que le PNJ puisse " \
            "le(s) prendre."

        # Configuration des variables de l'évènement donne
        var_objet = evt_donne.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet donné"
        var_qtt = evt_donne.ajouter_variable("quantite", "int")
        var_qtt.aide = "la quantité remise"
        var_perso = evt_donne.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le donneur"

        # Evénement tick
        evt_tick = self.creer_evenement("tick")
        evt_tick.aide_courte = "le tick du PNJ se déclenche"
        evt_tick.aide_longue = \
            "Cet évènement est appelé quand le tick du PNJ se déclenche " \
            "(toutes les minutes)."

        # Evénement repop
        evt_repop = self.creer_evenement("repop")
        evt_repop.aide_courte = "le PNJ se repop"
        evt_repop.aide_longue = \
            "Cet évènement est appelé quand le PNJ repop, dans deux " \
            "cas : soit quand le MUD se lance (tous les PNJ sont " \
            "repop automatiquement, bien qu'ils gardent la plupart " \
            "de leurs informations) ou quand ils apparaissent dans une " \
            "salle qui a configuré le PNJ en repop."

        # Événement marchand
        evt_marchand = self.creer_evenement("marchand")
        evt_marchand.aide_courte = "le vendeur du magasin agit"
        evt_marchand.aide_longue = \
            "Cet évènement est appelé si le PNJ est un vendeur de magasin, " \
            "dans différentes situations qui sont classées en sous-évènements."

        # Évènement marchand.achète
        evt_marchand_achete = evt_marchand.creer_evenement("achète")
        evt_marchand_achete.aide_courte = "un personnage vend quelque chose"
        evt_marchand_achete.aide_longue = \
            "Cet évènement est appelé quand un personnage vend quelque " \
            "chose dans le magasin, c'est-à-dire quand le magasin " \
            "achète un produit. Le sous-èvénement 'avant' permet " \
            "d'empêcher la transaction (le magasin ne veut pas de " \
            "l'objet, pour X raison) et permet de modifier d'autres " \
            "informations, comme la valeur de l'objet. Le sous-évènement " \
            "'après', au contraire, est appelé quand la transaction " \
            "a bel et bien eu lieu."

        # Évènement marchand.achète.avant
        evt_marchand_achete_avt = evt_marchand_achete.creer_evenement("avant")
        evt_marchand_achete_avt.aide_courte = "avant l'achat"
        evt_marchand_achete_avt.aide_longue = \
            "Cet évènement est appelé quand le personnage entre la " \
            "commande vendre/sell en précisant un produit. La transaction " \
            "n'est pas encore conclue et peut être refusée, en " \
            "utilisant l'action 'interrompre'. La valeur de la " \
            "transaction peut également être modifiée en modifiant " \
            "la variable 'valeur' qui doit valoir le prix du produit " \
            "vendu.\n\nVariables pouvant être modifiées :\n    valeur : " \
            "la valeur de vente du produit\n    conserver : met le " \
            "produit dans l'inventaire du magasin"

        # Configuration des variables de l'évènement marchand.achète.avant
        var_conserver = evt_marchand_achete_avt.ajouter_variable("conserver",
                "Fraction")
        var_conserver.aide = "doit-on mettre les objets en vente " \
                "(1 par défaut)"

        # Évènement marchand.achète.après
        evt_marchand_achete_apr = evt_marchand_achete.creer_evenement("après")
        evt_marchand_achete_apr.aide_courte = "après l'achat"
        evt_marchand_achete_apr.aide_longue = \
            "Cet évènement est appelé quand le personnage entre la " \
            "commande vendre/sell en précisant un produit. La transaction " \
            "a été conclue et validée (payée). On peut maintenant " \
            "souhaiter faire des opérations particulières sur les " \
            "objets vendus."

        # Configuration des variables de l'évènement marchand.achète
        var_perso = evt_marchand_achete.ajouter_variable("personnage",
                "Personnage")
        var_perso.aide = "le personnage vendant ses produits"
        var_objet = evt_marchand_achete.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet vendu"
        var_valeur = evt_marchand_achete.ajouter_variable("valeur",
                "Fraction")
        var_valeur.aide = "la valeur des objets vendus"

        # Évènement marchand.ferme
        evt_marchand_ferme = evt_marchand.creer_evenement("ferme")
        evt_marchand_ferme.aide_courte = "la magasin ferme ses portes"
        evt_marchand_ferme.aide_longue = \
            "Cet évènement est appelé quand le magasin ferme ses portes."

        # Évènement marchand.infos
        evt_marchand_infos = evt_marchand.creer_evenement("infos")
        evt_marchand_infos.aide_courte = "un personnage demande des infos"
        evt_marchand_infos.aide_longue = \
            "Cet évènement est appelé quand un personnage demande des " \
            "informations sur un service en vente grâce à la commande " \
            "|cmd|infos|ff|."

        # Configuration des variables de l'évènement marchand.infos
        var_perso = evt_marchand_infos.ajouter_variable("personnage",
                "Personnage")
        var_perso.aide = "le personnage demandant des informationss"
        var_type = evt_marchand_infos.ajouter_variable("type", "str")
        var_type.aide = "le type de service concerné"
        var_cle = evt_marchand_infos.ajouter_variable("cle", "str")
        var_cle.aide = "la clé du service concerné"
        var_qtt = evt_marchand_infos.ajouter_variable("quantite", "Fraction")
        var_qtt.aide = "la quantité du service concerné"

        # Évènement marchand.ouvre
        evt_marchand_ouvre = evt_marchand.creer_evenement("ouvre")
        evt_marchand_ouvre.aide_courte = "le magasin ouvre ses portes"
        evt_marchand_ouvre.aide_longue = \
            "Cet évènement est appelé quand le magasin ouvre ses portes. Si " \
            "le vendeur n'est pas trouvé dans la salle du magasin, alors " \
            "le premier PNJ modelé sur le prototype indiqué dans le " \
            "magasin est choisi (qu'il soit là où non)."

        # Évènement marchand.vend
        evt_marchand_vend = evt_marchand.creer_evenement("vend")
        evt_marchand_vend.aide_courte = "un personnage achète quelque chose"
        evt_marchand_vend.aide_longue = \
            "Cet évènement est appelé quand un personnage achète quelque " \
            "chose dans le magasin, c'est-à-dire quand le magasin " \
            "vend un produit. Le sous-èvénement 'avant' permet " \
            "d'empêcher la transaction (le magasin ne veut pas vendre " \
            "le service, pour X raison) et permet de modifier d'autres " \
            "informations, comme la valeur du service. Le sous-évènement " \
            "'après', au contraire, est appelé quand la transaction " \
            "a bel et bien eu lieu."

        # Évènement marchand.vend.avant
        evt_marchand_vend_avt = evt_marchand_vend.creer_evenement("avant")
        evt_marchand_vend_avt.aide_courte = "avant la vente"
        evt_marchand_vend_avt.aide_longue = \
            "Cet évènement est appelé quand le personnage entre la " \
            "commande acheter/buy en précisant un service. La transaction " \
            "n'est pas encore conclue et peut être refusée, en " \
            "utilisant l'action 'interrompre'. La valeur de la " \
            "transaction peut également être modifiée en modifiant " \
            "la variable 'valeur' qui doit valoir le prix du service " \
            "vendu. |att|ATTENTION|ff| toutefois : à la différence " \
            "de l'évènement marchand.achète, le magasin vend des " \
            "services, pas forcément des objets. Le type du service " \
            "est passé en variable (objet, familier, navire...) et " \
            "la clé du service se trouve dans la variable |ent|cle|ff|."

        # Évènement marchand.vend.après
        evt_marchand_vend_apr = evt_marchand_vend.creer_evenement("après")
        evt_marchand_vend_apr.aide_courte = "après l'achat"
        evt_marchand_vend_apr.aide_longue = \
            "Cet évènement est appelé quand le personnage entre la " \
            "commande acheter/buy en précisant un service. La transaction " \
            "a été conclue et validée (payée)."

        # Configuration des variables de l'évènement marchand.vend
        var_perso = evt_marchand_vend.ajouter_variable("personnage",
                "Personnage")
        var_perso.aide = "le personnage achetant les services"
        var_type = evt_marchand_vend.ajouter_variable("type", "str")
        var_type.aide = "le type de service acheté"
        var_cle = evt_marchand_vend.ajouter_variable("cle", "str")
        var_cle.aide = "la clé du service acheté"
        var_qtt = evt_marchand_vend.ajouter_variable("quantite", "Fraction")
        var_qtt.aide = "la quantité du service acheté"
        var_valeur = evt_marchand_vend.ajouter_variable("valeur",
                "Fraction")
        var_valeur.aide = "la valeur des services achetés"

        # Événement meurt
        evt_meurt = self.creer_evenement("meurt")
        evt_meurt.nom_acteur = "adversaire"
        evt_meurt_avant = evt_meurt.creer_evenement("avant")
        evt_meurt_avant.nom_acteur = "adversaire"
        evt_meurt_apres = evt_meurt.creer_evenement("après")
        evt_meurt_apres.nom_acteur = "adversaire"
        evt_meurt.aide_courte = "le PNJ meurt"
        evt_meurt_avant.aide_courte = "avant la mort du PNJ"
        evt_meurt_apres.aide_courte = "après la mort du PNJ"
        evt_meurt.aide_longue = \
            "Cet évènement est appelé quand le PNJ meurt d'une façon ou " \
            "d'une autre (lors d'un combat, tué par un script, tué à " \
            "proximité ou à distance)."
        evt_meurt_avant.aide_longue = \
            "Cet évènement est appelé avant la mort du PNJ. Le PNJ n'est " \
            "pas encore réellement mort, cependant le message a déjà été " \
            "envoyé aux autres joueurs présents dans la salle. Si " \
            "le script est interrompu avec 'interrompre', le cadavre " \
            "du PNJ n'est pas créé."
        evt_meurt_apres.aide_longue = \
            "Cet évènement est appelé quand le PNJ est déjà mort et que " \
            "son cadavre a été créé sur le sol."

        # Configuration des variables de l'évènement meurt et
        # sous-évènements
        var_salle = evt_meurt.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle où meurt le PNJ"
        var_adv = evt_meurt.ajouter_variable("adversaire", "Personnage")
        var_adv.aide = "l'adversaire du PNJ (si meurt en combat)"

        # Evénement tue
        evt_tue = self.creer_evenement("tue")
        evt_tue.aide_courte = "le PNJ tue un personnage"
        evt_tue.aide_longue = \
            "Cet évènement est appelé quand le PNJ tue (en combat rapproché " \
            "ou non) un autre personnage."

        # Configuration des variables de l'évènement attaque
        var_perso = evt_tue.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage tué par le PNJ"

        # Événement dépece
        evt_depece = self.creer_evenement("dépece")
        evt_depece.aide_courte = "le PNJ est dépecé"
        evt_depece.aide_longue = \
            "Cet évènement est appelé quand le cadavre du PNJ est " \
            "dépecé. Le personnage dépeçant le PNJ se trouve dans " \
            "la variable 'personnage'. Cet évènement est appelé " \
            "après l'envoie du message au personnage."

        # Configuration des variables de l'évènement dépece
        var_perso = evt_depece.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage dépeçant le PNJ"
        var_salle = evt_depece.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle où est dépecé le PNJ"

        # Événement gagne_niveau
        evt_niveau = self.creer_evenement("gagne_niveau")
        evt_niveau.aide_courte = "le PNJ gagne un niveau"
        evt_niveau.aide_longue = \
            "Cet évènement est appelé quand le PNJ gagne un niveau, " \
            "principal ou secondaire. Pour obtenir le niveau actuel " \
            "du PNJ, vous pouvez utiliser la fonction du même nom."

        # Événement dit
        evt_dit = self.creer_evenement("dit")
        evt_dit.aide_courte = "un personnage dit quelque chose dans la " \
                "salle du PNJ"
        evt_dit.aide_longue = \
            "Cet évènement est appelé quand un personnage dit quelque " \
            "chose dans la salle. Il est appelé après la diffusion " \
            "du message à tous les personnages présents. Notez que, " \
            "si le PNJ parle via commande, son propre script n'est " \
            "pas appelé."

        # Configuration des variables de l'évènement dit
        var_message = evt_dit.ajouter_variable("message", "str")
        var_message.aide = "ce qui est dit par le personnage"
        var_perso = evt_dit.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage disant quelque chose"
        var_salle = evt_dit.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle le personnage parle"


        # Événement effacer_memoire
        evt_effacer_memoire = self.creer_evenement("effacer_memoire")
        evt_effacer_memoire.aide_courte = "une mémoire est effacée"
        evt_effacer_memoire.aide_longue = \
            "Cet évènement est appelé quand une mémoire " \
            "enregistrée dans le prototype de PNJ est effacée par le " \
            "système. C'est très utile pour exécuter une action " \
            "particulière quand une mémoire expire. |att|ATTENTION|ff| : " \
            "les mémoires de PNJ sont stockées dans le prototype de " \
            "PNJ. Ainsi, quand la mémoire s'efface, c'est le " \
            "prototype de PNJ qui est considérée, pas le PNJ. La " \
            "variable 'prototype' contient donc le prototype de PNJ. " \
            "Vous pouvez récupérer sa clé avec la fonction " \
            "'cle_prototype'."

        # Configuration des variables de l'évènement effacer_memoire
        var_proto = evt_effacer_memoire.ajouter_variable("prototype",
                "PrototypePNJ")
        var_proto.aide = "le prototype de PNJ"
        var_nom = evt_effacer_memoire.ajouter_variable("nom", "str")
        var_nom.aide = "le nom de la mémoire à effacer"
        var_valeur = evt_effacer_memoire.ajouter_variable("valeur", "Object")
        var_valeur.aide = "la valeur de la mémoire qu'on va effacer"

        # Événement attitude
        evt_attitude = self.creer_evenement("attitude")
        evt_attitude.aide_courte = "on fait une attitud4e sur le PNJ"
        evt_attitude.aide_longue = \
            "Cet évènement est appelé quand un personnage fait une " \
            "attitude en prenant le PNJ pour cible, comme lui sourit, " \
            "ou se fait tout petit devant lui, par exemple. La clé " \
            "de l'attitude est conservée dans la variable 'cle'."

        # Configuration des variables de l'évènement attitude
        var_cle = evt_attitude.ajouter_variable("cle", "str")
        var_cle.aide = "la clé de l'attitude utilisée"
        var_perso = evt_attitude.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage faisant l'attitude"
        var_salle = evt_attitude.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se produit l'attitude"

        # Événement apparait
        evt_apparait = self.creer_evenement("apparaît")
        evt_apparait.aide_courte = "le PNJ apparaît dans une salle"
        evt_apparait.aide_longue = \
            "Cet évènement est appelé quand le PNJ est créé dans une " \
            "salle, c'est-à-dire quand le PNJ se crée au repop. Notez que " \
            "si le PNJ est pspawn, ou si il est crée grâce à la " \
            "fonction creer_PNJ(), le PNJ n'ayant pas de " \
            "salle, cet évènement n'est pas appelé. À la différence de " \
            "l'évènement repop, l'évènement apparaît n'est appelé qu'une " \
            "fois par PNJ qui apparaît dans une salle."

        # Configuration des variables de l'évènement apparait
        var_salle = evt_apparait.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle le PNJ apparaît"

        # On ajoute à tous les évènements la variable 'pnj'
        for evt in self.evenements.values():
            if evt.nom in ("dépece", "effacer_memoire"):
                continue

            var_pnj = evt.ajouter_variable("pnj", "PNJ")
            var_pnj.aide = "le PNJ scripté"
