#!/usr/local/bin/python

"""Hook de pre-commit Git pour Windows.

Pour utiliser, placez-le dans le dossier .git/hooks en le renommant
en 'pre-commit' sans extension.

"""

import os
import sys

# On exécute les tests unitaires
os.chdir("src")
code = os.system(sys.executable + " runtest.py")
sys.exit(code)
