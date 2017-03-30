"""
Strings Sort

sort_strings function will return sorted version of input which is list of strings

To implement this function first we augment data and map them to the data types.
For example, if we have string as "Andoird2.2" augmented version of this would be ["Android2.2", "android", 2.2] where we will map this to strnum datatype since first we will sort as per string and then as per number. With this logic we can have alternate versions of str and num such as numstrnumstrnum and we will assume each version as different class in which we will sort same class items. Once we sort same class items we will combine them to a one list using only their label data which is their initial value as string before being augmented.

This method will indeed work with dates as well such that dates represented as "2016-10-11" which will be augmented to ["2016-10-11", 2016, 10, 11] as numnumnum datatype where it will be sorted initially per year then per month and then per day. In fact, we can extend this to any kind of numbers seperated with dash such as "11111-2222-3333-4444-...." and it will sort it as per its mapped data class.

When user inputs some unpredicted value such as 1..598 we will assume it as string since we will not be able to know whether input represents number or string or combination of boths.
"""


from operator import itemgetter
from itertools import groupby

def sortBuckets(buckets):
    """
    Sort values of the augmented data types as per their class

    :type buckets: Dict
    :param buckets: Classes of augmented data types where key represents class

    return -> List[String]
    """
    augmentedSorted = []
    for values in buckets.values():
        augmentedSorted.extend(sorted(values, key = itemgetter(slice(1, None))))

    return [data[0] for data in augmentedSorted]


def parseString(item, buckets):
    """
    Augment string data and get define its data class. Then, insert augmented data to dictionary where data class is key.

    :type item: String
    :param item: Each input in the list

    :type buckets: Dict
    :param buckets: Classes of augmented data types where key represents class

    return -> None
    """
    augmented = [item]
    parsed = ["".join(g) for k, g in groupby(item, str.isalpha)]
    key = ""
    for substring in parsed:
        try:
            num = float(substring)
            augmented.append(num)
            key += "num"
        except:
            splittedSubstring = substring.split("-")
            for s in splittedSubstring:
                try:
                    num = float(s)
                    augmented.append(num)
                    key += "num"
                except:
                    augmented.append(s.lower())
                    key += "str"

    if key not in buckets:
        buckets[key] = []
    buckets[key].append(augmented)

def sort_strings(l):
    """
    Group same types of strings together, sort them seperately and then return results combined
    
    :type l: List[String]
    :param l: Input which containes either numbers, dates, words or combinations of these

    return -> List[String]
    """
    buckets = dict()
    for item in l:
        parseString(item, buckets)
    
    res = sortBuckets(buckets)
    return res

print(sort_strings(["10160-10-12", "2016-10-10", "2017-01-01","2016-12"]))
print(sort_strings(["Apple", "Watermellon", "bacon", "sacon"]))
print(sort_strings(["-1", "2", "1..2", "10", "-2.4"]))
print(sort_strings(["Z", "3", "Y", "1", "X", "2.5", "False"]))
print(sort_strings(["android2.2-5","ios2.9", "ANDROID2.2-2","1345asa", "android13.0-1", "8bsa", "iOS1.3"]))
