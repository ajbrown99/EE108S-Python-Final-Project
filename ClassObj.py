class UTClass:
    def __init__(self, name, unique, times, room, prof, status):
        self.name = name
        self.unique = unique
        self.times = times
        self.room = room
        self.prof = prof
        self.status = status

    def findConflict(self, otherClass):
        """
        Compares the given class with this class and see if there is a schedule conflict.
        """

        if self.name == otherClass.name:
            print("Can't take two of the same class.")
            return True

        parsedTime = self.parseTime()
        otherParsedTime = otherClass.parseTime()

        for i in parsedTime:
            for j in otherParsedTime:
                if i[0] == j[0] and (min(i[1][1], j[1][1]) - max(i[1][0], j[1][0]) > 0):
                    return True
        return False

    def parseTime(self):
        """
        Parses the raw string representing class time and put it into a simpler format to calculate with
        """

        days = self.times[0]
        hour = self.times[1]

        daysList = []
        hoursList = []

        for i in range(len(days)):
            daysRet = []
            spl = days[i].split("H")
            for day in spl:
                if day:
                    lst = list(day)
                    if day != spl[-1]:
                        lst[-1] = lst[-1] + "H"
                    daysRet += lst
            daysList.append(daysRet)

            startEnd = hour[i].split("-")
            starting = [int(num) for num in startEnd[0][:len(startEnd[0]) - 5].split(":")]
            ending = [int(num) for num in startEnd[1][:len(startEnd[1]) - 5].split(":")]
            startingTime = (starting[0] + 12) * 60 + starting[1] if startEnd[0][-4] == "p" and starting[0] != 12 else starting[0] * 60 + starting[1]
            endingTime = (ending[0] + 12) * 60 + ending[1] if startEnd[1][-4] == "p" and ending[0] != 12 else ending[0] * 60 + ending[1]
            hourInterval = [startingTime, endingTime]

            hoursList.append(hourInterval)

        classSchedule = []
        for i in range(len(daysList)):
            for j in range(len(daysList[i])):
                classSchedule.append([daysList[i][j], hoursList[i]])

        return classSchedule

    def __str__(self):
        """
        String representation of a UT class.
        """

        return "Name: " + self.name + "\n"\
              + "Unique Number: " + self.unique + "\n"\
              + "Class Times: " + str(self.parseTime()) + "\n"\
              + "Room: " + self.room + "\n"\
              + "Instructor: " + self.prof + "\n"\
              + "Status: " + self.status + "\n"
