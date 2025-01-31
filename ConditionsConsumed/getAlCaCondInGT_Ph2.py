############################################
# get AlCa conditions consumed in the CMSSW
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCalAliTrigger2022
############################################
import os
import re
import sys
import optparse

def checkTagInFile(tag, logFile):
    found = False
    checkTagLine =0
    foundTag = False
    foundPayload = False
    for i, line in enumerate(open(logFile)):
        #print i, line
        if tag.strip() in line.strip():
            foundTag = True
            checkTagLine = i
            continue
        if foundTag and "payloadIds" in line and (i == checkTagLine + 2):
            foundPayload = True
        if  foundTag and foundPayload and len(line.split(" ")) > 5 and (i == checkTagLine+3):
            found = True
    if(found):
        #return "Y"
        return "%GREEN% Yes %ENDCOLOR%"
    else:
        return ""

def escape_wikiwords(text):
    # Use a regular expression to find words starting with a capital letter
    return re.sub(r'\b([A-Z][a-zA-Z0-9]*)', r'!\1', text)

def getOneRow(tag, logFiles):
    escaped_tag = escape_wikiwords(tag.strip())
    rowName = "|" + escaped_tag
    for file_ in logFiles:
        checkTagInFile_ = checkTagInFile(tag, file_)
        rowName = rowName + " | " + checkTagInFile_
    return rowName + " | \n"

def printAllRow(tagFile, logFiles, outForTwiki, tableTitle):
    for file_ in logFiles:
        outfile = open(tagFile, "w")
        with open(file_) as f:
            lines = f.readlines()
            for l in lines:
                newl = l.split(': frontier:')[0]
                if re.search(r' / ', newl):
                    #print(newl)
                    outfile.write(newl+'\n')
    outfile.close()

    outForTwiki.write(tableTitle)
    for tag in open(tagFile):
        getOneRow_ = getOneRow(tag, logFiles)
        #print (getOneRow_)
        outForTwiki.write(getOneRow_)

def main():
    
    #Default input
    defaultData = False
    
    parser = optparse.OptionParser(usage = 'Usage: python3 getAlCaCondInGT.py [options] \n')

    parser.add_option('-d', '--data',
                      dest = 'isData',
                      default = defaultData,
                      help = 'enter True for data, False for MC. Default: False')

    (options, arguments) = parser.parse_args()

    #isData = False
    output_table = "MC" 
    tagFile = "allAlCaTags.txt"
    logFiles = []
    if(options.isData):
        logFiles.append("output_step1_L1.log")
        logFiles.append("output_step2_HLT.log")
        logFiles.append("output_step3_AOD.log")
        logFiles.append("output_step4_MINIAOD.log")
        logFiles.append("output_step5_NANOAOD.log")
    else:
        logFiles.append("output_step2_L1P2GTHLT.log")

    #output
    if(options.isData):
        output_table = "DATA"
        tableTitle = "|Tags|L1|HLT|AOD|MINIAOD|NANOAOD|\n"
    else:
        tableTitle = "|Tags|HLT|\n"

    outputForTwiki = open(f"outputForTwiki_{output_table}.txt", 'w')

    printAllRow(tagFile, logFiles, outputForTwiki, tableTitle)

if __name__ == '__main__':
    main()

