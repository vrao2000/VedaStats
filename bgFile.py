import operator
import copy
import re
from fuzzywuzzy import fuzz
from threading import Thread


# function to check if there are fuzzy matches
def fuzzyCheck(word, hashTable):
    match = ""

    try:
        for key in hashTable:
            if word <> key  and len(key)>4 and len(word) > 4 and fuzz.partial_ratio(key,word) > 95: ## dont pick small words like cha, aa, tu
                if match == "":
                    match = key
                else:
                    match += ", " + key

        # hashTable[key][4] = match # for some reason not working !! cannot manipulate in function
    except TypeError:
        st  = "error"
        #print "Error: ", Exception, " key:", line


    # print "match=", match
    return match


###
def readShabdaKalpadruma():
    sbd_htable = {}
    exp1 = re.compile("^<HI>(.)*,")
    exp2 = re.compile("(\w)+,")
    file = open("./shabda_kalpadruma.txt", "r")

    for line in file:
        #
        # arr = line.split()
        try:
            m = exp1.search(line)
            if m:
                m2 = exp2.search(line)
                if m2:
                    temp = m2.group(0)
                    sbd_htable[temp[0:len(temp) - 1]] = "found"  ## remove the commma at the end
        except IndexError:
            errStr = "Error: ", Exception, " line:", line
    return sbd_htable
    # print "shabda kalpadruma entries", len(sbd_htable)


file = open("./GitashabdArtha.txt", "r")
htable = {}
htable_meaning = {}
obj = ["key", "meaning" , 1 , "", "pa" ] #word, meaning, count, chapter


#regular exp
exp = re.compile("^End of")

# using objects
chapter = "1"
for line in file:
    arr = line.split()

    try:
        meaning = ""
        endOfChapterMatch = exp.search(line)
        # # search() returns a Match object with information about what was matched

        if endOfChapterMatch: # new chapter found
            chapter = str( int(chapter) + 1)

        if (line.find("=")) > 1: # new token found
            position = line.find("=")
            meaning = line[(position + 1): len(line) - 1]  # right function

        if arr.count > 2:
             # fuzzyMatch = fuzzyCheck(arr[1], htable)
             # if  fuzzyMatch <> "":
             #    print arr[1], ", ", fuzzyMatch

             if arr[1] in htable:   #word already in hashtable
                 newObj = htable[arr[1]]
                 newObj[2] += 1
                 newObj[3] +=  ", " + chapter
                 #htable[arr[1]] = newObj
             else:
                 newObj = copy.deepcopy(obj)
                 newObj[0] = arr[1]
                 newObj[1] = meaning
                 newObj[2] = 1
                 newObj[3] = chapter
                 htable[arr[1]] = newObj
    except IndexError:
        errString = "err"
        # print "Error: ", Exception, " line:", line

# #
print "Gita htable size: ", len(htable)
# print "htable_meaning size: ", len(htable_meaning)
#
# for key in sorted_x:
#      print key
#
#
# keylist = htable_meaning.keys()
# keylist.sort()
# for key in keylist:
#     print "%s, %s" % (key, htable_meaning[key])
#

#call function
sbdTable = {} # readShabdaKalpadruma()

# print "shabda kalpadruma entries", len(sbd_htable)

# check if keys exists in sbd hashtable
keylist = htable.keys()
numberOfHits = 0

htable_threads = []
for key in keylist:
    #without threads
    htable[key][4] = fuzzyCheck(key, htable)

    # t1 = Thread(target=fuzzyCheck, args=(key, htable))
    # t1.start()
    # # t1.join()
    # htable_threads.append(t1)

    # if key in sbdTable: ## never do key in sbd_htable.keys()
    #     numberOfHits += 1


print "hits = ", numberOfHits

# for th in htable_threads:
#     # print "is alive:" , th.is_alive()
#     th.join()

#print the key and the content of hash
keylist = htable.keys()
keylist.sort()
for key in keylist:
    print "%s\t%s\t%s\t%s\t%s" % ( htable[key][0],htable[key][1], htable[key][2],htable[key][3],htable[key][4]  )




# for line in file:
#     arr = line.split()
#     for s in arr:
#         if s in htable:
#             htable[s] += 1
#         else:
#             htable[s] = 1



# for line in file:
#     arr = line.split()
#
#     try:
#         meaning = ""
#         if (line.find("=")) > 1:
#             position = line.find("=")
#             meaning = line[(position + 1): len(line) - 1]  # right function
#
#         if arr.count > 2:
#              htable_meaning[arr[1]] = meaning
#              if arr[1] in htable:
#                  htable[arr[1]] += 1
#              else:
#                  htable[arr[1]] = 1
#     except IndexError:
#         print "Error: ", Exception, " line:", line
#         #sorted_x = sorted(htable.items(), key=operator.itemgetter(1))
#         # print "htable size: ", len(htable)
#         # for key in sorted_x:
#         #     print key
#         # htable.clear()



# sorted_x = sorted(htable.items(), key=operator.itemgetter(1))
