import csv
import json

quaidlist = [97172418258280448, 101462910349381632, 97171583524691968, 97171421553233920, 98542595751288832, 100412818922168320, 97171512729014272]

quaidlinglist = [280833155148021773, 104333643404546048]

def readcsvtodict(filename):
    filepath = f"/pythbot/Buttery_Biscuit_Bot/{filename}.csv"
    with open(f'{filepath}', mode='r') as infile:
        dictionary = dict(csv.reader(infile))
    return dictionary
    
def writedictcsv(dictionary, filename):
    filepath = f"/pythbot/Buttery_Biscuit_Bot/{filename}.csv"
    w = csv.writer(open(filepath, "w"))
    for key, val in dictionary.items():
        w.writerow([key, val])


def authname(context):
    if context.author.nick != None:
        return context.author.nick
    else:
        return str(context.author)[0:-5]


def writedictjson(dictionary, filename):
    filepath = f"/pythbot/Buttery_Biscuit_Bot/{filename}.csv"
    with open(filepath, 'w') as fp:
        json.dump(dictionary, fp)
        

def readdictjson(filename):
    filepath = f"/pythbot/Buttery_Biscuit_Bot/{filename}.csv"
    with open(filepath) as json_file:
        load = json.load(json_file)
    return dict(load)
    
def hasquaid(context):
    return context.author.id in quaidlist
    
def hasquaidling(context):
    return context.author.id in quaidlinglist
    
def getprivs(context):
    if context.author.id == 97172418258280448:
        return 'tesseract'
    elif context.author.id in quaidlist:
        return 'quaid'
    elif context.author.id in quaidlinglist:
        return 'quaidling'
    else:
        return None

async def is_tesseract(context):
    return context.author.id == 97172418258280448
    
async def makekwargs(arglist):
    kwargs = {}
    for x in arglist:
        temp = x.split(sep="=")
        if len(temp) == 1:
            return None
        kwargs[temp[0]] = temp[1]
    return kwargs