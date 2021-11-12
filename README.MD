# Movie-Theatre-Seating-Arrangement
Algorithm to implement seating arrangement in a movie theatre to maximize both customer satisfaction and theater utilization.

### Summary: 

Given a theatre with seating capacity of 20 seats in each of the 10 rows (200 seats).
This algorithm arranges the seats to maximize both customer satisfaction and customer safety. For the purpose of public safety, assume that a buffer of the three seats or one row is required.


### Input: 

An input file which would contain one line of input for each reservation request. The order of the lines in the file reflects the order in which the reservation requests were received. Each line in the file will be comprised of a reservation identifier, followed by a space, and then the number of seats requested. The reservation identifier will have the format: R####.
Example: 
R001 2 
R002 4 
R003 4 
R004 3


### Output: 

The program should output a file containing the seating assignments for each request. Each row in the file should include the reservation number followed by a space, and then a comma-delimited list of the assigned seats.
Example: 
R001 I1,I2
R002 F16,F17,F18,F19 
R003 A1,A2,A3,A4 
R004 J4,J5,J6


### Assumptions from the problem:

1. Cost of all the seats in the theatre are same. 
2. One theater for the above mentioned layout, row J is farthest from the screen and A is the closest to the screen.
3. Seats are reserved on the First come first serve. 
4. Customers who reserves the seat first are offered better seats (seats that are far from the screen). 
5. When no row is empty and only vacant seats need to be full filled reservation that suits the sattisfaction are selected.  
6. The maximum seats from a request cannot be greater than the total number of seats in the theater's row. 


### Approach to the solution: 

 1. The theatre is a double Linked List.
 2. Each Row is a node of the list.
 3. New rows are added when the seats to be reserved are greater than continguous seats empty in the row. 
    - If available seats in J are smaller than the seats requested a new node with name I is added to the linked list
 4. If the row is full, it is removed from the List and replaced with next row. We can't add more seats to the row
 5. Save all reserved seats to output hashmap then write to output.txt after.
 6. Save unsuccess reservation to noSafe list if the all the rows are full or cannot accomodate the rest of the reservation with the vacant seats. 
 
 
### Room for improvement: 
 1. Linked List can be replaced by Binary Search Tree where the root node is always the Last Row with Empty Seats. It will help to reduce the search time through the nodes. 
 2. Better seats are at middle of the threater
 3. Large seat booking reservation will be given more priority than small bookings. 
 

### Run the code
1. Make sure there is input file.
2. Open Terminal
3. Run ```python main.py <input_file>```

