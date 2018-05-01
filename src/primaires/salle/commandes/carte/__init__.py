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


"""Package contenant la commande 'carte'."""

import time

from primaires.interpreteur.commande.commande import Commande

class CmdCarte(Commande):
    
    """Commande 'carte'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "carte", "map")
        self.nom_categorie = "bouger"
        self.groupe = "administrateur"
        self.schema = "(<options>)"
        self.aide_courte = "génère une carte"
        self.aide_longue = \
                "Sans paramètres, cette commande génère une carte standard c" \
                "entrée sur vous où chaque case est représentée par l'initia" \
                "le du nom de son terrain. Les options suivantes permettent " \
                "un contrôle plus fin (la syntaxe est celle des options de c" \
                "ommandes Unix) :                                           " \
                "                   +  -f ARG, --format=ARG Précise un forma" \
                "t (de 1, petit à 3, grand).             |  -t ARG, --taille" \
                "=ARG Précise la taille de la carte, càd le nombre de cases " \
                "  |                       affichées dans chaque direction a" \
                "utour de vous. Ce      |                       nombre doit " \
                "être strictement inférieur à 20.            |  -a ARG, --al" \
                "t=ARG    Force l'altitude de la carte (par défaut la vôtre)" \
                ".     |  -c ARG, --coords=ARG Permet de cartographier une z" \
                "one particulière :         |                       précisez" \
                " en argument les coordonnées de deux salles     |          " \
                "             sous la forme |cmd|x1.y1/x2.y2|ff| (en ommetta" \
                "nt les    |                       altitudes) et la carte gé" \
                "nérée sera un rectangle avec   |                       ces " \
                "salles pour angles.                                " \
"|  -e ARG, --ecrase=ARG Ecrase les salles cartographiées sur l'épaisseur       " \
"|                       spécifiée. Seule la plus haute salle d'une couche      " \
"|                       de ARG salles à partir de l'altitude sera affichée,    " \
"|                       ce qui permet d'aplatir certaines zones où le relief   " \
"|                       ne permet pas de visualiser correctement la carte.     " \
"|  -i, --interieur      Affiche l'état du flag dans chaque salle.              " \
"+  -s, --stats          Affiche quelques données sur la carte."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("options")
        nom_objet.proprietes["options_courtes"] = "'f:t:a:c:e:is'"
        nom_objet.proprietes["options_longues"] = "['format=', 'taille=', " \
                "'alt=', 'coords=', 'ecrase=', 'interieur', 'stats']"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        coords = personnage.salle.coords
        distance = 5
        altitude = coords.z
        nord = sud = est = ouest = 0
        epaisseur = 0
        nb_salles = 0
        terrains = []
        
        # Traitement des options
        if dic_masques["options"] is not None:
            options = dic_masques["options"].options
            if "format" in options:
                try:
                    format = int(options["format"]) - 1
                    assert format >= 0
                    distance = (5, 10, 15)[format]
                except (ValueError, IndexError, AssertionError):
                    personnage << "|err|Spécifiez un format existante " \
                            "(entre 1 et 3).|ff|"
                    return
            if "taille" in options:
                try:
                    distance = int(options["taille"])
                    assert distance > 0 and distance < 20
                except (ValueError, AssertionError):
                    personnage << "|err|La taille doit être un nombre " \
                            "valide et positif, inférieur à 20.|ff|"
                    return
            if "alt" in options:
                try:
                    altitude = int(options["alt"])
                except ValueError:
                    personnage << "|err|L'altitude doit être un entier.|ff|"
                    return
            if "coords" in options:
                try:
                    borne1, borne2 = options["coords"].split("/")
                    x1, y1 = borne1.split(".")
                    x2, y2 = borne2.split(".")
                    int(x1) + int(x2) + int(y1) + int(y2)
                except (ValueError, AssertionError):
                    personnage << "|err|Précisez des coordonnées valides.|ff|"
                    return
                else:
                    if x1 == x2 and y1 == y2:
                        personnage << "|err|Précisez deux salles " \
                                "distinctes.|ff|"
                        return
                    if abs(int(x1) - int(x2)) > 39 or \
                            abs(int(y1) - int(y2)) > 39:
                        personnage << "|err|Les dimensions d'est en ouest " \
                                "et du nord au sud doivent être inférieures " \
                                "à 40.|ff|"
                        return
                    if int(x1) <= int(x2):
                        ouest, est = int(x1), int(x2)
                    else:
                        ouest, est = int(x2), int(x1)
                    if int(y1) <= int(y2):
                        sud, nord = int(y1), int(y2)
                    else:
                        sud, nord = int(y2), int(y1)
            if "ecrase" in options:
                try:
                    epaisseur = int(options["ecrase"])
                    assert epaisseur > 1
                except (ValueError, AssertionError):
                    personnage << "|err|L'épaisseur d'écrasement doit être " \
                            "un nombre entier supérieur à 1.|ff|"
                    return
        
        # Construction de la carte
        str_map = ""
        a_salles = []
        for ajouter in importeur.salle.salles_a_cartographier:
            a_salles.extend(ajouter())
        # Si les coordonnées ne sont pas définies on les définit avec distance
        if not(ouest or est or nord or sud):
            ouest = int(coords.x) - distance
            est = int(coords.x) + distance
            nord = int(coords.y) + distance
            sud = int(coords.y) - distance
        lat = nord - sud + 1
        lon = est - ouest + 1
        # On parcourt les salles de la zone délimitée
        for y in range(lat):
            for x in range(lon):
                # On teste si une salle existe à ces coordonnées
                # Si une épaisseur est spécifiée, on teste toutes les salles
                # sur cette épaisseur en partant du haut
                salle = None
                if epaisseur:
                    for z in range(epaisseur):
                        try:
                            salle = type(self).importeur.salle[(ouest + x,
                                    nord - y, altitude + epaisseur - z - 1)]
                        except KeyError:
                            pass
                        else:
                            salle = (salle.nom_terrain, salle.interieur,
                                    (salle.coords.x, salle.coords.y))
                            break
                else:
                    try:
                        salle = type(self).importeur.salle[(ouest + x,
                                nord - y, altitude)]
                        salle = (salle.nom_terrain, salle.interieur,
                                (salle.coords.x, salle.coords.y))
                    except KeyError:
                        pass
                # La salle en question peut être un obstacle d'étendue
                for etendue in importeur.salle.etendues.values():
                    if (ouest + x, nord - y) in etendue:
                        point = etendue[(ouest + x, nord - y)]
                        if hasattr(point, "nom_terrain"):
                            salle = (point.nom_terrain, point.interieur,
                                    (point.coords.x, point.coords.y))
                        else:
                            salle = (point.nom, False, (ouest + x, nord - y))
                # Ou une salle ajoutée par un module secondaire
                for a_salle in a_salles:
                    if ouest + x == a_salle[2][0] and nord - y == a_salle[2][1]:
                        salle = a_salle
                
                if salle is None:
                    str_map += ". "
                else:
                    if salle[2][0] == round(personnage.salle.coords.x) and \
                            salle[2][1] == round(personnage.salle.coords.y):
                        str_map += "i "
                    else:
                        if "interieur" in options:
                            str_map += "o " if salle[1] else "n "
                        else:
                            str_map += salle[0][0] + " "
                # Statistiques
                if salle is not None:
                    nb_salles += 1
                    if salle[0] not in terrains:
                        terrains.append(salle[0])
        
        # Formattage de la carte
        titre = "Carte du monde entre {ouest}.{nord} et {est}.{sud}".format(
                ouest=ouest, nord=nord, est=est, sud=sud)
        larg = max(len(titre), lon * 2)
        marge = " " if larg == lon * 2 else ""
        f_map = "|tit|" + titre.center(larg) + "|ff|\n"
        while len(str_map) > 0:
            f_map += marge + str_map[:lon * 2].center(larg) + "\n"
            str_map = str_map[lon * 2:]
        if "stats" in options:
            f_map += \
                    "\nTaille de la carte du nord au sud : |rg|{ns}|ff|\n" \
                    ".................. d'est en ouest : |vr|{eo}|ff|\n" \
                    "Altitude : |bl|{alt}|ff|\n" \
                    "Epaisseur d'écrasement : |bc|{epaisseur}|ff|\n" \
                    "Nombre de salles affichées : |bc|{nb}|ff|\n" \
                    "Nombre de terrains différents : |bc|{ter}|ff|".format(
                    ns=nord - sud + 1, eo=est - ouest + 1, alt=altitude,
                    epaisseur=epaisseur, nb=nb_salles, ter=len(terrains))
        else:
            f_map = f_map.rstrip("\n")
        personnage << f_map
