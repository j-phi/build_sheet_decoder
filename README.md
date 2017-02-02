# Build Sheet Decoder
Build sheet scraper for CCC vehicle build sheets in pdf format.

Utilizes pdf2htmlEX to convert .pdf to .html, then parses html using beautifulsoup. See BuildSheetDecoder.py.

**To-do:**
- [ ] Build additional error checking
- [ ] Use regex to verify divs based on contents in addition to class designations assigned by pdf2htmlEX
- [ ] Add output module to create .csv or add directly to database
- [X] Remove first and second column output of OEM data
- [ ] For standard equipment (final) section, determine if it's critical that same-section lines should be grouped together. If so, consider rule to group with previous line if previous line div width >480px & current line begins with lowercase or a parenthesis was opened previously and not yet closed. This will likely not be perfect, but would work for our two sample documents. Unfortunately, there is no css style that dictates the color of the row background; it's a full-page image file.


![alt tag](https://cloud.githubusercontent.com/assets/23618756/22530352/215a44d4-e8a9-11e6-8e8a-dee3e55904d4.gif)
