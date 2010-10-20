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


"""Ce package définit une classe abstraite BaseObj de laquelle TOUTES
les classes produisant des objets susceptibles d'être picklés, directement
ou indirectement, doivent être héritées.
Voir la documentation de la classe pour plus d'informations.

"""

class BaseObj:
    """Cette classe doit être une classe-mère de tous les objets
    susceptibles d'être enregistrés dans des fichiers grâce au module pickle,
    directement ou indirectement.
    
    Ne pas confondre avec abstraits.enr.ObjetEnr de laquelle toutes
    les classes susceptibles de produire des objets à enregistrer dans des
    fichiers doivent héritées. La classe présente est plus globale, car
    elle doit être, par exemple, utilisée pour chaque attribut d'un type non-
    natif si l'objet le contenant doit être à enregistrer.
    
    En somme, tous les attributs d'objet n'étant pas de type propre à Python
    doivent être hérités de cette classe. Les conteneurs, IDs, le doivent.
    
    """
    def a_sauver(self):
        """Méthode appelée lors du picklage de l'objet.
        On pickle la valeur de retour de cette méthode, self par défaut.
        Si on souhaite pickler autre chose, il suffit de le retourner.
        
        """
        return self
    
    def update(self, dct_attr):
        """Cette méthode doit être appelée lors du dépicklage de l'objet.
        On récupère un objet contenant certains attributs. Toutefois,
        depuis la dernière sauvegarde, les objets de ce type ont pu s'enrichir
        de nouveaux attributs, attributs qui doivent être présents pour que le
        projet tourne. Ainsi, on met à jour selon un schéma classique :
        -   si l'attribut existe dans l'objet, on n'y touche pas
        -   sinon, on l'écrit avec la valeur par défaut décrite dans
            le dictionnaire passé en paramètre
        
        dct_attr est un dictionnaire de la forme {nom_attr:valeur_par_defaut}
        
        Note: toutes les classes héritant de la classe BaseObj doivent :
        -   posséder un dictionnaire d'attribut / valeur par défaut présent
            en tête du fichier contenant la classe
        -   redéfinir la méthode update pour rediriger sur celle de cette
            classe, ce qui doit rendre un code comme celui-ci :
            
            def update(self):
                BaseObj.update(self, dct_base) # dictionnaire des attributs
        
        """
        dct_attr.update(self.__dict__)
        self.__dict__ = dct_attr
