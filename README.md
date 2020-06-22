# Pog_script

### setup

```
>>> make
>>> source ./env/bin/activate
```

or 

```
>>> virtualenv env
>>> source ./env/bin/activate
>>> pip3 install -e .
```

### how to run

* single run 

```
>>> pog -p data/185/2397OSR2020.psa
```
| Note: -p means the path to the file need to be converted

* batch run

```
>>> pog -p data/185/ -o output
```

| Note: -p means the path to the file need to be converted(will find all the psa files automatically), -o means the output folder (can be automatically generate)


### Example output format

| Note: find all possible combinations if it can combine together and combined them to one single shelf and list all the products in that shelf with essential informations.

* shelf_name is all the shelves' name that can be combined conctating with `*`

|shelf_name                                                                                                  |coordinate_x|coordinate_y|shelf_width|shelf_height|shelf_depth|merch_width|merch_height|merch_depth|
|------------------------------------------------------------------------------------------------------------|------------|------------|-----------|------------|-----------|-----------|------------|-----------|
|OPEN AIR COOLER DECK 4 FT - 102183 * OPEN AIR COOLER DECK 4 FT - 112184 * OPEN AIR COOLER DECK 4 FT - 122185|0.0         |0.0         |144.0      |1.25        |32.5       |144.0      |21.12       |32.5       |
| upc | number_of_facing_unit_wide |number_of_facing_unit_high | number_of_facing_unit_deep| 
|3410080741                                                                                                  |1           |2           |2          |            |           |           |            |           |
|3410007341                                                                                                  |1           |2           |2          |            |           |           |            |           |
|1820037030                                                                                                  |1           |2           |2          |            |           |           |            |           |
|1820027030                                                                                                  |1           |2           |2          |            |           |           |            |           |
|1820015030                                                                                                  |1           |2           |4          |            |           |           |            |           |
|1820061030                                                                                                  |1           |2           |2          |            |           |           |            |           |
|1820086031                                                                                                  |2           |2           |4          |            |           |           |            |           |
|3410001341                                                                                                  |1           |2           |2          |            |           |           |            |           |
|3410003341                                                                                                  |1           |2           |2          |            |           |           |            |           |
|1820096202                                                                                                  |1           |2           |2          |            |           |           |            |           |
|1820096550                                                                                                  |1           |3           |2          |            |           |           |            |           |
|1820096624                                                                                                  |1           |2           |2          |            |           |           |            |           |
|1820096721                                                                                                  |1           |3           |2          |            |           |           |            |           |
|1820005990                                                                                                  |1           |2           |3          |            |           |           |            |           |
|1820006991                                                                                                  |1           |2           |5          |            |           |           |            |           |


### |Note :  This is the first version, the format and information can be changed as required , if it needs to change, feel free to discuss :)
