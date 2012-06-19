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
# pereIBILITY OF SUCH DAMAGE.


"""Fichier contenant le contexte 'personnage:connexion:mode_connecte"""

from primaires.interpreteur.contexte import Contexte
from primaires.interpreteur.masque.dic_masques import DicMasques
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_interpretation \
        import ErreurInterpretation
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.perso.exceptions.action import ExceptionAction
from primaires.scripting.exceptions import InterrompreCommande

class ModeConnecte(Contexte):
    
    """Le contexte de mode connecté.
    C'est une petite institution à lui tout seul.
    A partir du moment où un joueur se connecte, il est connecté à ce contexte.
    Les commandes se trouvent définies dans ce contexte. En revanche, d'autres
    contextes peuvent venir se greffer par-dessus celui-ci. Mais il reste
    toujours un contexte présent dans la pile des contextes du joueur dès
    lors qu'il est connecté.
    
    """
    nom = "personnage:connexion:mode_connecte"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.unom = "mode_connecté"
        self.opts.prompt_clr = ""
        self.opts.prompt_prf = ""
    
    def accueil(self):
        """Message d'accueil du contexte"""
        return self.pere.joueur.salle.regarder(self.pere.joueur)
    
    def get_prompt(self):
        """Méthode du prompt du contexte"""
        joueur = self.pere.joueur
        return joueur.prompt + "\n"
    
    def interpreter(self, msg):
        """Méthode d'interprétation.
        
        Ce contexte est destiné à l'interprétation de commande en mode
        connecté.
        On commence donc par valider la commande entrée par le joueur
        (autrement dit savoir quelle commande le joueur souhaite exécuter,
        quel paramètre il lui a fourni, quelles informations on peut retirer
        de cette commande...).
        La seconde partie est l'interprétation de la commande : que fait-on
        avec les paramètres que le joueur a entré ?
        
        Note: ne rajoutez pas d'instructions impliquant l'instance de
        connexion 'pere' après l'interprétation de la commande. Si
        la commande entraîne un 'hotboot' (redémarrage à chaud des modules),
        l'instance pourrait ne pas être à jour.
        
        """
        personnage = self.pere.joueur
        
        # D'abord, on cherche à isoler les alias
        if msg:
            msgs = msg.split(" ")
            comm = msgs[0]
            a_msg = " ".join(msgs[1:])
            comm = comm.lower()
            alias = personnage.alias
            if comm in alias:
                comm = alias[comm]
                msg = comm
                if a_msg:
                    msg += " " + a_msg
        
        # On commence par parcourir tous les modules
        res = False
        for module in type(self).importeur.modules:
            try:
                res = module.traiter_commande(self.pere.joueur, msg)
            except ExceptionAction as err_act:
                self.pere.joueur << "|err|{}|ff|".format(err_act)
                return
            except InterrompreCommande as err:
                if err.message:
                    self.pere.joueur << "|err|{}|ff|".format(err)
                return
            else:
                if res:
                    break
        
        if not res:
            interpreteur = type(self).importeur.interpreteur
            masques = []
            dic_masques = DicMasques()
            lst_commande = chaine_vers_liste(msg)
            logger = type(self).importeur.man_logs.get_logger("sup")
            traceback = __import__("traceback")
            try:
                interpreteur.repartir(self.pere.joueur, masques, lst_commande)
                for masque in masques:
                    dic_masques[masque.nom] = masque
                
                interpreteur.valider(self.pere.joueur, dic_masques)
            except ErreurValidation as err_val:
                err_val = str(err_val)
                for masque in masques:
                    dic_masques[masque.nom] = masque
                if not err_val and dic_masques:
                    masque = dic_masques.dernier_parametre
                    err_val = masque.erreur_validation(self.pere.joueur, \
                            dic_masques)
                self.pere.joueur.envoyer(str(err_val))
            except Exception:
                logger.fatal("Exception " \
                        "levée lors de la validation d'une commande.")
                logger.fatal(traceback.format_exc())
                self.pere.joueur.envoyer(
                    "|err|Une erreur s'est produite lors du traitement de " \
                    "votre commande.\nLes administrateurs en ont été " \
                    "avertis.|ff|")
            else:
                exception = ErreurInterpretation
                try:
                    # On cherche le dernier paramètre
                    for masque in reversed(list(dic_masques.values())):
                        if masque.est_parametre():
                            commande = masque
                            break
                    
                    commande.execution_differee(self.pere.joueur, dic_masques)
                except ExceptionAction as err_act:
                    self.pere.joueur << "|err|{}|ff|".format(err_act)
                except exception as err_int:
                    self.pere.joueur.envoyer(str(err_int))
