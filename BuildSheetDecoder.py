from bs4 import BeautifulSoup
from pdf2htmlEX import buildSheetImportIterator, pdfToHTML
'''
Prior to use, ensure that you have used pdf2htmlEX.py to convert pdf files
to parse-able html files.
'''
pdfDirectory = '/Users/jayphinizy/Desktop/TestProcessor'
processFiles = buildSheetImportIterator(pdfDirectory, 'pdf') # Add pdfs from root dir to list
divList = []
[pdfToHTML(i) for i in processFiles] # Converts pdfs to html, cleans it, moves everything but htmls to imported folder
processFiles = [] # Clear processFiles
processFiles = buildSheetImportIterator(pdfDirectory, 'html') # Gets new list of html files from list


def initialClean(soup):

    # Remove extraneous img, style, and script tags and their contents
    #
    # http://stackoverflow.com/questions/5598524/can-i-remove-script-tags-with-beautifulsoup
    #
    # Unsure if this could be replaced by a soupstrainer to just allow and parse divs?

    [s.decompose() for s in soup('img')]
    [s.decompose() for s in soup('style')]
    [s.decompose() for s in soup('script')]
    [s.decompose() for s in soup(class_= '_ _6')] # Remove hidden spans in vehicle info
    [s.decompose() for s in soup(class_= '_ _7')] # Remove hidden spans in vehicle info
    divList = []
    divList = [s.text for s in soup.find_all('div')]


def find(lst, searchTerm, offset):
    """
    Iterates through list (lst) and returns a list of indexes of items matching searchTerm, offset by offset.
    If if the list item at index 3 matches searchTerm and offset = 2, then it will return 5.
    This can be used to return the next (offset=1) or previous (offset=-1) value in a list
    http://stackoverflow.com/questions/16685384/finding-the-indices-of-matching-elements-in-list-in-python
    """
    return [i+offset for i, x in enumerate(lst) if x==searchTerm]

def findUpper(lst, offset):
    """
    Iterates through list (lst) and returns a list of indexes of items matching searchTerm, offset by offset.
    If if the list item at index 3 matches searchTerm and offset = 2, then it will return 5.
    This can be used to return the next (offset=1) or previous (offset=-1) value in a list
    http://stackoverflow.com/questions/16685384/finding-the-indices-of-matching-elements-in-list-in-python
    """
    return [i + offset for i, x in enumerate(lst) if x.isupper()]

def buildStatDict():
    """
    Gathers vehicle data from the first page using class-based searches.
    TODO: Build error-checking for fields, consider regex approach to account for class
    assignment anomolies
    :return: Dictionary of vehicle stats, including vehicle, vin, full_auto, msrp, and invoice.
    """
    # Begin collecting general vehicle information from the first page
    vehicle = soup.find_all(class_='ff3 fc0')[0].string.strip() # Year/Make/Model (2015 Chevrolet Impala)
    vin = soup.find_all(class_='ff3 fc0')[1].string.strip() # VIN (2G1165S38F9293614)
    auto_data = [s.string for s in soup.find_all(class_='y1e')][0] # Vehicle 1: 2015 Chevrolet Impala 4dr
    full_auto = auto_data[0][11:] #2015 Chevrolet Impala 4dr
    msrp = soup.find(class_='y1e').next_sibling.string #$35,440.00
    invoice = soup.find(class_='y1e').next_sibling.next_sibling.string #$33,490.80

    vehicleStats = {}
    vehicleStatKeys = ['vehicle','vin','full_auto','msrp','invoice']
    vehicleStatValues = []
    vehicleStatValues.extend([vehicle,vin,auto_data,msrp,invoice])
    vehicleStats = dict(zip(vehicleStatKeys,vehicleStatValues))
    return(vehicleStats)


def submissionChecklist():
    """
    This searches for checkmarks inside divs and returns the text in the
    next div, which contains the checked feature
    The html looks like this: <div>✓</div><div>FeatureName</div>
    TODO: fix double-escaped quotations (if needed)
    :return: List of items where equipment is currently selected in the valuation request
    """
    divList = [s.text for s in soup.find_all('div')]
    chkList = find(divList, '✓',1)
    fnlChkLst = []
    print('\nChecked Items:')
    for i in chkList[1:]: #([1:] because first check is in Legend)
        fnlChkLst.append(divList[i].split(' -')[0])

    return(fnlChkLst)

