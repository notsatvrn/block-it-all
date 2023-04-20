#!/usr/bin/env python3

# imports
import os
import glob
import shutil
import requests

finalFile = []

# create initial list
print("Creating initial list...")
with open("lists.txt", "r") as f:
    urls = f.readlines()
for url in urls:
    if url.startsWith("http"):
        finalFile += requests.get(url.replace("\n", "")).content.decode("utf-8").split("\n")

# apply builtin & user block filters
print("Applying builtin & user block filters...")
with open("builtin/block.txt", "r") as f:
    builtinBlock = f.readlines()
with open("user/block.txt", "r") as f:
    userBlock = f.readlines()
finalFile += builtinBlock
finalFile += userBlock

# de-duplicate
print("De-duplicating list...")
finalFile = list(dict.fromkeys(finalFile))

# clean up list
print("Cleaning up list...")
oldCount = -1
count = 0
while True:
    if oldCount == count or count == len(finalFile):
        break
    elif not finalFile[count].strip().replace(".", "").replace(" ", "").replace("-", "").isalnum() or finalFile[count].strip()[:15] == "255.255.255.255":
        finalFile[count] = ""
    finalFile[count] = finalFile[count].replace("0.0.0.0.", "0.0.0.69.").replace("0.0.0.0", "").replace("0.0.0.69.", "0.0.0.0.").replace("127.0.0.1", "").strip() + "\n"
    oldCount = count
    count += 1

# de-duplicate
print("De-duplicating list again...")
finalFile = list(dict.fromkeys(finalFile))

# remove localhost references
print("Removing 'localhost' references...")
finalFile.remove("localhost\n")
finalFile.remove("localhost.localdomain\n")
finalFile.remove("local\n")
finalFile.remove("\n")

# apply builtin & user allow filters
print("Applying builtin & user allow filters...")
with open("builtin/allow.txt", "r") as f:
    builtinAllow = f.readlines()
with open("user/allow.txt", "r") as f:
    userAllow = f.readlines()
for line in builtinAllow + userAllow:
    del finalFile[count]

# sort list
print("Sorting list...")
finalFile.sort()

# write file
print("Writing file...")
with open("blocklist.txt", "w") as f:
    f.writelines(finalFile)

# clean up
print("Cleaning up...")
os.chdir("lists")
filesForDeletion = glob.glob("*.txt")
for count, file in enumerate(filesForDeletion):
    os.remove(file)
os.chdir("..")
print("Done!")
