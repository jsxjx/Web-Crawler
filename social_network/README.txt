********************** ABOUT THIS PROJECT *************************

I wrote this project about half year ago when I interned in HuaAT Data Tech Company. My supervisor was considering adding more data to our credit rating model and thought social network profile and relationship data might help. I was asked to scrap sample data set as some kind of pre experiment.

The programming itself is quite messy I have to say. This is my first programming project and I haven’t taken any programming class back then. I’m working on writing readable, testable and reusable program now.

********************** TAKE A LOOK AT THE RESULT****************

In “userAnalysis.csv” there are statistics of 400+ users. Such as: the percentage of their close friends having a degree from a distinguished university (see” 211/School” column,) the percentage of active users in their close friends. To collect these information, I need to go through 50000+ users profile.

“weiboUserNetwork.png” is a visualization result from Gephi, each dot represents a Weibo User, different colors of lines stand for different relationship types. The layout of the network also represents how important the relation between two dots is.

*********************** UNDERSTAND HOW IT WORKS *******************
WeiboEncode.py and Login.py were used for log in decoding process.