import random
import math
import statistics

#Class for samples
class sampleDataSet:
    def __init__(self,initSample,initIsPopulation = False,initSampleSize = 0, initIsProportion = False,initAlpha = 0):
        #Settings
        self.alpha = initAlpha #For calculating the C.I %
        self.population = initIsPopulation #The population from which samples are taken
        self.sampleSize = initSampleSize #Sample size for random sample generation
        self.isProportion = initIsProportion #Whether or not we're dealing with proportions

        #Sample data
        self.sample = initSample
        if self.population != False and self.sampleSize != 0: #Calculates random sample
            self.simpleRandomSample()
        self.n = len(self.sample)

        #Central tendency
        self.sampEstMean = 0
        self.calcMean()

        #Proportion
        if self.isProportion == True:
            self.pino = (self.sampEstMean*self.n+2)/(self.n+4)  # "P med bølge over" til Agretsi Coulle
            self.nino = (self.n +4)


        #Samp Dispersion
        self.sampStandDev = 0
        self.calcStandDev()
        self.sampVar = self.sampStandDev**2

        #Inferential stats
        self.standErrMean = 0
        self.calcStandErrMean()
        self.confI = 0
        self.calcConfI()

    #Laver en liste med n antal tilfældige elementer fra populationen
    def simpleRandomSample(self):
        randomSample = []
        for x in range(self.sampleSize):
            randomSample = randomSample + [self.population[random.randint(min(self.population), max(self.population)-1)]]
        self.sample = randomSample

    #Beregner mean
    def calcMean(self):
        self.sampEstMean = sum(self.sample) / len(self.sample)


    #Beregner variance på baggrund af et sample
    def calcStandDev(self):
        if self.isProportion == True:
            self.sampStandDev = math.sqrt(self.sampEstMean*(1-self.sampEstMean)) #sqrt(p*(1-p))
        else:
            self.sampStandDev = math.sqrt((1/(self.n-1)) * sum([(x - self.sampEstMean)**2 for x in self.sample]))

    def calcStandErrMean(self):
        self.standErrMean = self.sampStandDev/math.sqrt(self.n)

    def calcConfI(self,isTScore = False):
        if self.alpha != 0:
            ratio95 = self.alpha
        else:
            ratio95 = 1.96

        self.confI = ratio95*self.standErrMean


        if (0.9<self.confI or self.confI<0.1) & (self.isProportion == True) and self.alpha == 0: #Agretsi-Coulle
            self.standErrMean = math.sqrt((self.pino *(1-self.pino)/self.nino))
            self.confI = ratio95 * self.standErrMean

        self.cInterval = [self.sampEstMean - self.confI, self.sampEstMean + self.confI]



    #Beregner variance på baggrund af en population
    def popVariance(sample):
        sampleMean = calcMean(sample)
        diffSampleMeanxSquared =  [(x - sampleMean)**2 for x in sample]
        sumDiffSampleMeanxSquared = sum(diffSampleMeanxSquared)
        diffi = 1/len(sample)
        sampleVariance = (math.sqrt(diffi*sumDiffSampleMeanxSquared))**2
        return sampleVariance


    #Beregner variance vha. Populationens variance
    def sampleVarianceFromPop(population,sample):
        sampleVarFrompop = popVariance(population)/len(sample)
        return sampleVarFrompop



population = [1,1,0,0,0,0,1,0]
gruppe1 = [1,1,0,1]
gruppe2 = [0,0,0,0]


t_3 = 2.920  #T-value, hvis sample size er 3
t_4 = 2.353  #T-value, hvis sample size er 4
t_6 = 2.015  #T-value, hvis sample size er 6

calc1 = sampleDataSet(gruppe1, initIsProportion=True, initAlpha=t_4)
calc2 = sampleDataSet(gruppe2, initIsProportion=True,initAlpha=t_4)
calc3 = sampleDataSet(population)

print(calc1.sampEstMean)
print(calc1.standErrMean)
print(f"95% coverage confidence interval: {calc1.sampEstMean} +/- {calc1.confI}")
print(calc1.cInterval)
print("\n")


print(calc2.sampEstMean)
print(calc2.standErrMean)
print(f"95% coverage confidence interval: {calc2.sampEstMean} +/- {calc2.confI}")
print(calc2.cInterval)
print("\n")
