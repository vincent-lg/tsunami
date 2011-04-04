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


"""Ce package définit la classe Module, détaillée plus bas."""

# Statuts
INSTANCIE = 0
CONFIGURE = 1
INITIALISE = 2
DETRUIT = 3
ARRETE = 4

# Dictionnaire permettant de faire correspondre un statut à une chaîne
STATUTS = {
    INSTANCIE:"instancié",
    CONFIGURE:"configuré",
    INITIALISE:"initialisé",
    DETRUIT:"détruit",
    ARRETE:"arrêté",
}

class BaseModule:
    
    """Cette classe est une classe abstraite définissant un module, primaire
    ou secondaire.
    
    Chacun des modules primaires ou secondaires devra hériter de cette classe.
    Elle reprend les méthodes d'un module, appelées dans l'ordre :
    -   config : configuration du module
    -   init : initialisation du module (ne pas confondre avec le constructeur)
    -   ajouter_masque : ajout des masques propres au module
    -   ajouter_commandes : ajout des commandes propres au module
    -   preparer : préparation du module avant lancement
    -   detruire : destruction du module, appelée lors du déchargement
    -   arreter : arrêt COMPLET d'un module (n'est appelé qu'en cas
        d'arrêt contrôlé du programme)
    
    L'initialisation est la phase la plus importante. Elle se charge,
    en fonction de la configuration définie et instanciée dans config,
    de "lancer" un module. Si des actions différées doivent être mises en
    place pendant l'appel au module, elles doivent être créées dans cette
    méthode.
    
    La méthode 'preparer' est appelée juste après. Elle permet d'effectuer
    des actions d'initialisation mais en étant sûr que les objets des
    autres modules aient bien été chargées (voir la documentation de
    la méthode pour un exemple).

    La méthode detruire doit éviter de se charger de l'enregistrement des
    données. Il est préférable que cette opération se fasse en temps réel,
    quand cela est nécessaire (c'est-à-dire quand un objet a été modifié).
    En cas de crash, il se peut très bien que la méthode detruire ne soit pas
    appelée, le garder à l'esprit.
    
    D'autres méthodes génériques sont définies :
    -   boucle : appelée à chaque tour de boucle synchro, elle permet
        d'accomplir une certaine action le plus régulièrement possible

    On passe en paramètre du module l'importeur. Cela permet, pour un module,
    d'avoir accès à tous les autres modules chargés. Mais de ce fait,
    il est fortement déconseillé de faire référence à d'autres modules lors
    de la construction du module (méthode __init__).
    
    """
    
    def __init__(self, importeur, nom, m_type="inconnu"):
        """Constructeur d'un module.
        Par défaut, on lui attribue surtout un nom IDENTIFIANT, sans accents
        ni espaces, qui sera le nom du package même.

        Le type du module est soit primaire soit secondaire.

        """
        self.importeur = importeur
        self.nom = nom
        self.type = m_type
        self.statut = INSTANCIE

    def __str__(self):
        """Retourne le nom, le type et le statut du module."""
        return "{0} (type {1}), {2}".format(self.nom, self.type, \
                STATUTS[self.statut])

    def config(self):
        """Méthode de configuration.
        On charge ici la configuration.
        
        Note: cette méthode est également utilisée pour recharger la
        configuration. Si on doit faire certaines actions dans le cadre
        de la première configuration, se baser sur le statut qui doit être
        INSTANCIE. S'il est INITIALISE, cela signifie que le module
        a été configuré une fois au moins.

        """
        if self.statut == INSTANCIE:
            self.statut = CONFIGURE

    def init(self):
        """Méthode d'initialisation.
        Dans cette méthode, on se charge, en fonction de la configuration
        (éventuelle), de "lancer" le module. Tout ce qui est lancé dans
        cette méthode doit s'interrompre dans la méthode detruire.
        
        """
        self.statut = INITIALISE

    def ajouter_masques(self):
        """Ajoute les masques propres au module"""
        pass
    
    def ajouter_commandes(self):
        """Ajoute les commandes propres au module"""
        pass
    
    def preparer(self):
        """Cette méthode est appelée après l'initialisation,a vant
        le lancement de la boucle synchro.
        Elle peut permettre à un module de faire une vérification sur ses objets.
        
        Par exemple :
            Le module salle récupère des salles avec des listes de joueurs
            et NPCs présents dans chaque salle. Il serai préférable
            que chaque salle vérifie que tous les joueurs et NPCs présents
            soient toujours dans cette salle. Cette vérification ne pourrait
            se faire dans la méthode 'init' car c'est ici que les objets
            sont récupérés. Or, comment être sûr que les joueurs ont
            bien été récupérés au moment de la vérification ? Dans ce
            cas, il est donc préférable de redéfinir cette méthode
            qui prépare le module et ses objets avant le lancement
            de la boucle synchro.
        
        """
        pass
    
    def detruire(self):
        """Méthode de déchargement du module.
        On l'appelle avant l'arrêt du MUD (en cas de reboot total) ou
        si l'on souhaite décharger ou recharger complètement un module.
        
        """
        self.statut = DETRUIT
    
    def arreter(self):
        """Méthode d'arrêt du module.
        On l'appelle avant l'arrêt du MUD (en cas de reboot total).
        On ne l'appelle PAS si l'on souhaite recharger le module.
        
        """
        self.statut = ARRETE
    
    def boucle(self):
        """Méthode appelée à chaque tour de boucle synchro."""
        pass
    
    def traiter_commande(self, personnage, commande):
        """Méthode à redéfinir si on veut que le module traite des commandes
        hors interprétation.
        
        Par exemple, pour que les sorties d'une salles soient des commandes
        pour les joueurs, le module salle doit redéfinir cette méthode et
        y ajouter un traitement des commandes.
        
        On retourne True si le module a traité la commande, False sinon.
        
        """
        return False
    
    @property
    def str_statut(self):
        """Retourne le statut sous la forme d'une chaîne"""
        return STATUTS[self.statut]
