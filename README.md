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
- Refer to https://www.dashingd3js.com/d3js-scales
- Domain values (our real data values) --> convert to --> Range values (pixel values)
- 4 categories: continuous, ordinal (discrete), sequential (ex. range [0,1]), quantize (ex. each range for each bin color)
- Example 1: How to set domain and range and how to show them side by side
   <div id='div1'></div>  <!-- make a div out side script -->
   var data = d3.range(0, 11, 1); 
   var xScale = d3.scaleLinear() //here v4 but at v3: d3.scale.linear()
                  .domain([d3.min(data), d3.max(data)] // our real values
                  .range([0, 800]);  // pixel values (display values)
   d3.select('#div1').selectAll('div')
      .data(data)
      .enter()
      .append('div') 
      .text(function (d) {
          return d + "    " + xScale(d); // d is real data and xScale(d) is a range values
      });
- Example 2: Scale for color of "data" at column "region" of a json file.
   var regionColorScale = d3.scaleOrdinal()
                            .domain(d3.set(data.map(function(d) { return d.region; })))
                            .range(d3.schemeCategory20);
