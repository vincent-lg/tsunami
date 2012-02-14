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


"""Fichier contenant la centralisation des statistiques dans un même objet."""

from abstraits.obase import BaseObj
from .dic_max import DicMax

class Stats(BaseObj):
    
    """Classe contenant les différentes statistiques du MUD.
    Ces stats sont enregistrées en fichier pour être rechargées en cas de
    redémarrage du module 'statistique'.
    On s'assure, avant de considérer les statistiques récupérées comme
    les statistiques 'actuelles' que le temps d'uptime est bien égal à celui
    de la session.
    
    Rappel : le temps d'uptime est conservé dans serveur.uptime. Cet attribut
    est renseigné à la création de l'objet serveur et indique depuis quand le
    MUD tourne. C'est ainsi un chiffre indépendant de tout chargement de
    module.
    
    """
    
    enregistrer = True
    def __init__(self, uptime):
        """Constructeur de l'objet"""
        BaseObj.__init__(self)
        self.uptime = uptime
        self.nb_commandes = 0
        self.tps_moy_commandes = None
        self.max_commandes = DicMax(3)
        
        # Watch Dog
        self.moy_wd = None
        self.nb_wd = 0
        self.dernier_wd = None
        self.max_wd = 0
    
    def __getnewargs__(self):
        return (None, )
    
    def surveiller_watch_dog(self, temps_actuel):
        """Ajoute le temps actuel comme statistique du Watch Dog.
        Le watch dog surveille le temps d'exécution moyen et maximum de
        l'exécution de la boucle principale du programme. C'est dans cette
        boucle que toutes les opérations sont faites (traitement des
        connexions, traitement des messages réceptionnés, gestion des actions
        différées...).
        
        Si tout va bien, le temps du WD ne doit pas être de beaucoup supérieur
        aux temps d'attente précisés pour atendre une connexion ou un message
        à réceptionner. Ces informations sont configurables dans le
        paramétrage du serveur. Si elles n'ont pas été modifiées, elles sont
        de 0.05s et 0.05s.
        Cela signifie que le WD moyen doit tourner autour de
        0.05 + 0.05 = 0.1s. Si il est bien plus élevé que 100 ms, il faudra
        chercher à savoir pourquoi.
        
        D'autre part, un WD élevé mais très ponctuel n'est pas très
        inquiétant. Peut-être qu'une commande met tout simplement un peu de
        temps à s'exécuter.
        
        """
        # d'abord, on cherche à savoir la différence avec le dernier temps
        if self.moy_wd is not None:
            diff = temps_actuel - self.dernier_wd
            self.moy_wd = (self.moy_wd * self.nb_wd + diff) / \
                    (self.nb_wd + 1)
            if diff > self.max_wd:
                self.max_wd = diff
        else:
            self.moy_wd = 0
        self.nb_wd += 1
        self.dernier_wd = temps_actuel
