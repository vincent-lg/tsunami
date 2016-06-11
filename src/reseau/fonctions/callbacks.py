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


"""Ce fichier définit les fonctions de callback du serveur.

Ces fonctions sont appelées dans le cadre d'évènements serveur (connexion
d'un client, déconnexion, réception d'un message...)

Elles prennent toutes le préfixe cb_ (callback)

"""

import traceback

def cb_connexion(serveur, importeur, logger, client):
    """Que se passe-t-il quand client se connecte ?"""
    logger.info("Connexion du client {0}".format(client))
    importeur.connex.ajouter_instance(client)

def cb_deconnexion(serveur, importeur, logger, client):
    """Que se passe-t-il quand client se déconnecte ?"""
    logger.info("Déconnexion du client {0} : {1}".format(client, client.retour))
    importeur.connex.retirer_instance(client)


def cb_reception(serveur, importeur, logger, client, msg):
    """Que se passe-t-il quand client envoie un message au serveur ?"""
    instance = importeur.connex[client]
    try:
        instance.receptionner(msg)
    except Exception:
        msg = importeur.interpreteur.erreurs.get((instance.joueur,
                msg), msg)
        trace = traceback.format_exc()
        logger.fatal("Exception levée lors de l'interprétation de " \
                "l'entrée : {}".format(msg))
        logger.fatal(traceback.format_exc())
        instance.envoyer(
            "|err|Une erreur s'est produite lors du traitement " \
            "de votre commande.|ff|")
        if instance.joueur:
            importeur.hook["joueur:erreur"].executer(instance.joueur,
                    msg, trace)
