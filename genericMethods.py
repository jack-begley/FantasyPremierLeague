import requests
import json
import math
from scipy.stats.stats import pearsonr 
from scipy.stats import linregress
import datetime
from tkinter import filedialog
from tkinter import Tk
import tkinter 
import csv 
import sys, traceback

# URL set up and league codes
from datetime import date
today = date.today()

#Setting up url construction
def mergeURL(sub):
    return 'https://fantasy.premierleague.com/api/' + sub

# Load the data from a URL into a list readable format - strings can be used to determine position in the list (E.g. url['key'] ) 
def generateJSONDumpsReadable(url):
        JSON = requests.get(url)
        Data = JSON.json()
        Dumps = json.dumps(Data)
        Readable = json.loads(Dumps)

        return Readable

# Generates a comma seperated list of the gameweek numbers (currently with 'gameweek' in position 0)
def generateCommaSeperatedGameweekNumberList():
    currentGameweek = math.floor((datetime.datetime.now() - datetime.datetime(2019, 8, 5)).days/7)
    gameweekList = list()
    gameweekList.append('gameweek')
    x = 1
    while x < currentGameweek:
        gameweekList.append(x)
        x = x + 1
    return gameweekList

# Try and parse text as an int. Returns integer or text
def parse(userInput):
    try:
       return int(userInput)
    except ValueError:
       return str(userInput)
                
# Try and parse and int. Results in boolean outputs
def isInt(userInput):
    try: 
        int(userInput)
        return True
    except ValueError:
        return False

