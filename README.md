# Proof of concept for adding ibeacon technology to the system
Proof of concept for using ibeacon technology and proximity to choose a drink and trigger the sale. Due to not having access to the machine, the whole project was simulated on a linux virtual machine. The original forked project has been changed to an aproximation of what the future system with the implemented technology will look like. Certain parts have not been implemented and future testing is needed.

## Requirements
### Hardware requirements
- Bluetooth 4.0 or higher

## Installation
Run the install_libraries.sh script. It should install everything needed to test the scanner. Depending on the strength of the signal of your beacon and the Tx value that you choose the scanner might behave differently. Adjust the distance at which the sale is triggered accordingly.

## Testing the system
Run these programs in this order:
	1. sudo python3 bashloop.py
	2. python3 threadedgui.py
	3. python3 sender.py
	4. sudo python3 tmp_vend.py

The program starts to scan for nearby ibeacons. The tmp_vend.py process prints out the arriving packages and all the info related to them. The most important one to pay attention to is distance. Distance is the variable that when compared to a certain number triggers the sale. It depends heavily on the hardware, signal strength and beacon options chosen and should be adjusted accordingly.

Once the transaction starts it's success is simulated by typing in 'PAID' in the sender.py console.

----------------------------------------------------------------------------------------------------------------------------------------


# Dash point of sale embedded system
Point of sale embedded system based on Dash cryptocurrency. The whole project was done on a Raspberry Pi 3 model B+ with the original 7" touch screen running Raspbian Stretch OS. Based on moocowmoo's [dashvend](https://github.com/moocowmoo/dashvend) project

## Requirements
### Hardware requirements
- Raspberry Pi 3 model B+
- Raspberry Pi official 7" touch screen
- [Qibixx MDB Pi Hat](https://www.qibixx.com/en/products/mdb-pi-hat-interface/)
- External drive for blockchain storage
### Software requirements
- Raspbian Stretch OS

## Installation
The first thing to do is an update/upgrade:
```
sudo apt-get update && sudo apt-get upgrade
```
Position yourself in the root of the repository and run the make command.
```
make
```
Edit the [config](./bin/dashvend/config.py.template) file and set your variables.

Place the following commands in crontab:
```
@reboot python3 <path-to-dash-pos>/dash-pos/bin/start_dashvend.py
0 */1 * * * python3 <path-to-dash-pos>/dash-pos/bin/conversion/conversion_dash_hrk.py
```
Conversion only works for HRK (Croatian kunas)

### MDB
To get your Raspberry Pi to work with the Pi Hat follow this [official documentation](https://docs.qibixx.com/qibixx-documentation/pi-and-uarts).

### Display
If you want to use the original 7 inch touch screen in /etc/enviroment add the following line:
```bash
DISPLAY=:0
```
and in ~/.bashrc add the following line:
```bash
export DISPLAY=:0
```
In /boot/config.txt place the following lines:
```bash
display_rotate=1 # or different numbers depending on the orientation
```
Finally, in /etc/xdg/lxsession/LXDE-pi/autostart place the following lines:
```bash
@unclutter -idle 0 # remove mouse pointer
@<path-to-dash-pos>/dash-pos/bin/fliptouch.sh # flip the touch screen(change the script depending
					      # on your rotation
@xset s off # disable screen turn off after 10 minutes
@xset -dpms # disable screen turn off after 10 minutes
```

## Video demo
[Demonstration video](https://youtu.be/A7MZlR-G4GU)
