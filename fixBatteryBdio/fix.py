import os
import shutil
import zipfile

batteryTestBdioFileRelPath='bazel/haskell-cabal-library/bdio/battery.bdio'

workingDirPath='/tmp/ppp'
try:
  shutil.rmtree(workingDirPath)
  print("Removed " + workingDirPath)
except:
  print("Error removing " + workingDirPath + "; maybe it didn't exist")

os.mkdir(workingDirPath)
print("Created " + workingDirPath)
originalBdioFilePath='/Users/billings/src/synopsys-detect/src/test/resources/battery/' + batteryTestBdioFileRelPath
workingBdioFilePath=workingDirPath + "/battery.bdio"
print("Processing " + originalBdioFilePath)
print("Copying  " + originalBdioFilePath + " to " + workingBdioFilePath)
shutil.copyfile(originalBdioFilePath, workingBdioFilePath)

with zipfile.ZipFile(workingBdioFilePath, 'r') as archive:
  archive.extractall(workingDirPath)

headerFilename = 'bdio-header.jsonld'
entryFilename = 'bdio-entry-00.jsonld'

workingHeaderFilePath = workingDirPath + '/' + headerFilename
workingEntryFilePath = workingDirPath + '/' + entryFilename
print("")
print(workingHeaderFilePath + ":")
workingHeaderFile = open(workingHeaderFilePath, "r")
workingHeaderReplacementFilePath = workingHeaderFilePath + "_NEW"
workingHeaderReplacementFile = open(workingHeaderReplacementFilePath, "w")
for line in workingHeaderFile:
  hasNamePos = line.find('#hasName')
  if hasNamePos >= 0:
    #print(line.rstrip() + ' <== FOUND IT!')
    fixedLine = line.replace("Black Duck I/O Export", "bdio")
    print(fixedLine.rstrip())
    workingHeaderReplacementFile.write(fixedLine)
  else:
    print(line.rstrip())
    workingHeaderReplacementFile.write(line)


workingHeaderFile.close()
workingHeaderReplacementFile.close()

os.remove(workingBdioFilePath)
os.remove(workingHeaderFilePath)
os.rename(workingHeaderReplacementFilePath, workingHeaderFilePath)

os.chdir(workingDirPath)
with zipfile.ZipFile(workingBdioFilePath, 'w') as archive:
  archive.write(headerFilename)
  archive.write(entryFilename)

os.remove(originalBdioFilePath)
shutil.copyfile(workingBdioFilePath, originalBdioFilePath)
