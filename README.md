# GDP per capita, constant PPP
version 18

##About
These are the official Gapminder's time-series for GDP per capita. This dataset combines two kinds of sources: 1. Long histroic trends and 2. Modern estimates form official contemporary sources. In this way we bridge the gap between the historic data and recent development, to be able to visualize a consistant history from the past to the present. This data changes when new estimates are made available, roughly on a yearly basis. If you find problems with the data or have any quesitons, please contact: https://getsatisfaction.com/gapminder/#problem

##Documentation version 18
The data for recent years (1990 - 2015) comes from the World Bank indicator: http://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD
The long historic trends are combined from historic records by Mattias Lindgren and documented here: https://www.gapminder.org/data/documentation/gd001/
The historic source is mainly based on Maddison data(http://www.ggdc.net/maddison/maddison-project/home.htm), which are not expressed in PPP 2011. We have used a rough method to adjust the historic trends, to hit the World Bank estimates of 1990. This method will be better documented in the future, and we are happy to explain it in detail upon request. But in rough terms we have made calculations that  maintain the total income growth of world over 200 years, as seen in Maddison's data. While we also adjust every countries trajectory so that it smoothly adjusts towards the level in World Bank data of 1990.

###Special cases
In order to give students a complete worldview, we don't want to leave any country out of our charts. Therefor we are forced to make rough estimates for countries with no official estimates from the World Bank.
* Cuba: World Bank has no estimates for Cuba after 2013. We let Cubas GDP per capita remain stable for 2014 & 2015, as we are not aware of any good source of data about it's most recent economic development.
* Syria: To estimate Syria's GDP per capita in constant 2011PPP, we have used the following sources:
a. GDP: IMF staff have guestimated the recent change in Real GDP in this working paper: wp16123.pdf http://bit.ly/2eNbOFr
b. Population: With the 4.8 Million People have fled the country according to http://www.unocha.org/syria, and roughly half a million war-fatalities. This gives us a rough estimate of the current population inside the country, of roughly 5.1 Million people.
Based on these changes of the nominator and the denominator of GDP per capita, we get an estimate of GDP per capita in 2015; at aproximatly 3500 PPP2011 dollars.
