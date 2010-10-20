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


"""Ce fichier définit la classe Module, détaillée plus bas."""

# Statuts
INSTANCIE = 0
CONFIGURE = 1
INITIALISE = 2
DETRUIT = 3

# Dictionnaire permettant de faire correspondre un statut à une chaîne
STATUTS = {
    INSTANCIE:"instancié",
    CONFIGURE:"configuré",
    INITIALISE:"initialisé",
    DETRUIT:"détruit",
}

class Module:
    """Cette classe est une classe abstraite définissant un module, primaire
    ou secondaire.
    
    Chacun des modules primaires ou secondaires devra hériter de cette classe.
    Elle reprend les méthodes d'un module, appelée dans l'ordre :
    -   config : configuration du module
    -   init : initialisation du module (ne pas confondre avec le constructeur)
    -   detruire : destruction du module, appelée lors du déchargement
    
    L'initialisation est la phase la plus importante. Elle se charge,
    en fonction de la configuration définie et instanciée dans config,
    de "lancer" un module. Si des actions différées doivent être mises en
    place pendant l'appel au module, elles doivent être créées dans cette
    méthode.

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
    
    De même, on passe le parser de commande pour avoir la liste des options
    précisées par l'utilisateur.

    """
    def __init__(self, importeur, parser_cmd, nom, m_type="inconnu"):
        """Constructeur d'un module.
        Par défaut, on lui attribue surtout un nom IDENTIFIANT, sans accents
        ni espaces, qui sera le nom du package même.

        Le type du module est soit primaire soit secondaire.

        """
        self.importeur = importeur
        self.parser_cmd = parser_cmd
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
        INSTANCIE. Si il est INITIALISE, cela signifie que le module
        a été configuré une fois au moins.

        """
        if self.statut == INSTANCIE:
            self.statut = CONFIGURE

    def init(self):
        """Méthode d'initialisation.
        Dans cette méthode, on se charge, en fonction de la configuration
        (éventuelle), de "lancer" le module. Tout ce qui est lancé dans
        cette méthode doit s'interrompre dans la méthode destroy.
        
        """
        self.statut = INITIALISE

    def detruire(self):
        """Méthode d'arrêt ou de déchargement du module.
        On l'appelle avant l'arrêt du MUD (en cas de reboot total) ou
        si l'on souhaite décharger ou recharger complètement un module.
        """
        self.statut = DETRUIT
    
    def boucle(self):
        """Méthode appelée à chaque tour de boucle synchro."""
        pass

