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


"""Ce fichier contient la configuration par défaut du module 'connex'."""

cfg_connex = r"""
# Ce fichier contient la configuration du module primaire connex.
# Sont paramétrables diverses options liées à la connexion
# d'un client et la création de compte / personnage.


### Connexion

## Chaîne à entrer si on a oublié son mot de passe
# Par défaut, c'est simplement 'oubli' mais vous pouvez lui donner un autre
# nom. Le client devra entrer cette chaîne à la place de son mot de passe,
# un nouveau mot de passe lui sera envoyé.
# Evitez de modifier cette chaîne après le premier lancement de votre serveur.
# Certains comptes pourraient devenir inaccessibles, bien que la probabilité
# soit faible.
chaine_oubli = "oubli"

## Paramétrages des avertissements
# Ces deux nombres configurent respectivement le nombre d'essais autorisés
# avant d'envoyer un message d'avertissement et de déconnecter le client.
# Au bout de 3 entrées erronées par défaut, le client est déconnecté et un
# e-mail automatique est envoyé au détenteur du compte.
# Au bout de 20 par défaut, le mot de passe est réinitialisé et envoyé par
# e-mail. Dans les deux cas, l'administrateur est avertir par e-mail.
# Les décompte sont remis à zéro lors d'une connexion réussi ou lors d'un
# changement de mot de passe.
nb_avant_alerte = 3
nb_avant_nouveau = 20

## Paramétrages des déconnexions et de l'attente
# Le premier nombre paramètre le nombre de tentatives pour rentrer un mot de
# passe avant d'être déconnecté. Le second paramètre le nombre de secondes
# à attendre avant une nouvelle entrée (3 secondes suffisent virtuellement à
# éviter le brute-forcing d'un compte).
nb_avant_deconnexion = 3
secondes_a_attendre = 3


### Création d'un compte

## Création autorisée
# En passant cette donnée de True à False, vous interdisez la création
# de nouveaux comptes. Cela veut dire que les seuls comptes
# auxquels on pourra se connecter seront ceux existants.
# Cependant, une connexion locale (c'est-à-dire depuis le serveur
# hébergeant le MUD) aura toujours le droit de créer des comptes.
# Ainsi, si vous voulez restreindre la création de compteg, mettez
# cette donnée à False, connectez-vous en local sur le MUD
# et créez les comptes de cette façon.
creation_autorisee = True

## Chaîne à entrer pour créer un nouveau compte
# Par défaut, c'est simplement 'nouveau' mais vous pouvez lui donner un autre
# nom. Le client devra entrer cette chaîne pour créer un nouveau compte.
# Il ne pourra naturellement pas créer un compte avec ce nom.
# Evitez de modifier cette chaîne après le premier lancement de votre serveur.
# Certains comptes pourraient devenir inaccessibles, avec un peu de malchance.
chaine_nouveau = "nouveau"

## Noms interdits
# Cette liste contient les noms de compte considérés comme interdits
# Vous pouvez par exemple y ajouter le nom de votre projet
noms_interdits = ["kassie"]

## Tailles minimum et maximum du nom de compte
taille_min = 3
taille_max = 15

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

# Taille minimum du mot de passe
pass_min = 6

## Nombre maximum de personnages
# Cette variable paramètre le nombre maximum de personnages pouvant être
# liés à un compte. Pour enlever cette limite, mettez à -1.
nb_perso_max = 5

## Fermeture du MUD aux comptes non autorisés
# Si l'option fermeture_filtree est à True, chaque compte devra être
# autorisé manuellement pour pouvoir se connecter, sauf le compte
# administrateur. Dans ce mode, aucune création de compte n'est
# possible par la voie habituelle.
fermeture_filtree = False

## Compte administrateur
# Sur Kassie, un nom de compte est retenu comme étant
# "le compte administrateur". Tous les joueurs créés dans ce compte seront dans
# le groupe des administrateurs.
# Cela vous permet de récupérer facilement le contrôle du MUD, au premier
# lancement du serveur ou par la suite.
# Pour des raisons de sécurité, évitez de choisir un nom comme "admin" ou
# le nom de votre MUD.
# Changez la valeur par défaut avant de lancer votre MUD.
compte_admin = "admin"

"""