# Replaces all the unicode characters in a tring with their unaccented equivalents
def unicodeReplace(string):
    cleanedString = string.replace("Á", "A").replace("á", "a").replace("À", "A").replace("à", "a").replace("Ȧ", "A").replace("ȧ", "a").replace("Â", "A").replace("â", "a").replace("Ä", "A").replace("ä", "a").replace("Ǎ", "A").replace("ǎ", "a").replace("Ă", "A").replace("ă", "a").replace("Ā", "A").replace("ā", "a").replace("Ã", "A").replace("ã", "a").replace("Å", "A").replace("å", "a").replace("Ą", "A").replace("ą", "a").replace("Ⱥ", "A").replace("Ǡ", "A").replace("ǡ", "a").replace("Ǻ", "A").replace("ǻ", "a").replace("Ǟ", "A").replace("ǟ", "a").replace("Ȁ", "A").replace("ȁ", "a").replace("Ȃ", "A").replace("ȃ", "a").replace("Æ", "AE").replace("æ", "ae").replace("Ǽ", "AE").replace("ǽ", "ae").replace("Ǣ", "AE").replace("ǣ", "ae").replace("Ḃ", "B").replace("ḃ", "b").replace("ƀ", "b").replace("Ƀ", "B").replace("Ɓ", "B").replace("Ƃ", "B").replace("ƃ", "b").replace("Ƅ", "b").replace("ƅ", "b").replace("Ć", "C").replace("ć", "c").replace("Ċ", "C").replace("ċ", "c").replace("Ĉ", "C").replace("ĉ", "c").replace("Č", "C").replace("č", "c").replace("Ç", "C").replace("ç", "c").replace("Ȼ", "C").replace("ȼ", "c").replace("Ƈ", "C").replace("ƈ", "c").replace("Ɔ", "C").replace("Ḋ", "D").replace("ḋ", "d").replace("Ď", "D").replace("ď", "d").replace("Đ", "D").replace("đ", "d").replace("Ƌ", "D").replace("ƌ", "d").replace("Ɗ", "D").replace("Ð", "D").replace("ð", "d").replace("ƍ", "d").replace("ȸ", "db").replace("Ǳ", "DZ").replace("ǲ", "Dz").replace("ǳ", "dz").replace("Ǆ", "DZ").replace("ǅ", "Dz").replace("ǆ", "dz").replace("Ɖ", "D").replace("ȡ", "d").replace("É", "E").replace("é", "e").replace("È", "E").replace("è", "e").replace("Ė", "E").replace("ė", "e").replace("Ê", "E").replace("ê", "e").replace("Ë", "E").replace("ë", "e").replace("Ě", "E").replace("ě", "e").replace("Ĕ", "E").replace("ĕ", "e").replace("Ē", "E").replace("ē", "e").replace("Ę", "E").replace("ę", "e").replace("Ȩ", "E").replace("ȩ", "e").replace("Ɇ", "E").replace("ɇ", "e").replace("Ȅ", "E").replace("ȅ", "e").replace("Ȇ", "E").replace("ȇ", "e").replace("Ǝ", "E").replace("ǝ", "e").replace("Ə", "e").replace("Ɛ", "e").replace("Ȝ", "e").replace("ȝ", "e").replace("Ḟ", "F").replace("ḟ", "f").replace("Ƒ", "F").replace("ƒ", "f").replace("Ǵ", "G").replace("ǵ", "g").replace("Ġ", "G").replace("ġ", "g").replace("Ĝ", "G").replace("ĝ", "g").replace("Ǧ", "G").replace("ǧ", "g").replace("Ğ", "G").replace("ğ", "g").replace("Ģ", "G").replace("ģ", "g").replace("Ǥ", "G").replace("ǥ", "g").replace("Ɠ", "G").replace("Ɣ", "g").replace("Ĥ", "H").replace("ĥ", "h").replace("Ȟ", "H").replace("ȟ", "h").replace("Ħ", "H").replace("ħ", "h").replace("ƕ", "h").replace("Ƕ", "H").replace("ı", "i").replace("Í", "I").replace("í", "i").replace("Ì", "I").replace("ì", "i").replace("İ", "I").replace("Î", "i").replace("î", "I").replace("Ï", "i").replace("ï", "I").replace("Ǐ", "i").replace("ǐ", "I").replace("Ĭ", "i").replace("ĭ", "I").replace("Ī", "i").replace("ī", "I").replace("Ĩ", "i").replace("ĩ", "I").replace("Į", "i").replace("į", "I").replace("Ɨ", "i").replace("Ȉ", "I").replace("ȉ", "i").replace("Ȋ", "I").replace("ȋ", "i").replace("Ɩ", "I").replace("Ĳ", "IJ").replace("ĳ", "ij").replace("ȷ", "j").replace("Ĵ", "J").replace("ĵ", "j").replace("ǰ", "j").replace("Ɉ", "j").replace("ɉ", "j").replace("ĸ", "k").replace("Ǩ", "K").replace("ǩ", "k").replace("Ķ", "K").replace("ķ", "k").replace("Ƙ", "K").replace("ƙ", "k").replace("Ĺ", "L").replace("ĺ", "l").replace("Ŀ", "L").replace("ŀ", "l").replace("Ľ", "L").replace("ľ", "l").replace("Ļ", "L").replace("ļ", "l").replace("ƚ", "l").replace("Ƚ", "L").replace("Ł", "L").replace("ł", "l").replace("ƛ", "L").replace("Ǉ", "LJ").replace("ǈ", "Lj").replace("ǉ", "lj").replace("ȴ", "l").replace("Ṁ", "M").replace("ṁ", "m").replace("Ɯ", "M").replace("Ń", "N").replace("ń", "n").replace("Ǹ", "N").replace("ǹ", "n").replace("Ň", "N").replace("ň", "n").replace("Ñ", "N").replace("ñ", "n").replace("Ņ", "N").replace("ņ", "n").replace("Ɲ", "N").replace("ŉ", "n").replace("ƞ", "n").replace("Ƞ", "N").replace("Ǌ", "NJ").replace("ǋ", "Nj").replace("ǌ", "nj").replace("ȵ", "n").replace("Ŋ", "N").replace("ŋ", "n").replace("Ó", "O").replace("ó", "o").replace("Ò", "O").replace("ò", "o").replace("Ȯ", "O").replace("ȯ", "o").replace("Ô", "O").replace("ô", "o").replace("Ö", "O").replace("ö", "o").replace("Ǒ", "O").replace("ǒ", "o").replace("Ŏ", "O").replace("ŏ", "o").replace("Ō", "O").replace("ō", "o").replace("Õ", "O").replace("õ", "o").replace("Ǫ", "O").replace("ǫ", "o").replace("Ő", "O").replace("ő", "o").replace("Ɵ", "O").replace("Ø", "O").replace("ø", "o").replace("Ȱ", "O").replace("ȱ", "o").replace("Ȫ", "O").replace("ȫ", "o").replace("Ǿ", "O").replace("ǿ", "o").replace("Ȭ", "O").replace("ȭ", "o").replace("Ǭ", "O").replace("ǭ", "o").replace("Ȍ", "O").replace("ȍ", "o").replace("Ȏ", "O").replace("ȏ", "o").replace("Ơ", "O").replace("ơ", "o").replace("Ƣ", "O").replace("ƣ", "o").replace("Œ", "OE").replace("œ", "oe").replace("Ȣ", "O").replace("ȣ", "o").replace("Ṗ", "P").replace("ṗ", "p").replace("Ƥ", "P").replace("ƥ", "p").replace("Ɋ", "P").replace("ɋ", "p").replace("ȹ", "qp").replace("Ʀ", "R").replace("Ŕ", "R").replace("ŕ", "r").replace("Ř", "R").replace("ř", "r").replace("Ŗ", "R").replace("ŗ", "r").replace("Ɍ", "R").replace("ɍ", "r").replace("Ȑ", "R").replace("ȑ", "r").replace("Ȓ", "R").replace("ȓ", "r").replace("Ś", "S").replace("ś", "s").replace("Ṡ", "S").replace("ṡ", "s").replace("Ŝ", "S").replace("ŝ", "s").replace("Š", "S").replace("š", "s").replace("Ş", "S").replace("ş", "s").replace("Ș", "S").replace("ș", "s").replace("ȿ", "s").replace("Ʃ", "S").replace("Ƨ", "S").replace("ƨ", "s").replace("ƪ", "S").replace("ß", "ss").replace("ſ", "t").replace("ẛ", "t").replace("Ṫ", "T").replace("ṫ", "t").replace("Ť", "T").replace("ť", "t").replace("Ţ", "T").replace("ţ", "t").replace("Ƭ", "T").replace("ƭ", "t").replace("ƫ", "t").replace("Ʈ", "T").replace("Ț", "T").replace("ț", "t").replace("Ⱦ", "T").replace("ȶ", "t").replace("Þ", "t").replace("þ", "t").replace("Ŧ", "T").replace("ŧ", "t").replace("Ú", "U").replace("ú", "u").replace("Ù", "U").replace("ù", "u").replace("Û", "U").replace("û", "u").replace("Ü", "U").replace("ü", "u").replace("Ǔ", "U").replace("ǔ", "u").replace("Ŭ", "U").replace("ŭ", "u").replace("Ū", "U").replace("ū", "u").replace("Ũ", "U").replace("ũ", "u").replace("Ů", "U").replace("ů", "u").replace("Ų", "U").replace("ų", "u").replace("Ű", "U").replace("ű", "u").replace("Ʉ", "U").replace("Ǘ", "U").replace("ǘ", "u").replace("Ǜ", "U").replace("ǜ", "u").replace("Ǚ", "U").replace("ǚ", "u").replace("Ǖ", "U").replace("ǖ", "u").replace("Ȕ", "U").replace("ȕ", "u").replace("Ȗ", "U").replace("ȗ", "u").replace("Ư", "U").replace("ư", "u").replace("Ʊ", "U").replace("Ʋ", "U").replace("Ʌ", "V").replace("Ẃ", "W").replace("ẃ", "w").replace("Ẁ", "W").replace("ẁ", "w").replace("Ŵ", "W").replace("ŵ", "w").replace("Ẅ", "W").replace("ẅ", "w").replace("ƿ", "x").replace("Ƿ", "X").replace("Ý", "Y").replace("ý", "y").replace("Ỳ", "Y").replace("ỳ", "y").replace("Ŷ", "Y").replace("ŷ", "y").replace("ÿ", "Y").replace("Ÿ", "y").replace("Ȳ", "Y").replace("ȳ", "y").replace("Ɏ", "Y").replace("ɏ", "y").replace("Ƴ", "Y").replace("ƴ", "y").replace("Ź", "Z").replace("ź", "z").replace("Ż", "Z").replace("ż", "z").replace("Ž", "Z").replace("ž", "z").replace("Ƶ", "Z").replace("ƶ", "z").replace("Ȥ", "Z").replace("ȥ", "z").replace("ɀ", "Z").replace("Ʒ", "z").replace("Ǯ", "Z").replace("ǯ", "z").replace("Ƹ", "Z").replace("ƹ", "z").replace("ƺ", "Z").replace("ƾ", "z").replace("Ɂ", "Z").replace("ɂ", "z")
    return cleanedString

