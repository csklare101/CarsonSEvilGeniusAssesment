import pandas as pd
import geopandas as gpd
import shapely.geometry
import matplotlib.pyplot as plt
#using pandas/geopandas as it fits the data set well enough. Would consider other methods of solving point in polygon problems too if complexity was larger.
class ProcessGameState:
    df = pd.read_parquet('data\game_state_frame_data.parquet') #extracting parquet file using pandas
    lightBlue =  shapely.geometry.Polygon([(-1735,250), (-2024, 398), (-2806,742), (-2472, 1233), (-1565, 580)]) #

    def extract_weapons(self, w):
        ''' Will be used in getting the average time for bombsite b with 2 smgs or rifles
            Takes in a slice of a pandas data frame
            returns the slice as a list or nothing if None is inputed
        '''
        if w is not None:
            return w.tolist()[0]["weapon_class"] 
        return


    def lightBlueAvg(self, side, team):
        ''' Takes input for side and team
            returns the ammount of players that where in the light blue zone per round divided by the ammount of rounds counted, then multiplies by 100
        '''
        #Takes a slice from the main dataframe to make a dataframe of just the players from the inputed side and team
        testFrame = self.df.loc[(self.df['side'] == side) & (self.df['team'] == team)] 
        #Makes another slice to get the correct z axis values
        testFrame = testFrame[(testFrame['z'] > 285) & (testFrame['z'] < 421)]

        #GeoDataFrame to map the players x and y values
        gdf = gpd.GeoDataFrame(testFrame, geometry = gpd.points_from_xy(testFrame['x'], testFrame['y']))
        #narrows the dataframe down to the ones that where within the light blue zone
        gdf = gdf[gdf.geometry.within(self.lightBlue)]
        return len(gdf.groupby(['round_num'])) / len(testFrame.groupby(['round_num'])) * 100
    
    def bombsiteBAvg(self, side, team):
        ''' Takes input for side and team
            Returns the rounded average of the 'seconds' row from the testFrame
        '''
        #Takes a slice from the main dataframe to make a dataframe of just the players from the inputed side and team
        testFrame = self.df.loc[(self.df['side'] == side) & (self.df['team'] == team)]
        #Another slice to narrow it down to area BombsiteB
        testFrame = testFrame.loc[(testFrame['area_name'] == 'BombsiteB')]
        #used because pandas would give a warning about needing to use loc, not necessary for this code
        pd.options.mode.chained_assignment = None
        #applys the extract_weapons function on the sliced testFrame to make a new row weapons, a list of weapons from inventory.
        testFrame['weapons'] = testFrame['inventory'].apply(self.extract_weapons)

        def smgRifleCheck(weapons):
            ''' Takes in weapons input
                returns if the count of times a weapon is an "SMG" or "Rifle" is equal to or higher than 2
            '''
            count = 0
            for w in weapons:
                if w == "SMG" or w == "Rifle":
                    count += 1
            return count >= 2
        
        def elapsedTime(x):
            ''' Takes in a list of ints
                Returns elapsed time from subtracting max of the list to minimum of the list
            '''
            return max(x) - min(x)
        
        def weapons_group(weapons):
            ''' Takes in weapons row
                returns it as a list version
            '''
            return list(weapons)
        
        #using seconds variable for getting average time since it goes with the game's clock timer.
        #Groups the frame by team and round, then aggrigates the seconds using elapsedTime and weapons with weapons_group functions
        testFrame = testFrame.groupby(['team','round_num']).agg({'seconds': elapsedTime, 'weapons': weapons_group})
        #Makes a new row for checking if there are 2 or more rifles/smgs
        testFrame['smg_rifle_check'] = testFrame['weapons'].apply(smgRifleCheck)
        #filters the dataframe to only true values of smg_rifle_check
        testFrame = testFrame[testFrame['smg_rifle_check'] == True]
        #rounded answer for average seconds
        return round(testFrame['seconds'].mean())
        
    def playerHeatMap(self, side, team):
        ''' Takes input for side and team
            Saves and shows a pyplot of the heatmap relating to the frequency of x and y cordinates of the selected side and team near BombsiteB
        '''
        #Takes a slice from the main dataframe to make a dataframe of just the players from the inputed side and team
        testFrame = self.df.loc[(self.df['side'] == side) & (self.df['team'] == team)]
        #Another slice to narrow it down to area BombsiteB
        testFrame = testFrame.loc[(testFrame['area_name'] == 'BombsiteB')]

        #2d hexagonal vinning plot of the data frames x and y cordinates
        pc = plt.hexbin(testFrame['x'], testFrame['y'], gridsize=20, cmap="YlGn")
        pc.axes.set_title("Heatmap")
        pc.axes.set_xlabel("x")
        pc.axes.set_ylabel("y")
        pc.axes.set_aspect("equal")
        cb = plt.colorbar(ax=pc.axes)
        cb.set_label("Frequency of presence at location")

        #save file and show pyplot
        plt.savefig('Figure_1.png')
        plt.show()