def mfgInstalledList():
    """
    This searches for spans containing -inst (installed), and returns
    the text of the parent div, which contains the installed feature.
    The html looks like this: <div>FeatureName<span>-inst</span></div>
    :return: list of items with '-inst' designation, meaning the manufacturer indicates the equipment is installed.
    """
    spanList = [s.text for s in soup.find_all('span')]
    spanParents = [s.parent.text for s in soup.find_all('span')]
    instList = find(spanList, '- inst', -1) # Start with span before '-inst'
    fnlInstLst = []
    print('\nInstalled Items (MFG):')
    for l in instList[1:]: #([1:] because first inst is in Legend)
        fnlInstLst.append(spanParents[l].split(' -')[0])
    return(fnlInstLst)

def OEMInstalledList():
    """
    This searches for 'Installed' inside divs and returns the text
    in the next divs
    The html looks like this: <div>Installed</div><div>$</div><div>1050</div><div>C3U</div><div>[Description]</DIV>
    TO-DO:  If non-installed items desired, consider adding.
            Remove first and second item from every list ('Installed', '$')
    :return: list of items from OEM list, including MSRP, OEM CODE, and DESCRIPTION
    """
    divList = [s.text for s in soup.find_all('div')]
    msrpList = find(divList, 'Installed',0)
    availEquip = []

    print('\nInstalled Items (OEM):')
    for ind,item in enumerate(msrpList[0:]):
        next = ind + 1
        if next < len(msrpList):
            start = item
            end = msrpList[next]
            curEquip = []
            # Return everything between the current 'Installed' position (start) and the next 'Installed' position (end)
            for x in range(start, end):
                if(divList[x]):
                    # Skip if first word is 'Copyright', 'Page', 'Installed', or '$'
                    if(divList[x].split(' ')[0] not in ['Copyright', 'Page', 'Installed', '$']):
                        curEquip.append(divList[x])
            availEquip.append(curEquip)
    return availEquip

def stdEquip():
    """
    This locates the position of the div with the contents 'Standard Equipment' and then saves the numeric index
    position of the ALL-CAPS divs after that (section headers). It then creates a list for each of those sections,
    starting with the all-caps section header and then listing every row of data afterwards.
    TO-DO: Determine if it's critical that same-section lines should be grouped together. As the document stands now,
    I can find no way to tell whether a given line is the start of a new entry or continuation of the previous entry.
    :return: List of standard equipment
    """
    divList = [s.text for s in soup.find_all('div')]
    #stdEquip locates the start of the Standard Equipment Section
    stdEquip = find(divList, 'Standard Equipment',0)
    #upperList finds divs whose contents are all uppercase and then filters that list to only items after stdEquip
    upperList = findUpper(divList, 0)[2:]
    upperList = [item for item in upperList if item > stdEquip[0]]
    standardEquipment = []
    print('\nStandard Equipment:')
    for ind,item in enumerate(upperList[0:]):
        next = ind + 1
        if next < len(upperList):
            start = item
            end = upperList[next]
            curEquip = []
            # Return everything inbetween the current subsection (start) and the next subsection(end)
            for x in range(start, end):
                if(divList[x]):
                    # Skip if first word is 'Copyright', 'Page', or empty ('.').
                    if(divList[x].split(' ')[0] not in ['Copyright', 'Page', '.']):
                        curEquip.append(divList[x])
            standardEquipment.append(curEquip)
    return standardEquipment

for p in processFiles:
    print('\n')
    html_doc = p+'.html'
    html = open(html_doc,'r').read()
    soup = BeautifulSoup(html, 'html.parser')
    initialClean(soup)

    autoStats = buildStatDict()
    for k, v in autoStats.items():
        print(k + ': ' + v)

    checkedSelected = submissionChecklist()
    print(checkedSelected)

    mfgInstalled = mfgInstalledList()
    print(mfgInstalled)

    oemInstalled = OEMInstalledList()
    print(oemInstalled)

    stdEquipment = stdEquip()
    print(stdEquipment)

#print(soup.prettify())
