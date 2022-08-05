import os
import shutil
import zipfile

batteryTestBdioFileRelPaths = [ 
  'packrat-lock/bdio/battery.bdio', 
  'composer-lock/bdio/battery.bdio', 
  'pip-cli/bdio/battery.bdio', 
  'npm-packagelock/bdio/battery.bdio', 
  'pipenv-cli-projectonly/bdio/battery.bdio', 
  'cocoapods-podlock/bdio/battery.bdio', 
  'pipenv-cli/bdio/battery.bdio', 
  'rubygems-versionless-lock/bdio/battery.bdio', 
  'cpanm-lock/bdio/battery.bdio', 
  'maven-cli/simple/bdio/battery.bdio', 
  'maven-cli/inconsistent-definitions/bdio/battery.bdio', 
  'pear-cli/bdio/battery.bdio', 
  'conan-cli/withrevisions/bdio/battery.bdio', 
  'conan-cli/pkgrevonly/bdio/battery.bdio', 
  'conan-cli/withuserchannel/bdio/battery.bdio', 
  'conan-cli/withprojectnameversion/bdio/battery.bdio', 
  'conan-cli/minimal/bdio/battery.bdio', 
  'sbt-dot/bdio/battery.bdio', 
  'yarn/yarn-workspaces-simple-allworkspaces/bdio/battery.bdio', 
  'yarn/yarn-workspaces-simple/bdio/battery.bdio', 
  'yarn/yarn-workspaces-berry/bdio/battery.bdio', 
  'yarn/yarn2-lock/bdio/battery.bdio', 
  'yarn/yarn2-workspace-hierarchy/bdio/battery.bdio', 
  'yarn/yarn2-hierarchical-monorepo/bdio/battery.bdio', 
  'yarn/yarn-lock/bdio/battery.bdio', 
  'yarn/yarn2-unnamed-workspaces/bdio/battery.bdio', 
  'yarn/yarn-workspaces-simple-selectwksp/bdio/battery.bdio', 
  'yarn/yarn2-workspace-hierarchy-exclude/bdio/battery.bdio', 
  'yarn/yarn-workspaces-excludedev/bdio/battery.bdio', 
  'yarn/yarn1-workspaces/bdio/battery.bdio', 
  'yarn/yarn1-workspaces-workspacedep/bdio/battery.bdio', 
  'conan-lock/shortform/bdio/battery.bdio', 
  'conan-lock/longform/bdio/battery.bdio', 
  'gradle-detect-on-detect/bdio/battery.bdio', 
  'rubygems-lock/bdio/battery.bdio', 
  'bazel/maven-jar/bdio/battery.bdio', 
  'bazel/haskell-cabal-library/bdio/battery.bdio', 
  'bazel/maven-install-complex/bdio/battery.bdio', 
  'bazel/haskell-cabal-library-all/bdio/battery.bdio', 
  'bazel/maven-install/bdio/battery.bdio', 
  'gradle-inspector/bdio/battery.bdio', 
  'sbt-dot-multipleprojectnode/bdio/battery.bdio', 
  'rubygems-circular-lock/bdio/battery.bdio', 
  'conda-list/bdio/battery.bdio', 
  'dep-lock/bdio/battery.bdio', 
  'bitbake/full/bdio/battery.bdio', 
  'bitbake/excldev/bdio/battery.bdio', 
  'go_vndr-lock/bdio/battery.bdio', 
  'sbt-resolutioncache/bdio/battery.bdio', 
  'go-mod/bdio/battery.bdio'
  ]

workingDirPath='/tmp/ppp'

for batteryTestBdioFileRelPath in batteryTestBdioFileRelPaths:
  try:
    shutil.rmtree(workingDirPath)
    print("Removed " + workingDirPath)
  except:
    print("Error removing " + workingDirPath + "; maybe it didn't exist")

  os.mkdir(workingDirPath)
  print("(Re)created " + workingDirPath)

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
