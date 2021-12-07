import random
import math
import numpy as np
import InferentialStatistics as inf

""" Takes to sampledata objects and returns their covariance"""
def covarianceCalc(sampleD1,sampleD2):
    x = np.array(sampleD1.sample)
    y = np.array(sampleD2.sample)

    N = sampleD1.n
    if N != sampleD2.n:
        raise ValueError("Cannot calculate covariance of samples with different sizes")

    x = x - sampleD1.sampEstMean #As all x and y values need to be subtracted by their respective estimated means
    y = y - sampleD2.sampEstMean

    xyProducts = 0
    for ind,val in enumerate(x):
        xy = val*y[ind]
        xyProducts = xyProducts + xy
    covariance = xyProducts/sampleD1.n
    return covariance


"""Takes two sampledata objects and returns their correlation coefficient"""
def correlationCoefficientCalc(sampleD1,sampleD2):
    covxy = covarianceCalc(sampleD1,sampleD2)

    sigmax = sampleD1.popStandDev
    sigmay = sampleD2.popStandDev

    sigmaxy = sigmax * sigmay

    corrCoef = covxy/sigmaxy

    return corrCoef