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


"""Package contenant la commande 'carte'."""

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
                "nérée sera un rectangle avec   " \
"|                       ces salles pour angles.                                " \
"+  -i, --interieur      Affiche l'état du flag dans chaque salle."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("options")
        nom_objet.proprietes["options_courtes"] = "'f:t:a:c:i'"
        nom_objet.proprietes["options_longues"] = "['format=', 'taille=', " \
                "'alt=', 'coords=', 'interieur', ]"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        coords = personnage.salle.coords
        distance = 5
        altitude = coords.z
        nord = sud = est = ouest = 0
        
        # Traitement des options
        if dic_masques["options"] is not None:
            options = dic_masques["options"].options
            if "format" in options:
                try:
                    format = int(options["format"]) - 1
                    assert format > 0
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
                    if int(x1) <= int(x2):
                        ouest, est = int(x1), int(x2)
                    else:
                        ouest, est = int(x2), int(x1)
                    if int(y1) <= int(y2):
                        sud, nord = int(y1), int(y2)
                    else:
                        sud, nord = int(y2), int(y1)
        
        # Construction de la carte
        str_map = ""
        # Si les coordonnées ne sont pas définies
        if not(ouest or est or nord or sud):
            ouest = coords.x - distance
            est = coords.x + distance
            nord = coords.y + distance
            sud = coords.y - distance
        lat = nord - sud + 1
        lon = est - ouest + 1
        for y in range(lat):
            for x in range(lon):
                try:
                    salle = type(self).importeur.salle[(ouest + x, nord - y,
                            altitude)]
                except KeyError:
                    str_map += ". "
                else:
                    if salle is personnage.salle:
                        str_map += "i "
                    else:
                        if "interieur" in options:
                            str_map += "o " if salle.interieur else "n "
                        else:
                            str_map += salle.nom_terrain[0] + " "
        
        # Formattage de la carte
        f_map = ""
        while len(str_map) > 0:
            f_map += str_map[:lon * 2] + "\n"
            str_map = str_map[lon * 2:]
        personnage << f_map
