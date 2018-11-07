/* This file is to give some notes on D3.js so that it will reduce the time when developing a data visualization
dashboard using D3.js.
   For a full code of one particular example, please refer to https://bl.ocks.org/
*/

1. table.html
- Loading data: *.json, *.csv, *.tsv,... 
- Using map() function: map for every object {...} in json file
- Making simple html table
2. svg_elements (circle, rect, ect).html
- Making svg elements.
- Applying this simple element to make scatter plot, line plot and legend, ect.
3. Scaling
- Domain values (our real data values) --> convert to --> Range values (pixel values)
- 4 categories: continuous, ordinal (category), sequential (ex. range [0,1]), quantize (ex. each range for each bin color)
