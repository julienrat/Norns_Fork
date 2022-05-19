# Norns_Fork
Dépôt Norns - installation Damien Skoraki
L'idée principale est de forker l'officiel NORNS pour **la sublimer, la destructurer et la revisiter** avec un chapeau hifiberry DAC ADC Pro et des composants pas trop coûteux...
![Norns destructuré](https://github.com/julienrat/Norns_Fork/blob/main/images/norns_poc.jpg)
La doc du HIFIBERRY est ici : (https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/)

## Modification du Kernel Original
Le noyau original  de norns ne contient pas les modules permettant le bon fonctionnement du chapeau HIFIBERRY, mais contient les modules de l'ecran !

D'autres noyaux sont présents dans la distribution officielle de Norns .... mais sans les modules de l'écran !

D'où le casse tête ! donc 2 solutions !

- Recompiler un noyau vierge sur une install vierge au risque de louper des trucs en s'inspirant du [vieux tuto](https://github.com/okyeron/norns-image/wiki/1.-Norns-2.0-Full-Build-on-RasPi)
- Partir du  dernier noyau de l'installation y ajouter l'écran en bénéficiant des modules installés d'office pour ce noyau et garder tous les fichiers de config de l'installation en s'inpirant de ce [tuto vieux aussi :D](https://github.com/okyeron/norns-image/wiki/Reference:--Compile-OLED-display-drivers)

J'ai décidé de choisir la seconde option ! on pars de l'existant, on modifie le vieux tuto ! et si ça bouge ce sera facile d'upgrader une image des familles !

**DONC :**

À partir de la realease NORNS **norns 220306**  :

[Images SD Norns](https://github.com/monome/norns-image/releases)

On flash une carte SD avec le logiciel Balena ETCHER : 

[Balena Etcher](https://www.balena.io/etcher/)

### On se connecte en ssh
```
ssh we@<adresse_ip>
Mot de passe : sleep
```
On étend la partition pour travailler à l'aise !
```
sudo raspi-config
```
et on reboot !

### Installation des paquets de compilation 
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install flex bison raspberrypi-kernel-headers
sudo apt install build-essential fakeroot dpkg-dev perl libssl-dev bc gnupg dirmngr libncurses5-dev libelf-dev 
```
### On commente la derniere ligne du fichier /boot/config.txt
On va commenter cette ligne pour lancer la derniere version du kernel connue ! et non celle bidouillée par NORNS
```
#kernel=gnagnagna
```
et pendant qu'on est sur le fichier, on va commenter la ligne :
```
#dtoverlay=monome-snd-4271
```
et ajouter ces deux lignes pour utiliser la carte son du hifiberry adcplusdac-pro
```
dtoverlay=hifiberry-dacplusadcpro
force_eeprom_read=0
```
et on reboot ! et on jete un coup d'oeil sur la carte hifiberry, normalement les leds rouges doivent scintiller...

### Récupération du noyau pour compiler les modules:

```
git clone --depth=1 https://github.com/raspberrypi/linux
```



### On compile
on va récupérer les fichiers de config
```
cp /usr/src/linux-headers-$(uname -r)/Module.symvers .
cp /usr/src/linux-headers-$(uname -r)/.config .
```
ensuite on lance le menuconfig
```
make menuconfig
```
et on active l'écran !

```
Device Drivers  ---> Staging Drivers ---> Support for small TFT LCD display modules  --->
        <M>   SH1106 driver
        <M>   SSD1322 driver
```
et enfin on compile !
```
make -j4 prepare

make -j4 -C ~/linux SUBDIRS=drivers/staging/fbtft modules

```
on attends 3-4 heures ...

### Copie des modules et test
On va copier les modules compilés au bon endroit
```
sudo cp -v ~/linux/drivers/staging/fbtft/*.ko /lib/modules/$(uname -r)/kernel/drivers/staging/fbtft/

sudo depmod -a
```
et zou on teste !
```
sudo modprobe fbtft custom name=fb_ssd1322 debug=1 speed=16000000 gpios=reset:15,dc:14
dmesg
```

### On va tweaker !
L'écran est desormais monté sur /dev/fb1 au lieu de /dev/fb0, il va falloir modifier la configuration de **matron** interface graphique, pour rediriger l'affichage sur le bon point de montage :

On édite

```
nano ~/norns/matronrc.lua
```
et on change la ligne 2 pour pointer sur /dev/fb1

```
_boot.add_io('screen:fbdev', {dev='/dev/fb1'})
```
On reboot et voilà !
