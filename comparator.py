from numpy import dot 
from numpy.linalg import norm


def verify(saved_vector, sample_vector, threshold):
    """ Calculates cosine similarity between two vectors 
    and verifies or not depending on given threshold value"""

    similarity = dot(saved_vector, sample_vector)/(norm(saved_vector)*norm(sample_vector))

    if(similarity >= threshold):
        return True
    else:
        return False


# vector [x1, x2, x3, x4, x5, x6, x7, x8], where:
# x1 - average key hold time [ms]
# x2 - standard deviation of key hold time [ms]
# x3 - average time between key presses [ms]
# x4 - standard deviation of time between key presses [ms]
# x5 - average time between key combinations [ms]
# x6 - standard deviation of time between key combinations [ms]
# x7 - average typing speed [keys/min]
# x8 - average number of errors [keys/min]


# example saved vector loaded from the database

x1 = 6.335486363636355
x2 = 759.6346187517274
x3 = 170.10119523809522
x4 = 136.27725309933592
x5 = 64.73562857142852
x6 = 32.771514631801445
x7 = 369.5279317065352
x8 = 0.0

saved_vector = [x1, x2, x3, x4, x5, x6, x7, x8]


# example sample vector collected during verification process

x1 = 10.617804545454543
x2 = 731.0779516777488
x3 = 163.4613952380952
x4 = 120.71333794840764
x5 = 70.82006250000003
x6 = 36.34854192398669
x7 = 384.538152054717
x8 = 0.0

sample_vector = [x1, x2, x3, x4, x5, x6, x7, x8]
    
    
# print result

print(verify(saved_vector, sample_vector, 0.9))