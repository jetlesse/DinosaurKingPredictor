This is the folder which contains files with data that is used in the running of this application.
* TurnData: stores all the recorded turns in csv files
  * sorted by continent, location (as shown on the map) then name.csv
    * the name will often be robot_# for generic robot enemies where # is some descriptor or the #th robot you find in order
  * some locations such as Europe/South mean the overworld area you get to by leaving the Europe town from the south exit
* StringConversion/Dinos: stores all the names of dinosaurs encountered in this fight
  * sorted in the same way as TurnData
* StringConversion/Sayings: Stores all the known sayings the opponent can use in the fight
  * sorted in the same way as TurnData
* Models: saves the trained models for each fight so they can be used without re-compiling
  * sorted in the same way as TurnData