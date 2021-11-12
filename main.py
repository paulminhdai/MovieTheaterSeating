import os, sys

ROWS, SEATPERROW = 10, 20 # numbers of rows and seats on each row
result = {} # dictionary to store the result

class Row: # Row class as a node of doubly linked list
    def __init__(self, name, seats, seatRequested, reservationID, currentRow):
        self.name = name # name of the row
        self.previous = currentRow # previous row node
        self.next = None      # next row node
        self.seatsInRow = [0 for i in range(seats)]     # seats in the row
        self.reserveSeats(seatRequested, reservationID) # reserving seats
        self.seatsVacant = self.countVacantSeats()    # number of vacant seats in the row

    def countVacantSeats(self):
        '''getting the vacant seats in the row'''
        count = 0
        for i in range(len(self.seatsInRow)):
            if self.seatsInRow[i] == 0: # if seat is vacant
                count += 1
        return count

    def reserveSeats(self, seatRequested, reservationID):
        '''adding the reservationID to the reserved seats'''
        currentReseverd = [] # list of reserved seats
        for i in range(len(self.seatsInRow)):
            if seatRequested != 0:
                if self.seatsInRow[i] == 0:
                    self.seatsInRow[i] = reservationID
                    seatRequested -= 1
                    currentReseverd.append(self.name + str(i + 1))
            else:
                break

        # adding the reserved seats to the result dictionary
        if reservationID not in result: 
            result[reservationID] = ",".join(currentReseverd)
        else:
            result[reservationID] += "," + ",".join(currentReseverd)
        return self.seatsInRow

NIL_NODE = Row('NIL', SEATPERROW, 0, 0, None) # NIL node

class TheatreArrangement:   # TheatreArrangement class as a doubly linked list
    def __init__(self, rows=10, seatsPerRow=20):
        self.totalRows = rows # total number of rows
        self.seatsPerRow = seatsPerRow # total number of seats per row
        self.seatsAvailable = self.totalRows * self.seatsPerRow # total number of seats available in the theatre
        self.root = NIL_NODE   # root node

    def confirmReservation(self, seatRequested, reservationID):
        '''check and make reservation'''
        ableToReserve = False
        if (seatRequested > self.seatsPerRow): # if seat requested is greater than seats per row
            return ableToReserve

        row = self.searchRow(seatRequested)
        if row == None and self.totalRows > 0: # if no row is available and there are still rows left
            self.addToRow(seatRequested, reservationID, self.seatsPerRow)
            ableToReserve = True
        elif row != None: # if row is available
            self.seatsAvailable -= seatRequested
            row.reserveSeats(seatRequested, reservationID)
            row.seatsVacant = row.countVacantSeats()
            self.delete(row)
            ableToReserve = True
        elif self.totalRows == 0: # if no row is available and there are no rows left
            return ableToReserve
        return ableToReserve

    def searchRow(self, seatRequested):
        '''Search available row'''
        if self.root.name != 'NIL':
            return self.__searchRowHelper(self.root, seatRequested)
        return None

    def __searchRowHelper(self, row, seatRequested):
        '''Recursive function to find available row for seat requested'''
        if seatRequested <= row.seatsVacant: # if seats are available in the row
            return row
        else: 
            if row.next != None: # if next row is exists
                return self.__searchRowHelper(row.next, seatRequested) # search next row
            else:
                return None

    def addToRow(self, seatRequested, reservationID, seats):
        '''Inserting the row to the linked list'''
        if self.root.name != 'NIL':  # if list is not empty
            newRow = self.__addToRowHelper(self.root, seatRequested, self.totalRows, reservationID)
            self.delete(newRow)
        else:  # add the first row to the linked list
            name = chr(self.totalRows + 64)
            self.root = Row(name, seats, seatRequested, reservationID, None)
            self.totalRows -= 1
            self.seatsAvailable -= seatRequested

    def __addToRowHelper(self, currentRow, seatRequested, totalRows, reservationID):
        '''Recursive function to insert the row to the linked list'''
        if seatRequested <= currentRow.seatsVacant: # if seats are available in the current row
            currentRow.seatsInRow = currentRow.reserveSeats(seatRequested, currentRow.reservationID)
            currentRow.seatsVacant = currentRow.countVacantSeats()
            self.seatsAvailable -= seatRequested
        elif seatRequested > currentRow.seatsVacant: # if seats are not available in the current row
            if(currentRow.next): # if next row is exists
                return self.__addToRowHelper(currentRow.next, seatRequested, totalRows, reservationID) # insert to the next row
            elif currentRow.next == None and totalRows > 0:  # create new row if next row is not exists and does not exceed the total number of rows
                self.seatsAvailable -= seatRequested
                name = chr(self.totalRows + 64)
                currentRow.next = Row(name, self.seatsPerRow, seatRequested, reservationID, currentRow)
                self.totalRows -= 1
        return currentRow.next

    def delete(self, currentRow):  # deleting the row from the linked list when the seats are full
        if currentRow.seatsVacant == 0: # if the row is full
            if currentRow == self.root and currentRow.next is not None: # if the row is the root and has a next node
                currentRow.next.previous= None
                self.root=currentRow.next
                return self.root
            elif currentRow != self.root: # if the row is not the root
                currentRow.previous.next=currentRow.next
                if currentRow.next != None: # if the row has a next node
                    currentRow.next.previous = currentRow.previous  # update the previous of the next node
                    return currentRow.previous
            else: # if the row is the root and has no next node
                self.root = NIL_NODE
                return self.root


def readInput(path):
    '''Read input file and return an array contains data'''
    if os.path.exists(path):
        reservations = []
        file = open(path,'r')
        capacity = ROWS * SEATPERROW # total seats in the theater
        for line in file:
            if capacity >= 0 :
                line = line.split()
                reservations.append([line[0], int (line[1])])
                capacity -= 1
            else:
                break
        return reservations
    else:
        raise Exception("File Not Found.")

def writeOutput(input, output):
    '''Write result to output.txt'''
    outfile = open("output.txt", 'w+')
    for reservations in input:
        if reservations[0] in output: # if reservation is successful
            outfile.write('{} {}\n'.format(reservations[0],output[reservations[0]]))
        # else: # if reservation is not successful
        #     outfile.write('{}\n'.format(reservations[0]))

if __name__ == '__main__':
    try:
        filePath = sys.argv[1] # file path from argument
    except FileNotFoundError as err:
        print(err)

    reservations = readInput(filePath) # read input file
    #reservations = [['R0001', 5, 3], ['R0002', 5, 1],['R0003', 5, 2], ['R0004', 1, 2]]
    reservations.sort(key=lambda x: x[2]) # sort the reservations by seat requested
    Theater1 = TheatreArrangement(ROWS, SEATPERROW) # create a new theater
    unsuccessList = [] # list to store the reservations which can't be accomodated

    for reservation in reservations:  # allocating group seats in same row
        if Theater1.seatsAvailable == 0:
            break
        if not Theater1.confirmReservation(reservation[1], str(reservation[0])): # if reservation is not successful
            unsuccessList.append(reservation[0])

    writeOutput(reservations, result) # write output to output.txt
    outputFilePath = os.getcwd() + '/' + 'outfile.txt' # output file path
    print('>>> {}\n'.format(outputFilePath))  # print output file path

    if unsuccessList: print("Unable to reserve for " + str(unsuccessList)) # print unsuccess reservation
