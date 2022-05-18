# Norns_Fork
depot Norns installation Damien Skoraki
## Modification du Kernel Original
Le noyau original ne contient pas les modules permettant le bon fonctionnement du chapeau HIFIBERRY.
Il est donc nécessaire de recompiler le noyau afin d'ajouter le module.

à partir d'une realease NORNS :

[Images SD Norns](https://github.com/monome/norns-image/releases)

On flash une carte SD avec le logiciel Balena ETCHER : 

[Balena Etcher](https://www.balena.io/etcher/)

### On se connecte en ssh
```
ssh we@<adresse_ip>
Mot de passe : sleep
```
On etend la partition pour travailler à l'aise !
```
sudo raspi-config
```

### Récupération du noyau :

```
git clone --depth=1 https://github.com/raspberrypi/linux
```

### Installation des paquets de compilation 
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install flex bison raspberrypi-kernel-headers
sudo apt install build-essential fakeroot dpkg-dev perl libssl-dev bc gnupg dirmngr libncurses5-dev libelf-dev 
```
### On commente la derniere ligne du fichier /boot/config.txt
```
#kernel=gnagnagna
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
et on active l'ecran !

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
### Copie des modules et test
On va copier les modules au bon endroit
```
sudo cp -v ~/linux/drivers/staging/fbtft/*.ko /lib/modules/$(uname -r)/kernel/drivers/staging/fbtft/

sudo depmod -a
```
et zou on teste !
```
sudo modprobe fbtft_device custom name=fb_sh1106 debug=1 speed=2000000 gpios=reset:15,dc:14
sudo modprobe fbtft_device custom name=fb_ssd1322 debug=1 speed=16000000 gpios=reset:15,dc:14
```
