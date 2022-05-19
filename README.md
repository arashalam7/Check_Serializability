# Check_Serializability
Conflict - View - Result Serializability Checking

Arash Alam - M.Sc of Software student
Shahid Beheshti University

Project for Advanced DataBase and is about interleaved schedules between transactions 

input must be a text file like the examples uploaded.
The format is important.

for the define section of data :
data must come after '#'
data names must be lowercase
data values must be greater than zero so value > 0.

for the define section of operations :
operations must be between '<' and '>' sign
first index is: line number
second index is: transaction number
third index is: operate
fourth index is: the data used

note : 
open this root folder in environment and run .py file beside .txt files not seperated because python file can't fint .txt files.

2 types of operates :
1) math including : '*' , '/' , '-' , '+'
2) DataBase : R , W . means Read and Write. 
**attention : just define R and W nothing else for DB operates.

**Output :
Yes,No for checking Conflict,View,Result Serializability.
