import ProcessGameState
pgs = ProcessGameState.ProcessGameState()
f = open("assesment_output.txt", "w")
f.write("Percent of T side players on Team2 that where in the light blue zone: " + str(pgs.lightBlueAvg('T', 'Team2')) + "\n") #the light blue area is not commonly entered by the terriorst side on team 2
f.write("Average time in seconds of when Team2 on T side enters Bombsite B with least 2 rifles or SMGs: " + str(pgs.bombsiteBAvg('T','Team2'))) #average clock time is around 23 seconds
pgs.playerHeatMap('CT','Team2') #see Figure_1.png
#most common spots for CT side Team2 are around the areas (-800, 380), (-1005, 170), (-1137, 238), (-850, 480)
