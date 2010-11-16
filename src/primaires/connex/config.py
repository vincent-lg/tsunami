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
# POSSIBILITY OF SUCH DAMAGE.


"""Ce fichier contient la configuration par défaut du module 'email'."""

cfg_connex = r"""
# Ce fichier contient la configuration du module primaire connex.
# Sont paramétrables diverses options liées à la connexion
# d'un client et la création de compte / personnage.


### Création d'un personnage

## Choix du nom du compte

# Chaîne à entrer pour créer un nouveau compte
# Par défaut, c'est simplement 'nouveau' mais vous pouvez lui donner un autre
# nom. Le client devra entrer cette chaîne pour créer un nouveau compte.
# Il ne pourra naturellement pas créer un compte avec ce nom.
# Evitez de modifier cette chaîne après le premier lancement de votre serveur.
# Certains comptes pourraient devenir inaccessibles, avec un peu de malchance.
chaine_nouveau = "nouveau"

# Noms interdits
# Cette liste contient les noms de compte considérés comme interdits
# Vous pouvez par exemple y ajouter le nom de votre projet
noms_interdits = ["kassie"]

## Protection du mot de passe

# Chiffrement du mot de passe
# Par défaut, le mot de passe est haché en sha256. Cette valeur ne peut être
# changée qu'avant la création du premier compte sur le serveur, car une
# modification en cours entraînerait une invalidité de tous les comptes déjà
# créés auparavant.
type_chiffrement = "sha256"

# Clef de salage
# Cette variable facultative sert à protéger les mots de passe d'un forçage
# par dictionnaire. Par défaut "salee_", c'est un préfixe ajouté devant le
# mot de passe juste avant de le hacher.
clef_salage = "salee_"


### Connexion

# Chaîne à entrer si on a oublié son mot de passe
# Par défaut, c'est simplement 'oubli' mais vous pouvez lui donner un autre
# nom. Le client devra entrer cette chaîne à la place de son mot de passe,
# un nouveau mot de passe lui sera envoyé.
# Evitez de modifier cette chaîne après le premier lancement de votre serveur.
# Certains comptes pourraient devenir inaccessibles, avec un peu de malchance.
chaine_oubli = "oubli"

# Paramétrages des avertissements
# Ces deux nombres configurent respectivement le nombre d'essais autorisés
# avant d'envoyer un message d'avertissement et de déconnecter le client.
# Au bout de 3 entrées erronées par défaut, le client est déconnecté et un mail
# automatique est envoyé au possesseur du compte ; au bout de 20 par défaut
# le mot de passe est réinitialisé et envoyé par mail. Dans les deux cas, un
# autre mail avertit l'admin principal.
nombre_avant_avertissement = 3
nombre_avant_nouveau = 20

"""
