TODO: update readmy (new commands + odt)

# sml-reader
Implementation example to read the sml (and odt) data via the d0 interface.

@Python 3.11
# CLI
## Detect 
### all ftdi devices
```commandline
python run.py detect all
```
### single ftdi device
```commandline
python run.py detect serial ftdiSerial
foo@bar:~$ python run.py detect serial EB1337051
```
## Meter
```<meter> => mt681, mt175, ehz, easy, dd3_sml, dd3_sml_2way, dd3_odt, dd3_odt_2way```
### log bytes to file
```commandline
python run.py <meter> log_bytes ftdiSerial
foo@bar:~$ python run.py mt175 log_bytes EB1337051
``` 
### log sml to cli
```commandline
python run.py <meter> log_cli ftdiSerial
foo@bar:~$ python run.py mt175 log_cli EB1337051
``` 
### log sml to file
```commandline
python run.py <meter> log_sml ftdiSerial
foo@bar:~$ python run.py mt175 log_sml EB1337051
``` 
### enter pin
```commandline
python run.py <meter> pin ftdiSerial pin
foo@bar:~$ python run.py mt175 pin EB1337051 [1,2,3,4]
``` 
### clear history data (only dd3 and easy meters)
#### topics
* e
* his
```commandline
python run.py <meter> clear ftdiSerial pin topic
foo@bar:~$ python run.py dd3 clear EB1337051 [1,2,3,4] e
``` 
### show (only dd3 and easy meters)
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
python run.py <meter> show ftdiSerial pin topic
foo@bar:~$ python run.py dd3 show EB1337051 [1,2,3,4] e
``` 
### toggle (only dd3 and easy meters)
#### topics
* info
* p
* pin
```commandline
python run.py <meter> toggle ftdiSerial pin topic
foo@bar:~$ python run.py dd3 toggle EB1337051 [1,2,3,4] info
``` 
### interactive mode
#### interactive commands
* short pulse -> .
* long pulse -> -
* pause -> _space_
* quit interactive mode -> exit
```commandline
python run.py <meter> interactive ftdiSerial pin
foo@bar:~$ python run.py dd3 interactive EB1337051 [1,2,3,4]
``` 
