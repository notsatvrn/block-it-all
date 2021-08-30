#!/usr/bin/env python3

# imports
import os
import glob
import shutil

# blocklists
# most of these lists are from firebog.net.
# please consider supporting the creators of these lists for their hard work.

os.chdir("lists")

# malware/suspicious lists

# wally3k's suspicious list:
# license: http://creativecommons.org/licenses/by-nc/4.0/
# creator: https://github.com/WaLLy3K
os.system("wget -O wally3k.txt https://v.firebog.net/hosts/static/w3kbl.txt")

# rooneymcnibnug's "snafu" suspicious list:
# license: http://www.wtfpl.net/about/
# creator: https://github.com/RooneyMcNibNug/pihole-stuff
# repo: https://github.com/RooneyMcNibNug/pihole-stuff
os.system("wget -O rooneymcnibnug-snafu.txt https://raw.githubusercontent.com/RooneyMcNibNug/pihole-stuff/master/SNAFU.txt")

# description: blocks phising domains.
# license: https://creativecommons.org/licenses/by-nc/4.0/
# creator: https://twitter.com/AndreaDraghetti
# website: https://phishing.army/
os.system("wget -O phishingarmy-blocklist-extended.txt https://phishing.army/download/phishing_army_blocklist_extended.txt")

# advertising lists

# description: blocks ads.
# license: https://github.com/anudeepND/blacklist/blob/master/LICENSE
# creator: https://github.com/anudeepND/
# repo: https://github.com/anudeepND/blacklist
os.system("wget -O anudeepnd-adservers.txt https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt")

# description: blocks pop-up ads.
# license: https://github.com/Yhonay/antipopads/blob/master/LICENSE
# creator: https://github.com/Yhonay
# repo: https://github.com/Yhonay/antipopads
os.system("wget -O yhonay-antipopads.txt https://raw.githubusercontent.com/Yhonay/antipopads/master/hosts")

# tracking/telemetry lists

# description: blocks windows trackers.
# license: https://github.com/crazy-max/WindowsSpyBlocker/blob/master/LICENSE
# creator: https://github.com/crazy-max
# repo: https://github.com/crazy-max/WindowsSpyBlocker
os.system("wget -O crazymax-windowsspyblocker-spy.txt https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt")

# description: blocks first-party trackers.
# license: https://git.frogeye.fr/geoffrey/eulaurarien/src/branch/master/LICENSE
# creator: https://geoffrey.frogeye.fr
# repo: https://git.frogeye.fr/geoffrey/eulaurarien
os.system("wget -O frogeye-firstpartytrackers.txt https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt")

# description: blocks android trackers.
# license: https://github.com/Perflyst/PiHoleBlocklist/blob/master/LICENSE
# creator: https://github.com/Perflyst
# repo: https://github.com/Perflyst/PiHoleBlocklist/
os.system("wget -O perflyst-androidtracking.txt https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/android-tracking.txt")

# description: blocks multi-party trackers.
# license: https://git.frogeye.fr/geoffrey/eulaurarien/src/branch/master/LICENSE
# creator: https://geoffrey.frogeye.fr
# repo: https://git.frogeye.fr/geoffrey/eulaurarien
os.system("wget -O frogeye-multipartytrackers.txt https://hostfiles.frogeye.fr/multiparty-trackers-hosts.txt")

# other lists

# description: blocks windows updatess.
# license: https://github.com/crazy-max/WindowsSpyBlocker/blob/master/LICENSE
# creator: https://github.com/crazy-max
# repo: https://github.com/crazy-max/WindowsSpyBlocker
os.system("wget -O crazymax-windowsspyblocker-updates.txt https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/updates.txt")

# description: blocks web browser based coin mining.
# license: https://github.com/hoshsadiq/adblock-nocoin-list/blob/master/LICENSE
# creator: https://github.com/hoshsadiq
# repo: https://github.com/hoshsadiq/adblock-nocoin-list/
os.system("wget -O hoshsadiq-nocoin.txt https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt")

# description: blocks porn.
# license: https://github.com/EnergizedProtection/block/blob/master/LICENSE
# creator: https://github.com/EnergizedProtection
# repo: https://github.com/EnergizedProtection/block
os.system("wget -O energized-porn.txt https://block.energized.pro/porn/formats/domains.txt")

# description: blocks trackers, ads, malware, etc.
# license: https://github.com/StevenBlack/hosts/blob/master/license.txt
# creator: https://github.com/StevenBlack
# repo: https://github.com/StevenBlack/hosts
os.system("wget -O stevenblack.txt https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-porn/hosts")

# description: blocks trackers and ads.
# license: none
# creator: https://github.com/sjhgvr
# website: https://oisd.nl
os.system("wget -O oisd.txt https://dbl.oisd.nl/basic/")

# create non cleaned-up list
print("creating non cleaned list...")
files = glob.glob("*.txt")
finalFile = []
for count, file in enumerate(files):
    with open(file, "r") as f:
        fileContent = f.readlines()
    finalFile += fileContent

# go back to main directory
os.chdir("..")

# de-duplicate
print("de-duplicating list...")
finalFile = list(dict.fromkeys(finalFile))

# clean up list
print("cleaning up list...")
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

# user whitelist/blocklist
os.chdir("changes")
print("adding/removing stuff based on files in the changes folder...")
with open("add.txt", "r") as f:
    addFileContent = f.readlines()
with open("remove.txt", "r") as f:
    removeFileContent = f.readlines()
finalFile += addFileContent
for count, line in enumerate(removeFileContent):
    del finalFile[count]
os.chdir("..")

# de-duplicate
print("de-duplicating list again...")
finalFile = list(dict.fromkeys(finalFile))

# remove localhost stuff
print("removing localhost stuff...")
finalFile.remove("localhost\n")
finalFile.remove("localhost.localdomain\n")
finalFile.remove("local\n")
finalFile.remove("\n")

# sort
print("sorting list...")
finalFile.sort()

# write file
print("writing file...")
with open("hosts.txt", "w") as f:
    f.writelines(finalFile)
