# Getting started instructions for OSX
#
# 1. Install pdf2htmlEX (https://github.com/coolwanglu/pdf2htmlEX/wiki/Building)
# From terminal, run brew install pdf2htmlEX
#
# 2. Edit your PATH to include the directory where this was installed.
#
# On Mac OSX, this required the following commands in terminal (CMD+Spacebar, "terminal", enter):
# a) cd .
# b) nano .bash_profile
# c) Paste this: export PATH="/usr/local/Cellar/pdf2htmlex/0.14.6_10/bin:$PATH", CTRL+o, enter, CTRL+x
# d) To confirm it has worked, restart terminal (CMD+Q, relaunch), run: echo $PATH
#
# Reference:
# http://stackoverflow.com/questions/14256149/how-to-convert-pdf-to-html-using-pdf2htmlex-and-python
# https://coolestguidesontheplanet.com/add-shell-path-osx/
#
#
# BeautifulSoup PDF notes: http://mylifelogontheweb.blogspot.com/2009/05/scraping-pdfs-in-python.html

import subprocess
import fileinput
import os


def pdfToHTML(fileName):
    """
    Takes in fileName, converts it to HTML with pdf2htmlEX, and fixes a conversion
    error specific to the build sheets
    :param fileName: Name of file to be processed, WITHOUT extension
    :return:
    """
    pdfName = fileName+'.pdf'
    folder, tail = os.path.split(pdfName) # get folder where pdfs are stored
    pdfConvert(pdfName, folder) # convert all pdfs in folder to html
    htmlName = fileName+'.html'
    htmlFixer(htmlName) # make adjustments to html file to improve parsing


def pdfConvert(pdfName, directory):
    """
    Take an input pdf and convert it to HTML.
    :param pdfName:
    :return:
    """
    try:
        subprocess.call("pdf2htmlEX "+pdfName+' --dest-dir '+directory, shell=True)
    except:
        print('pdf2htmlEX did not work, is it installed and in your path?')
        raise
    createImported(pdfName)



def htmlFixer(htmlName):
    """
    pdf2htmlEX creates a few instances where empty spans are nested in divs
    to separate values in new columns, when the values should instead be in
    new divs. This searches for the close tag of the empty span [space]</span>
    and replaces it with tags to close the span and close the current and start a
    new div. This also creates a backup of the original file in the same directory.
    :param htmlName:
    :return:
    """
    fileToSearch = htmlName
    textToSearch = ' </span>'
    textToReplace = '</span></div><div>'

    try:
        with fileinput.FileInput(fileToSearch, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(textToSearch, textToReplace), end='')
    except:
        print('HTML editing error.')
        raise
    createImported(htmlName+'.bak')



def buildSheetImportIterator(rootDir, extension):
    """
    This function iterates through the subdirectories in rootDir,
    filters by files with a .pdf extension that aren't hidden,
    and builds a list of these files called filesImported.

    :param rootDir: Root directory
    :return: list of files
    """
    filesImported = []

    try:
        for dirs, subdirs, files in os.walk(rootDir):
            if not dirs.split("/")[-1] == 'imported':  # avoid directories called imported
                for file in files:
                    if not file[:1] == '.':  # avoid hidden files that start with a period
                        if file.split('.')[-1]==extension:
                            fullFile = (dirs + r'/' + file.split('.')[0])
                            filesImported.append(fullFile)
                    else:
                        pass
        if filesImported:
            #[print(i) for i in filesImported]
            return filesImported
        else:
            print('No files present to import')
            return False
    except:
        print('Directory parsing error.')
        raise


def createImported(fileName):
    """
    Take in fileName (includes directory and name), split into directory and file, create
    subdirectory under directory called "imported", and move file into that subdirectory
    :param fileName: Full file name, including directory (i.e. /Usr/Me/Desktop/file.xls
    :return: True if completed
    """
    directory, file = os.path.split(fileName)

    importedDir = directory + '/imported'
    os.makedirs(importedDir, exist_ok=True)
    finalFile = importedDir + '/' + file
    if os.rename(fileName, finalFile):
        return True
    else:
        return False









