# Build Sheet Decoder
Build sheet decoder for CCC vehicle build sheets in pdf format.

Utilizes pdf2htmlEX to convert .pdf to .html, then parses html using beautifulsoup. See BuildSheetDecoder.py.

**To-do:**
- [ ] Build additional error checking
- [ ] Use regex to verify divs based on contents in addition to class designations assigned by pdf2htmlEX
- [ ] Add output module to create .csv or add directly to database
- [ ] For standard equipment (final) section, determine if it's critical that same-section lines should be grouped together; if so, figure out how


![alt tag](https://cloud.githubusercontent.com/assets/23618756/22530352/215a44d4-e8a9-11e6-8e8a-dee3e55904d4.gif)
