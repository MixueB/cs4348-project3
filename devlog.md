# 11/29/24 8:42 PM
To start this project I have set up my Git repository through Github. I've checked the project description and have been thinking about how to divide up the pieces of the project. To start with today I will create the main menu for the project in Python. Each session I will work on another divided piece of the project.

# 11/30/24 10:25 AM
Today I am planning to write a parser class to read the index files. I will also create a heap class to parse the index file into. I will test this separately before integrating with the menu from yesterday. For testing I will use the sample.idx file.

# 11/30/24 7:25 PM 
Parsing the file was more difficult than expected. It took a lot of time to parse the bytes in the right spot correctly. The program kept crashing due to parsing into the wrong spot but is now working correctly. Next I will work on connecting the menu to the btree.

# 12/1/24 10:43 AM
I have started to work on implementing the B Tree functionality and am hoping to finish by later today. Once the B Tree functions are implemented I will also integrate the menu in project3.py.

# 12/2/24 6:02 PM
I have implemented the other menu command functions that were not implemented yesterday. While testing I realized that some of my B Tree functionality was not working correctly, so I fixed this today as well. I initially did not understand what the minumum degree means for the tree but understand now. I will continue to test throughout the week.

# 12/3/24 9:25 PM
After more testing today I am happy with my implementation. I tested again with the sample.idx file and did not encounter any issues. I created several other index files for testing and tried different combinations of commands. Today I will add the readme to go over how to run my application.