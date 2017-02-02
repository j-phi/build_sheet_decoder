# Build Sheet Decoder
Build sheet decoder for CCC vehicle build sheets in pdf format.

Utilizes pdf2htmlEX to convert .pdf to .html, then parses html using beautifulsoup. See BuildSheetDecoder.py.

**To-do:**
- [ ] Build additional error checking
- [ ] Use regex to verify divs based on contents in addition to class designations assigned by pdf2htmlEX
- [ ] Add output module to create .csv or add directly to database
- [X] Remove first and second column output of OEM data
- [ ] For standard equipment (final) section, determine if it's critical that same-section lines should be grouped together; if so, consider parsing css to build list of classes corresponding to the various background colors and use that to determine whether to append to the current list or start a new sublist.


![alt tag](https://cloud.githubusercontent.com/assets/23618756/22530352/215a44d4-e8a9-11e6-8e8a-dee3e55904d4.gif)
