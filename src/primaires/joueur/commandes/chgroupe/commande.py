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


"""Fichier contenant le paramètre 'commande' de la commande 'chgroupe'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCommande(Parametre):
    
    """Commande 'groupe commande'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "commande", "command")
        self.schema = "<chemin_commande> <groupe_existant>"
        self.aide_courte = "change une commande de groupe"
        self.aide_longue = \
            "Utilisez cette commande pour changer une commande de " \
            "groupe. Si par exemple vous voulez rendre l'écriture de " \
            "mudmails accessibles aux joueurs, déplacez la commande " \
            "|cmd|messages|ff| dans le groupe |tit|joueur|ff| grâce à la " \
            "commande : %chgroupe% %chgroupe:commande% |cmd|messages " \
            "joueur|ff|. Il est préférable, quand vous ajoutez " \
            "une nouvelle commande au MUD, de la placer d'office " \
            "dans un groupe essentiel (|tit|pnj|ff|, |tit|joueur|ff| " \
            "ou |tit|administrateur|ff|). Une fois que la commande " \
            "a bien été ajoutée, vous pourrez la déplacer dans " \
            "le groupe final de destination. " \
            "Enfin, sachez qu'en déplaçant une commande, toutes ses " \
            "sous-commandes seront déplacées dans le même groupe. Pour "\
            "évitez cela, mettez un point (|cmd|.|ff|) après le nom de " \
            "votre commande. Si vous faites %chgroupe% %chgroupe:commande% " \
            "|cmd|messages. joueur|ff|, la commande |cmd|mail|ff| " \
            "sera déplacée mais aucun de ses paramètres. " \
            "Libre à vous de les transférer ensuite un à un pour " \
            "n'autoriser que certains paramètres aux " \
            "joueurs, tout en en laissant certains accessibles qu'aux " \
            "administrateurs."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        chemins = dic_masques["chemin_commande"].chemins
        nom_groupe = dic_masques["groupe_existant"].nom_groupe
        for chemin in chemins:
            type(self).importeur.interpreteur.groupes.changer_groupe_commande(
                    chemin, nom_groupe)
        
        nb_mod = len(chemins)
        s = ""
        if nb_mod > 1:
            s = "s"
        
        personnage << "{0} commande{s} déplacée{s} dans le groupe {1}.".format(
                nb_mod, nom_groupe, s=s)