# prints comma seperated lists to excel, where the keys are the headers: NOTE: Doesn't work for multi-layered lists
def printListToExcel(listNameToPrintToExcel,commaSeperatedHeadersList):
    # Open a window allowing the user to specify the file save path using a File Explorer
    root = tkinter.Tk()
    savePath =tkinter.filedialog.askdirectory()
    root.destroy()
    # Get the file path
    fileName = input("What do you want to call the file? > ")
    filePath = f"{savePath}/{today} - {fileName}.csv"
    # Create the dictionaries for the data that we are going to print into csv
    dataExportList = dict()
    headerList = list()
    printed = 0

    # Open the csv with our file name and path so we can write in the data
    with open(filePath, 'w', newline='', encoding='utf-8') as out:
        # Create the csv writers with the settings we want (e.g. the different delimiters)
        csv_out_tab_seperator = csv.writer(out, delimiter="\t")
        csv_out_comma_seperator = csv.writer(out, delimiter=",")

        commaSeperatedHeadersList = str(commaSeperatedHeadersList).replace("'","")
        cleanedHeaderList = commaSeperatedHeadersList.replace('[','').replace(']','').replace('"',"")
        csv_out_tab_seperator.writerow([f'{cleanedHeaderList}'])

        for dataPoint in listNameToPrintToExcel:
            currentList = list()
            currentAddition = str(listNameToPrintToExcel[dataPoint]).strip()
            currentList.append(currentAddition)
            listNameToPrintToExcel[dataPoint] = currentList
            listNameToPrintToExcelAsString = str(listNameToPrintToExcel[dataPoint]).replace("'","")
            exportableData = listNameToPrintToExcelAsString.replace('[','').replace(']','').replace('"',"")
            csv_out_tab_seperator.writerow([f'{dataPoint},{exportableData}'])

