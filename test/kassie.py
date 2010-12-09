# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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

import os
import time
import signal
import shutil
import subprocess
import re

#Liste permettant le lancement de Kassie avec les bons arguments
arg_kassie = ["python3","kassie.py", \
    "-p","14000", \
    "-c","{0}" + os.sep + "config", \
    "-e","{0}" + os.sep + "enregistrement", \
    "-l","{0}" + os.sep + "log"]

#Effectue la correspondance entre l'alias configurations et leur fichier
correspondance = { \
    "email" : "email" + os.sep + "serveur.cfg", \
    "globale" : "kassie.cfg", \
    }


class Kassie():
    """Classe représentant un serveur Kassie.
    Elle lance Kassie et permet sa configuration
    
    """
    
    def __init__(self,rep_kassie):
        """Construction des arguments pour la commande
        et création du dossier de kassie en le lançant"""
        self.process = None
        self.rep_kassie = rep_kassie
        self.arg_kassie = []
        for arg in arg_kassie:
            self.arg_kassie.append(arg.format(rep_kassie))
        self.start()
        self.stop()
    
    def __del__(self):
        """Arrète le serveur"""
        self.stop()
    
    def change(self,config,var,val):
        """Changer une option dans un fichier de configuration"""
        # Si on a une chaine de chractère on rajoute des "
        if isinstance(val,str):
            val = "\"" + val + "\""
        path = self.rep_kassie + os.sep + "config" + os.sep + \
            correspondance[config]
        text = open(path,'r').read()
        text = re.sub("{0} *=.*".format(var, val),"{0} = {1}".format(var, val),text)
        open(path,'w').write(text)
    
    def start(self):
        """Démarre le serveur"""
        if os.path.exists(self.rep_kassie + os.sep + "enregistrement"):
            shutil.rmtree(self.rep_kassie + os.sep + "enregistrement")
        if os.path.exists(self.rep_kassie + os.sep + "log"):
            shutil.rmtree(self.rep_kassie + os.sep + "log")
        path,_,_ = os.getcwd().rpartition(os.sep)
        path += "/src"
        self.process = subprocess.Popen(self.arg_kassie,
            stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE, \
            cwd=path)
        time.sleep(0.2)
    
    def get_retours(self):
        return self.process.communicate()
    
    def stop(self):
        """Arrète le serveur"""
        if self.process.poll() == None:
            self.process.kill()
            self.process.wait()
