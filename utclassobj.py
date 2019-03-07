class UTClass:
    def __init__(self, unique, times, room, prof, status):
        self.unique = unique
        self.times = times
        self.room = room
        self.prof = prof
        self.status = status

    def findConflict(self, otherClass):
        pass

    def parseTime(self):
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
        return "Unique Number: " + self.unique + "\n"\
              + "Class Times: " + str(self.times) + "\n"\
              + "Room: " + self.room + "\n"\
              + "Instructor: " + self.prof + "\n"\
              + "Status: " + self.status + "\n"
