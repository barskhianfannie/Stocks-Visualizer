from itertools import groupby
import numpy as np

def numPlayers(k, scores=[]):

    scores = sorted(scores, reverse=True)
    ranked = [list(j) for i, j in groupby(scores)]
    totalranked = 0
    total = 0
    for i in range(0, k):
        if ranked[i][0] > 100 or ranked[i][0] < 0:
            continue
        else:
            total += len(ranked[i])
            if total >= k:
                
                return total
    
    return total
    


def hackerCards(collection, d):
    sortcollection = np.sort(collection)
    print(sortcollection)
    cards = []
    for i in range(1, d+1):
        if i not in sortcollection:
            cards.append(i)
        if sum(cards) == d:
            return cards
        elif sum(cards) > d:
            cards.remove(i)
            return cards

    return cards

if __name__ == "__main__":
    # print(numPlayers(3, [101,101,101,-1,0,25,25]))
    
    print(hackerCards([2,4,5], 7))
    