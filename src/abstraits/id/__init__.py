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


"""Ce package définit les objets et fonctions nécessaires à la manipulation
d'objets identifiées par des ID. La classe ObjetID, détaillée plus bas,
donne plus d'informations sur ces objets.

"""

from abstraits.objet_id.id import ID

class ObjetID:
    """Cette classe abstraite peut être héritée des objets qui souhaitent
    obtenir un identifiant unique, propre à chaque objet créé.

    Celui-ci se base sur deux données :
    -   une chaîne de caractère identifiant le groupe d'objets. Ce préfixe
        est nécessaire quand on souhaite grouper plusieurs objets dans
        une structure, un dictionnaire par exemple. Le module primaire parid
        associe un dictionnaire par groupe d'objet et cela permet de retrouver
        la classe concernée par le préfixe. Quand on souhaite créer
        un nouveau groupe, on doit hériter cette classe en lui donnant
        un nom de groupe qui sera utilisé pour chaque objet créé
    -   un entier identifiant clairement le numéro de l'objet. Cet entier
        s'incrémente à chaque fois que l'on créée un objet du groupe
    
    Exemple : 'salles:45' fait référence à un objet du groupe 'salles'
    (probablement une salle) dont le numéro identifiant est 45. Ainsi, on ne
    risque pas de le confondre avec 'joueurs:45'.
    
    """
    id_actuel = 1 # on compte à partir de 1
    groupe = "" # la chaîne contenant le nom du groupe préfixant l'ID
    
    def __init__(self):
        """Constructeur de la classe. On incrémente l'id_actuel du groupe.
        Dans le même temps, on crée un attribut nommé id dans l'objet
        manipulé. On associe à cet attribut un ID contenant le nom du groupe
        et l'identifiant entier le caractérisant.
        
        """
        self.id = ID(type(self).groupe, type(self).id_actuel)
        type(self).id_actuel += 1

# Fonctions liées à la manipulation de ces objets

def est_objet_id(objet):
    """Cette fonction renvoie True si l'objet manipulé est un ObjetID ou
    dérivé, False sinon.
    
    """
    return isinstance(objet, ObjetID)
