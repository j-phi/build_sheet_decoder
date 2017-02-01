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
# Beautifulsoup PDF notes: http://mylifelogontheweb.blogspot.com/2009/05/scraping-pdfs-in-python.html

import subprocess
import fileinput

def fileProcess(fileName):
    """
    Takes in fileName, converts it to HTML with pdf2htmlEX, and fixes a conversion
    error specific to the build sheets
    :param fileName: Name of file to be processed, WITHOUT extension
    :return:
    """
    pdfName = fileName+'.pdf'
    htmlName = fileName+'.html'
    pdfConvert(pdfName)
    htmlFixer(htmlName)

################################

def pdfConvert(pdfName):
    """
    Take an input pdf and convert it to HTML.
    :param pdfName:
    :return:
    """
    subprocess.call("pdf2htmlEX "+pdfName, shell=True)



#################################

def htmlFixer(htmlName):
    """
    pdf2htmlEX creates a few situations where empty spans are nested in divs
    to separate values, when the values should really be in new divs. This
    searches for the close tag of the empty span [space]</span> and replaces
    it with tags to close the span and close the current and start a new
    div. This also creates a backup of the original file in the same directory.
    :param htmlName:
    :return:
    """
    fileToSearch = htmlName
    textToSearch = ' </span>'
    textToReplace = '</span></div><div>'

    with fileinput.FileInput(fileToSearch, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(textToSearch, textToReplace), end='')

#################################

fileProcess('bs2')






