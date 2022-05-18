# Norns_Fork
depot Norns installation Damien Skoraki
## Modification du Kernel Original
Le noyau original ne contient pas les modules permettant le bon fonctionnement du chapeau HIFIBERRY.
Il est donc nécessaire de recompiler le noyau afin d'ajouter le module.

à partir d'une realease NORNS :

[Images SD Norns](https://github.com/monome/norns-image/releases)

On flash une carte SD avec le logiciel Balena ETCHER : 

[Balena Etcher](https://www.balena.io/etcher/)

On etend la partition pour travailler à l'aise !
```
sudo raspi-config
```

### Récupération du noyau :

```
git clone --depth=1 https://github.com/monome/linux
```

### Installation des paquets de compilation 
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install flex bison raspberrypi-kernel-headers
```
