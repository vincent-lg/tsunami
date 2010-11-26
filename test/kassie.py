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

#Liste permettant le lancement de Kassie avec les bons arguments
arg_kassie = ["python3","kassie.py", \
    "-p","14000", \
    "-c","../test/{0}/config", \
    "-e","../test/{0}/enregistrement", \
    "-l","../test/{0}/log"]

#Effectue la correspondance entre l'alias configurations et leur fichier
correspondance = { \
    "email" : "email/serveur.cfg", \
    "globale" : "kassie.cfg", \
    }


class Kassie():
    """Classe représentant un serveur Kassie.
    Elle lance Kassie et permet sa configuration
    
    """
    
    def __init__(self,rep_kassie):
        """Construction des arguments pour la commande
        et création du dossier de kassie en le lançant"""
        self.pid = None
        self.rep_kassie = rep_kassie
        self.arg_kassie = []
        for arg in arg_kassie:
            self.arg_kassie.append(arg.format(rep_kassie))
        self.start()
        time.sleep(0.1)
        self.stop()
    
    def __del__(self):
        """Arrète le serveur"""
        self.stop()
    
    def change(self,config,var,val):
        """Changer une option dans un fichier de configuration"""
        # Si on a une chaine de chractère on rajoute des "
        if isinstance(val,str):
            val = "\\\"" + val + "\\\""
        #Effectue un sed pour changer la valeur(pas beau)
        cmd = "sed -i \"s/^{0} *=.*$/{0} = {1}/\" {2}".format(var,val,
            self.rep_kassie + "/config/" + correspondance[config])
        os.system(cmd)
    
    def start(self):
        """Démarre le serveur"""
        if self.pid == None:
            if os.path.exists(self.rep_kassie + "/enregistrement"):
                shutil.rmtree(self.rep_kassie+ "/enregistrement")
            pid = os.fork()
            if pid == 0:
                c2pread, c2pwrite = os.pipe()
                os.close(1)
                os.dup(c2pwrite)
                os.chdir("../src")
                os.execvp(self.arg_kassie[0],self.arg_kassie)
                exit()
            else:
                self.pid = pid
                time.sleep(1)
    
    def stop(self):
        """Arrète le serveur"""
        if self.pid != None:
            os.kill(self.pid,signal.SIGKILL)
            self.pid = None
