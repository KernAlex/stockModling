'''
Owner-Alexander Kern
This project is open to anyone

**** Dependencies
'''

class SPY:

    def __init__(self):

        self.__m = 0
        self.__b = 0
        self.__std = 0
        self.__todayPrice = 0
        self.__logy = []
        self.__numDays = 0
        self.__dates = []
        self.__findLinearFunction()

    def say_state(self):
        print("The current linear line is y = {}x + {}, and the standard deviation is {}".format(self.__m, self.__b, self.__std))

    def todays_deviation(self):
        fromMean = self.__logy[self.__numDays - 2] - (len(self.__logy) - 2)*self.__m - self.__b
        print("std: {}, price {} at {} distance".format(self.__std, self.__numDays, fromMean))


    def __findLinearFunction(self):
        '''
            Finds historical data for the spx from today to 5 years ago
        '''
        start, end = self.__get_dates_5year()
        #### Make array for "y" outputs
        y = self.__logy_outputs(start, end)
        self.__linear_coefficents(list(y))
        self.__find_standard_deviation(y)

    def __find_standard_deviation(self, y):
        y_prime = [i * self.__m + self.__b for i in range(len(y))]
        #### SD = sqrt( [sum(y - y')/(n-2)]  )
        y_sum = sum([(y[i] - y_prime[i])**2 for i in range(len(y))])/(len(y) - 2.0)
        from math import sqrt
        self.__std = sqrt(y_sum)

    def __linear_coefficents(self, y):
        import numpy as np
        A = np.array([[float(i), 1.0] for i in range(len(y))])
        y = A.T.dot(np.array(y))
        A = A.T.dot(A)
        y = np.linalg.inv(A).dot(y)
        self.__m = y[0]
        self.__b = y[1]

    def __get_dates_5year(self):
        from datetime import datetime
        end = datetime.today()
        end = datetime(end.year + 1, 1, 1)
        start = datetime(end.year - 5, 1, 1)
        return start, end

    def __logy_outputs(self, start, end):
        from iexfinance.stocks import get_historical_data
        import numpy as np
        data = get_historical_data("SPY", start, end)
        self.__dates = data.keys()
        y = []
        for i in data.keys():
            y += [np.log(data[i]['close'])]
        self.__logy = list(y)
        self.__numDays = len(y)
        self.__todayPrice = y[self.__numDays - 1]
        return y

    def plot_with_dev(self):
        import numpy as np
        import matplotlib.pyplot as plt
        plt.figure(1)
        plt.plot(self.__logy, 'k')
        line =  [i * self.__m + self.__b for i in range(self.__numDays)]
        plt.plot(line, 'r')
        plt.plot([i - self.__std for i in line], 'g')
        plt.plot([i + self.__std for i in line], 'g')
        plt.xticks(np.arange(0, self.__numDays, 250), [list(self.__dates)[i] for i in range(0, self.__numDays, 250)])
        plt.show()


if __name__ == '__main__':
    spx = SPY()
    spx.say_state()
    spx.todays_deviation()
    spx.plot_with_dev()