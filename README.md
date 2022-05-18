# Norns_Fork
depot Norns installation Damien Skoraki
## Modification du Kernel Original
Le noyau original ne contient pas les modules permettant le bon fonctionnement du chapeau HIFIBERRY.

Il est donc nécessaire de recompiler le noyau afin d'ajouter le module.

à partir d'une realease NORNS :

###Récupération du noyau :
'''
git clone --depth=1 https://github.com/monome/linux
'''

###Installation des paquets de compilation 
'''
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install flex bison raspberrypi-kernel-headers
'''
