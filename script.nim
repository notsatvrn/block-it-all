# imports
import httpclient, strutils, sequtils, algorithm

# procs
proc isStrAlphaNum(s: string): bool =
  for letter in items(s):
    if not isAlphaNumeric(letter): return false
  return true

# vars
var
  client = newHttpClient(maxRedirects = 0)
  count = 0
  lists = readFile("lists.txt").split("\n")
  finalList = readFile("builtinlists/block.txt").split("\n") & readFile("userlists/block.txt").split("\n")
  allowFileContent = readFile("builtinlists/allow.txt").split("\n") & readFile("userlists/allow.txt").split("\n")
  loc = 0

# create list
echo "creating list..."
for list in items(lists):
  try: finalList &= client.getContent(list).split("\n")
  except: continue

# clean list: phase 1
echo "cleaning list: phase 1..."
for line in items(finalList):
  if not isStrAlphaNum(finalList[count].replace(".").replace("-")):
    finalList[count] = line.replace("0.0.0.0 ").replace("127.0.0.1 ").strip
  count += 1

# apply allow lists
echo "applying built-in and user allowlists..."
for line in items(allowFileContent):
  loc = finalList.find(line.replace("\n").strip)
  if not line.strip.startsWith("#") and loc != -1: finalList.del(loc)

# clean list: phase 2
echo "cleaning list: phase 2..."
count = 0
while count < len(finalList):
  if not isStrAlphaNum(finalList[count].replace(".").replace("-")) or not finalList[count].contains(".") or finalList[count].endsWith("."): finalList.del(count)
  else: count += 1
finalList = deduplicate(sorted(finalList), isSorted = true)

# write file
echo "writing file..."
let f = open("blocklist.txt", fmWrite)
for line in finalList: f.writeLine(line)
echo "done!"