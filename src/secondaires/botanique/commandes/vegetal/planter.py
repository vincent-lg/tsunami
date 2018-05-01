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


"""Fichier contenant le paramètre 'planter' de la commande 'vegetal'."""

from random import random

from primaires.interpreteur.masque.parametre import Parametre

# Constantes
AIDE = """
Cette commande permet de planter un ou plusieurs végétaux, dans une
salle, répartis aléatoirement sur une zone et avec de nombreux
paramètres. Elle permet par exemple de planter entre 5 et 7 pommiers
dans les terrains forêt de la zone picte en les répartissant
équitablement. Elle permet aussi de planter un unique pommier dans
la salle où on se trouve.

Paramètres attendus : soit |cmd|-s|ff| pour définir la salle actuelle
soit d'autres informations pour définir la zone, le terrain et
éventuellement le mnémonique. Il faut également utiliser
l'option |cmd|-c|ff| qui doit être suivi de la clé du végétal à planter.

Détails des options :
    |cmd|-c|ff| (|cmd|--cle|ff|) [cle]
            Précise la clé du prototype de végétal à planter. Cette
            option est obligatoire.
    |cmd|-s|ff| (|cmd|--salle-courante|ff|)
            Plante le ou les végétaux dans la salle courante.
            Soit on utilise cette option, soit on doit préciser une
            zone avec l'option |cmd|-z|ff|.
    |cmd|-z|ff| (|cmd|--zone|ff|) [zone]
            Précise une zone dans laquelle les végétaux seront plantés.
            Les salles dans lesquelles planter seront choisies au hasard.
            Notez cependant que seuls les terrains récoltables seront
            sélectionnés, vous pouvez modifier la liste grâce à
            l'option |cmd|-t|ff|.
    |cmd|-m|ff| (|cmd|--mnemo|ff|) [mnemonique]
            Précise le début du mnémonique. Les salles dans la zone
            et dont le mnémonique commence par celui indiqué seront
            sélectionnées. Cette option peut être utile si vous
            voulez planter tous les sapins dans les salles commençant
            par le mnémonique 'foret' par exemple.
    |cmd|-t|ff| (|cmd|--terrains|ff|) [terrains]
            Précise un ou plusieurs terrains. Cette option permet de
            sélectionner un ou plusieurs terrains dans une zone
            spécifiée. On doit préciser le nom de terrain ou les
            différents terrains séparés par le pipe (_b_).
    |cmd|-n|ff| (|cmd|--nombre|ff|) [nombre]
            Précise le nombre de végétaux à planter. Ce nombre pourra
            être varié aléatoirement plus il est élevé.
    |cmd|-a|ff| (|cmd|--age|ff|) [age]
            Permet de mettre un âge par défaut pour tous nos végétaux
            à planter. Par défaut les végétaux apparaissent avec un
            âge de 0 (des graines, probablement).
""".strip()

class PrmPlanter(Parametre):

    """Commande 'vegetal planter'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "planter", "plant")
        self.schema = "<options>"
        self.aide_courte = "plante un végétal"
        self.aide_longue = AIDE

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        options = self.noeud.get_masque("options")
        options.proprietes["options_courtes"] = "'c:n:t:z:m:a:s'"
        options.proprietes["options_longues"] = "['cle=', 'nombre=', " \
                "'terrains=', 'zone=', 'mnemo=', 'age=', 'salle-courante']"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        # Paramètres par défaut
        salles = []
        nb_plantes = 1
        terrains = ["forêt", "plaine", "rive"]
        cle = ""
        age = 0
        zone = ""
        mnemo = ""

        # Traitement des options
        if dic_masques["options"] is not None:
            options = dic_masques["options"].options
            if "cle" in options:
                cle = options["cle"]
            if "nombre" in options:
                nombre = options["nombre"]
                try:
                    nombre = int(nombre)
                    assert nombre > 0
                except (ValueError, AssertionError):
                    personnage << "|err|Nombre invalide.|ff|"
                    return
                else:
                    nb_plantes = nombre
            if "terrains" in options:
                terrains = options["terrains"].split(",")
                terrains = [t.strip() for t in terrains if t.strip()]
            if "salle-courante" in options:
                salles = [personnage.salle]
                nb_plantes = 1
            if "zone" in options:
                zone = options["zone"]
            if "mnemo" in options:
                mnemo = options["mnemo"]
            if "age" in options:
                nombre = options["age"]
                try:
                    nombre = int(nombre)
                    assert nombre >= 0
                except (ValueError, AssertionError):
                    personnage << "|err|Nombre invalide.|ff|"
                    return
                else:
                    age = nombre

        # Convertion des terrains
        nom_terrains = terrains
        terrains = []
        for terrain in nom_terrains:
            try:
                terrain = importeur.salle.terrains[terrain]
            except KeyError:
                personnage << "|err|Terrain {} introuvable.|ff|".format(
                        terrain)
                return

            terrains.append(terrain)

        if not cle:
            personnage << "|err|Aucune clé de prototype végétal n'a " \
                    "été précisée.|ff|"
            return

        if not terrains:
            personnage << "|err|Aucun terrain n'a été défini.|ff|"
            return

        if zone:
            salles = list(importeur.salle.salles.values())

        salles = [s for s in salles if s.terrain in terrains]
        if not salles:
            personnage << "|err|Aucune salle n'a été trouvée.|ff|"
            return

        try:
            prototype = importeur.botanique.prototypes[cle]
        except KeyError:
            personnage << "|err|Prototype végétal {} inconnu.|ff|".format(
                    cle)
            return

        if not prototype.valide:
            personnage << "|err|Ce prototype n'est pas complet.\n" \
                "Il doit avoir au moins un cycle et chacun de " \
                "ses cycles doit avoir au moins\nune période.|ff|"
            return

        if zone:
            salles = [s for s in salles if s.nom_zone == zone]
            if not salles:
                personnage << "|err|Aucune salle n'est trouvée " \
                        "dans la zone spécifiée.|ff|"
                return

        if mnemo:
            salles = [s for s in salles if s.mnemonic.startswith(mnemo)]
            if not salles:
                personnage << "|err|Aucune salle n'est trouvée " \
                        "commençant par le mnémonique spécifié.|ff|"
                return

        # On plante maintenant les plantes dans les salles spécifiées
        nb = 0
        nb_par_salle = int(nb_plantes / len(salles))
        if nb_par_salle < 1:
            nb_par_salle = 1

        fact = nb_plantes / len(salles) * nb_par_salle
        for salle in salles:
            for i in range(nb_par_salle):
                if random() <= fact:
                    plante = importeur.botanique.creer_plante(prototype, salle)
                    plante.age = age
                    plante.ajuster()
                    plante.actualiser_elements()
                    nb += 1

        personnage << "{} plante(s) créée(s).".format(nb)
