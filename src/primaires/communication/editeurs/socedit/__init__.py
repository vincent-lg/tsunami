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


"""Package contenant l'éditeur 'socedit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package.

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Auquel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur import Editeur

class EdtSocedit(Editeur):
    
    """Classe définissant l'éditeur d'attitude 'socedit'.
    
    """
    
    nom = "socedit"
    
    def __init__(self, personnage, attitude):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        Editeur.__init__(self, instance_connexion, attitude)
        self.ajouter_option("aim", self.opt_aim)
        self.ajouter_option("aif", self.opt_aif)
        self.ajouter_option("oim", self.opt_oim)
        self.ajouter_option("oif", self.opt_oif)
        self.ajouter_option("adm", self.opt_adm)
        self.ajouter_option("adf", self.opt_adf)
        self.ajouter_option("idm", self.opt_idm)
        self.ajouter_option("idf", self.opt_idf)
        self.ajouter_option("odm", self.opt_odm)
        self.ajouter_option("odf", self.opt_odf)
        self.aide_courte = \
            "Editeur de social\n"
    
    def opt_aim(self, arguments):
        self.objet.independant["aim"] = arguments
   
    def opt_aif(self, arguments):
        self.objet.independant["aif"] = arguments
    
    def opt_oim(self, arguments):
        self.objet.independant["oim"] = arguments
    
    def opt_oif(self, arguments):
        self.objet.independant["oif"] = arguments
    
    def opt_adm(self, arguments):
        self.objet.independant["adm"] = arguments
   
    def opt_adf(self, arguments):
        self.objet.independant["adf"] = arguments
    
    def opt_idm(self, arguments):
        self.objet.independant["idm"] = arguments
   
    def opt_idf(self, arguments):
        self.objet.independant["idf"] = arguments
    
    def opt_odm(self, arguments):
        self.objet.independant["odm"] = arguments
    
    def opt_odf(self, arguments):
        self.objet.independant["odf"] = arguments