# sml-reader
Implementation example to read the sml data via the d0 interface. Sample data included.

@Python 3.9
# cli
## detect 
### all ftdi devices
```commandline
python run.py detect all
```
### single ftdi device
```commandline
python run.py detect serial ftdiSerial
foo@bar:~$ python run.py detect serial EB_DE_PROT_3
```
## Meter: mt175
### log bytes to file
```commandline
python run.py mt175 logBytes ftdiSerial
foo@bar:~$ python run.py mt175 logBytes EB_DE_PROT_3
``` 
### log sml to cli
```commandline
python run.py mt175 logCli ftdiSerial
foo@bar:~$ python run.py mt175 logCli EB_DE_PROT_3
``` 
### log sml to file
```commandline
python run.py mt175 logSml ftdiSerial
foo@bar:~$ python run.py mt175 logSml EB_DE_PROT_3
``` 
### enter pin
```commandline
python run.py mt175 pin ftdiSerial pin
foo@bar:~$ python run.py mt175 pin EB_DE_PROT_3 [1,2,3,4]
``` 
## Meter: mt681
### log bytes to file
```commandline
python run.py mt681 logBytes ftdiSerial
foo@bar:~$ python run.py mt681 logBytes EB_DE_PROT_3
``` 
### log sml to cli
```commandline
python run.py mt681 logCli ftdiSerial
foo@bar:~$ python run.py mt681 logCli EB_DE_PROT_3
``` 
### log sml to file
```commandline
python run.py mt681 logSml ftdiSerial
foo@bar:~$ python run.py mt681 logSml EB_DE_PROT_3
``` 
### enter pin
```commandline
python run.py mt681 pin ftdiSerial pin
foo@bar:~$ python run.py mt681 pin EB_DE_PROT_3 [1,2,3,4]
``` 
## Meter: ehz
### log bytes to file
```commandline
python run.py ehz logBytes ftdiSerial
foo@bar:~$ python run.py ehz logBytes EB_DE_PROT_3
``` 
### log sml to cli
```commandline
python run.py ehz logCli ftdiSerial
foo@bar:~$ python run.py ehz logCli EB_DE_PROT_3
``` 
### log sml to file
```commandline
python run.py ehz logSml ftdiSerial
foo@bar:~$ python run.py ehz logSml EB_DE_PROT_3
``` 
### enter pin
```commandline
python run.py ehz pin ftdiSerial pin
foo@bar:~$ python run.py ehz pin EB_DE_PROT_3 [1,2,3,4]
``` 
## Meter: dd3
### log bytes to file
```commandline
python run.py dd3 logBytes ftdiSerial
foo@bar:~$ python run.py dd3 logBytes EB_DE_PROT_3
``` 
### log sml to cli
```commandline
python run.py dd3 logCli ftdiSerial
foo@bar:~$ python run.py dd3 logCli EB_DE_PROT_3
``` 
### log sml to file
```commandline
python run.py dd3 logSml ftdiSerial
foo@bar:~$ python run.py dd3 logSml EB_DE_PROT_3
``` 
### enter pin
```commandline
python run.py dd3 pin ftdiSerial pin
foo@bar:~$ python run.py dd3 pin EB_DE_PROT_3 [1,2,3,4]
``` 
### clear history data
#### topics
* e
* his
```commandline
python run.py dd3 clear ftdiSerial pin topic
foo@bar:~$ python run.py dd3 clear EB_DE_PROT_3 [1,2,3,4] e
``` 
### show
#### topics
* e
* 1d
* 7d
* 30d
* 365d
* info
* p
* pin
```commandline
python run.py dd3 show ftdiSerial pin topic
foo@bar:~$ python run.py dd3 show EB_DE_PROT_3 [1,2,3,4] e
``` 
### toggle
#### topics
* info
* p
* pin
```commandline
python run.py dd3 toggle ftdiSerial pin topic
foo@bar:~$ python run.py dd3 toggle EB_DE_PROT_3 [1,2,3,4] info
``` 
### interactive mode
#### interactive commands
* short pulse -> .
* long pulse -> -
* pause -> _space_
* quit interactive mode -> exit
```commandline
python run.py dd3 interactive ftdiSerial pin
foo@bar:~$ python run.py dd3 interactive EB_DE_PROT_3 [1,2,3,4]
``` 
## Meter: EasyMeter
### log bytes to file
```commandline
python run.py easy logBytes ftdiSerial
foo@bar:~$ python run.py easy logBytes EB_DE_PROT_3
``` 
### log sml to cli
```commandline
python run.py easy logCli ftdiSerial
foo@bar:~$ python run.py easy logCli EB_DE_PROT_3
``` 
### log sml to file
```commandline
python run.py easy logSml ftdiSerial
foo@bar:~$ python run.py easy logSml EB_DE_PROT_3
``` 
### enter pin
```commandline
python run.py easy pin ftdiSerial pin
foo@bar:~$ python run.py easy pin EB_DE_PROT_3 [1,2,3,4]
``` 
### clear history data
#### topics
* e
* his
```commandline
python run.py easy clear ftdiSerial pin topic
foo@bar:~$ python run.py easy clear EB_DE_PROT_3 [1,2,3,4] e
``` 
### show
#### topics
* e
* 1d
* 7d
* 30d
* 365d
* info
* p
* pin
```commandline
python run.py easy show ftdiSerial pin topic
foo@bar:~$ python run.py easy show EB_DE_PROT_3 [1,2,3,4] e
``` 
### toggle
#### topics
* info
* p
* pin
```commandline
python run.py easy toggle ftdiSerial pin topic
foo@bar:~$ python run.py easy toggle EB_DE_PROT_3 [1,2,3,4] info
``` 
### interactive mode
#### interactive commands
* short pulse -> .
* long pulse -> -
* pause -> _space_
* quit interactive mode -> exit
```commandline
python run.py easy interactive ftdiSerial pin
foo@bar:~$ python run.py easy interactive EB_DE_PROT_3 [1,2,3,4]
``` 
