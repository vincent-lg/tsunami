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


"""Ce fichier contient la configuration par défaut du module 'email'."""

cfg_email = r"""
# Ce fichier contient la configuration globale du serveur d'e-mail.
# C'est ici que vous autorisez le module 'email' à envoyer des mails, que
# vous précisez le nom d'hôte utilisé pour envoyer les messages

## Autorisation

# Si vous mettez cette donnée à False, le serveur d'e-mail sera considéré
# comme inactif. Le module primaire 'email' ne pourra donc pas envoyer
# d'e-mails.
# Notez tout de même qu'il est préférable d'avoir un serveur mail configuré
# sur le serveur hébergeant le projet.
serveur_mail = False

## Nom d'hôte

# Modifiez cette donnée pour spécifier le nom d'hôte de votre serveur
# d'e-mail. Si vous précisez "exemple.com" en nom d'hôte, les messages envoyés
# depuis l'alias "info" seront envoyés depuis l'adresse "info@exemple.com".
# Si vous précisez une chaîne vide en nom d'hôte, aucun mail ne pourra être
# envoyé. Si le serveur d'e-mail est considéré comme actif (voir plus haut)
# et que le nom d'hôte est une chaîne vide, une erreur sera loggée.
nom_hote = ""

## Adresse mail de l'administrateur

# Les e-mails destinés à l'administrateur seront envoyés à cette adresse.
# Elle n'est pas nécessairement du même nom de domaine que le serveur, elle
# peut très bien être une adresse hotmail, gmail, yahoo...
admin_mail = "admin@kassie.fr"

## Noms de domaines interdits
# Cette option est utile pour interdire certains noms de
# domaines, principalement des serveurs d'adresses e-mails jetables.
# On ne peut pas créer un compte en précisant une adresse e-mail
# ilisant l'un de ces noms de domaine.
noms_domaines_interdits = [
    'prtnx.com',
    '20minutemail.com',
    '33mail.com',
    'anonymbox.com',
    'dispostable.com',
    'emailisvalid.com',
    'emailsensei.com',
    'matapad.com',
    'gishpuppy.com',
    'guerrillamailblock.com',
    'harakirimail.com',
    'harakirimail.se',
    'incognitomail.org',
    'jetable.org',
    'mailforspam.com',
    'mfsa.ru',
    'email-jetable.fr',
    'mail-temporaire.fr',
    'mailtemporaire.fr',
    'mail-temporaire.com',
    'mailtemporaire.com',
    'easy-trash-mail.com',
    'easytrashmail.com',
    'email-jetable.biz.st',
    'padpub.co.cc',
    'jetable.co.cc',
    'email-jetable.co.tv',
    'mail-jetable.co.tv',
    'padpub.co.tv',
    'jetable.cz.cc',
    'email-jetable.cz.cc',
    'mail-jetable.cz.cc',
    'email-temporaire.cz.cc',
    'mail-temporaire.cz.cc',
    'mailcatch.com',
    'nanozone.net',
    'mailhz.me',
    'mailhazard.com',
    'mailhazard.us',
    'binkmail.com',
    'suremail.info',
    'safetymail.info',
    'Mailnesia.com',
    'vipmailonly.info',
    'mailnull.com',
    'mailsac.com',
    'ruffrey.com',
    'mailtemp.net',
    'av.mintemail.com',
    'mmmmail.com',
    'mytempemail.com',
    'thankyou2010.com',
    'noclickemail.com',
    'randomail.net',
    'spambox.us',
    'spamfree24.org',
    'spamgourmet.com',
    'spamspot.com',
    'uroid.com',
    'tempemail.net',
    'tempinbox.com',
    'dingbone.com',
    'fudgerub.com',
    'lookugly.com',
    'smellfear.com',
    'tempsky.com',
    'trash-mail.com',
    'kurzpost.de',
    'objectmail.com',
    'proxymail.eu',
    'rcpt.at',
    'trash-mail.at',
    'trashmail.at',
    'trashmail.me',
    'wegwerfmail.de',
    'wegwerfmail.net',
    'wegwerfmail.org',
    'trashmail.ws',
    'mailimate.com',
    '1stw.com',
    'tonggen.com',
    '34nm.com',
    'yopmail.fr',
    'yopmail.net',
    'cool.fr.nf',
    'jetable.fr.nf',
    'nospam.ze.tc',
    'nomail.xl.cx',
    'mega.zik.dj',
    'speed.1s.fr',
    'courriel.fr.nf',
    'moncourrier.fr.nf',
    'monemail.fr.nf',
    'monmail.fr.nf',
    'mail.mezimages.net',
    'nice-4u.com',
]

"""