# Generate coefficients between an array of data and one key in that array
def correlcoeffGeneration(nameOfArrayToCorrelate, keyToCorrelateAgainstName):
    # Correlation time
    correlations = dict()
    currentX = dict()
    currentY = dict()
    currentCorrel = list()
    for element in nameOfArrayToCorrelate:
        length = len(nameOfArrayToCorrelate) - 1
        currentIndex = list(nameOfArrayToCorrelate).index(element)
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"Running regression: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"Regression complete: 100%")
            sys.stdout.flush()
            print("")
        if element != 'kickoff_time':
            currentX = nameOfArrayToCorrelate[element]
            currentY = nameOfArrayToCorrelate[keyToCorrelateAgainstName]
            currentCorrel = linregress(currentX,currentY)
            correlations[element] = currentCorrel
        else:
            None
    
    return correlations

# Generate coefficients between an array of data and one key in another array to test prediction of data
def correlcoeffGenerationForPrediction(nameOfArrayToCorrelate, dictOfDataWeAreLookingToPredictAgainst):
    # Correlation time
    correlations = dict()
    currentX = dict()
    currentY = dict()
    for values in dictOfDataWeAreLookingToPredictAgainst:
        currentY = dictOfDataWeAreLookingToPredictAgainst[values]
    lenY = len(currentY)
    currentCorrel = list()
    for element in nameOfArrayToCorrelate:
        length = len(nameOfArrayToCorrelate) - 1
        currentIndex = list(nameOfArrayToCorrelate).index(element)
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"Running regression: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"Regression complete: 100%")
            sys.stdout.flush()
            print("")
        if element != 'kickoff_time':
            currentX = nameOfArrayToCorrelate[element]
            lenX = len(currentX)
            if lenX > lenY:
                currentX = dict(currentX.items()[0:lenY])
                currentCorrel = linregress(currentX,currentY)   
            elif lenY > lenX:
                currentY = dict(currentY.items()[0:lenX])
                currentCorrel = linregress(currentX,currentY)
                for values in dictOfDataWeAreLookingToPredictAgainst:
                    currentY = dictOfDataWeAreLookingToPredictAgainst[values]
                lenY = len(currentY)
            else:
                currentCorrel = linregress(currentX,currentY)
            correlations[element] = currentCorrel
        else:
            None
    
    return correlations

# Index all data in a dictionary with 1 or 2 levels to 100 (where max is 100 and min is 0)
def indexDataInADictionary(listOfDataToIndex, listOfCorrespondingMaxValues, listOfCorrespondingMinValues):
    finalPlayerIndexedData = dict()
    for primaryKey in listOfDataToIndex:
        indexedValues = dict()
        try:
            for secondaryKey in listOfDataToIndex[primaryKey]:
                currentPlayerDataToIterate = listOfDataToIndex[primaryKey]
                if secondaryKey == 'kickoff_time':
                    None
                else:
                    indexedValue = (float(currentPlayerDataToIterate[secondaryKey])-listOfCorrespondingMinValues[secondaryKey])/(listOfCorrespondingMaxValues[secondaryKey]-listOfCorrespondingMinValues[secondaryKey])*100
                    indexedValues[secondaryKey] = indexedValue
        except:
                currentPlayerDataToIterate = listOfDataToIndex[primaryKey]
                indexedValue = (float(currentPlayerDataToIterate) - listOfCorrespondingMinValues)/(listOfCorrespondingMaxValues -listOfCorrespondingMinValues)*100
                indexedValues = indexedValue

        finalPlayerIndexedData[primaryKey] = indexedValues

    return finalPlayerIndexedData

# Takes a dictionary and outputs a single metric in 'string key: value' format
def generateSingleEntryDictFromDict(addDataForCurrentGameweek, fieldToGenerateDataFrom):
    outputDict = dict()
    outputDict[fieldToGenerateDataFrom] = addDataForCurrentGameweek[fieldToGenerateDataFrom]
    return outputDict