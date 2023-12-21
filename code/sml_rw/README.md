# sml-reader
Implementation example to read the sml data via the d0 interface. Sample data included.

@Python 3.11
# cli
## detect 
### all ftdi devices
```commandline
python run.py detect all
```
### single ftdi device
```commandline
python run.py detect serial ftdiSerial
foo@bar:~$ python run.py detect serial EB1337051
```
## Meter: mt175
### log bytes to file
```commandline
python run.py mt175 log_bytes ftdiSerial
foo@bar:~$ python run.py mt175 log_bytes EB1337051
``` 
### log sml to cli
```commandline
python run.py mt175 log_cli ftdiSerial
foo@bar:~$ python run.py mt175 log_cli EB1337051
``` 
### log sml to file
```commandline
python run.py mt175 log_sml ftdiSerial
foo@bar:~$ python run.py mt175 log_sml EB1337051
``` 
### enter pin
```commandline
python run.py mt175 pin ftdiSerial pin
foo@bar:~$ python run.py mt175 pin EB1337051 [1,2,3,4]
``` 
## Meter: mt681
### log bytes to file
```commandline
python run.py mt681 log_bytes ftdiSerial
foo@bar:~$ python run.py mt681 log_bytes EB1337051
``` 
### log sml to cli
```commandline
python run.py mt681 log_cli ftdiSerial
foo@bar:~$ python run.py mt681 log_cli EB1337051
``` 
### log sml to file
```commandline
python run.py mt681 log_sml ftdiSerial
foo@bar:~$ python run.py mt681 log_sml EB1337051
``` 
### enter pin
```commandline
python run.py mt681 pin ftdiSerial pin
foo@bar:~$ python run.py mt681 pin EB1337051 [1,2,3,4]
``` 
## Meter: ehz
### log bytes to file
```commandline
python run.py ehz log_bytes ftdiSerial
foo@bar:~$ python run.py ehz log_bytes EB1337051
``` 
### log sml to cli
```commandline
python run.py ehz log_cli ftdiSerial
foo@bar:~$ python run.py ehz log_cli EB1337051
``` 
### log sml to file
```commandline
python run.py ehz log_sml ftdiSerial
foo@bar:~$ python run.py ehz log_sml EB1337051
``` 
### enter pin
```commandline
python run.py ehz pin ftdiSerial pin
foo@bar:~$ python run.py ehz pin EB1337051 [1,2,3,4]
``` 
## Meter: dd3
### log bytes to file
```commandline
python run.py dd3 log_bytes ftdiSerial
foo@bar:~$ python run.py dd3 log_bytes EB1337051
``` 
### log sml to cli
```commandline
python run.py dd3 log_cli ftdiSerial
foo@bar:~$ python run.py dd3 log_cli EB1337051
``` 
### log sml to file
```commandline
python run.py dd3 log_sml ftdiSerial
foo@bar:~$ python run.py dd3 log_sml EB1337051
``` 
### enter pin
```commandline
python run.py dd3 pin ftdiSerial pin
foo@bar:~$ python run.py dd3 pin EB1337051 [1,2,3,4]
``` 
### clear history data
#### topics
* e
* his
```commandline
python run.py dd3 clear ftdiSerial pin topic
foo@bar:~$ python run.py dd3 clear EB1337051 [1,2,3,4] e
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
foo@bar:~$ python run.py dd3 show EB1337051 [1,2,3,4] e
``` 
### toggle
#### topics
* info
* p
* pin
```commandline
python run.py dd3 toggle ftdiSerial pin topic
foo@bar:~$ python run.py dd3 toggle EB1337051 [1,2,3,4] info
``` 
### interactive mode
#### interactive commands
* short pulse -> .
* long pulse -> -
* pause -> _space_
* quit interactive mode -> exit
```commandline
python run.py dd3 interactive ftdiSerial pin
foo@bar:~$ python run.py dd3 interactive EB1337051 [1,2,3,4]
``` 
## Meter: EasyMeter
### log bytes to file
```commandline
python run.py easy log_bytes ftdiSerial
foo@bar:~$ python run.py easy log_bytes EB1337051
``` 
### log sml to cli
```commandline
python run.py easy log_cli ftdiSerial
foo@bar:~$ python run.py easy log_cli EB1337051
``` 
### log sml to file
```commandline
python run.py easy log_sml ftdiSerial
foo@bar:~$ python run.py easy log_sml EB1337051
``` 
### enter pin
```commandline
python run.py easy pin ftdiSerial pin
foo@bar:~$ python run.py easy pin EB1337051 [1,2,3,4]
``` 
### clear history data
#### topics
* e
* his
```commandline
python run.py easy clear ftdiSerial pin topic
foo@bar:~$ python run.py easy clear EB1337051 [1,2,3,4] e
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
foo@bar:~$ python run.py easy show EB1337051 [1,2,3,4] e
``` 
### toggle
#### topics
* info
* p
* pin
```commandline
python run.py easy toggle ftdiSerial pin topic
foo@bar:~$ python run.py easy toggle EB1337051 [1,2,3,4] info
``` 
### interactive mode
#### interactive commands
* short pulse -> .
* long pulse -> -
* pause -> _space_
* quit interactive mode -> exit
```commandline
python run.py easy interactive ftdiSerial pin
foo@bar:~$ python run.py easy interactive EB1337051 [1,2,3,4]
``` 
