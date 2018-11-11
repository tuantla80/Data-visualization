/* This file is to give some notes on D3.js so that it will reduce the time when developing a data visualization
dashboard using D3.js.
   For a full code of one particular example, please refer to https://bl.ocks.org/
*/

/* 1. Loading data *.json, *.csv, *.tsv,... Using map() function  */
<script type="text/javascript">
    d3.csv("../../data/example.json",
        function (error, raw_data) {
            if (error) throw error;
            var data = raw_data.map(function (d) {
                return {
                    name: d.name, // name is a column name
                    age: +d.age
                };
                console.log(data);
            });
        });
</script>

/* 2. Refer to "table.html"
- Loading data: *.json, *.csv, *.tsv,... 
- Using map() function: map for every object {...} in json file
- Making simple html table
*/

/* 3 Refer to "svg_elements (circle, rect, ect).html"
- Making svg elements.
- Applying this simple element to make scatter plot, line plot and legend, ect.
*/

/* 4. Scaling
- Refer to https://www.dashingd3js.com/d3js-scales
- Domain values (our real data values) --> convert to --> Range values (pixel values)
- 4 categories: continuous, ordinal (discrete), sequential (ex. range [0,1]), quantize (ex. each range for each bin color)
*/
// Example 1: How to set domain and range and how to show them side by side
//   <div id='div1'></div>  <!-- make a div out side script -->
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

// Example 2: Scale for color of "data" at column "region" of a json file.
   var regionColorScale = d3.scaleOrdinal()
                            .domain(d3.set(data.map(function(d) { return d.region; })))
                            .range(d3.schemeCategory20);
/* 5. Drawing Axes */
// Example 1. x axis
 var xAxis = d3.axisBottom()   // "Bottom mean the tick is at the bottom of axis line. Can choose axisTop()
                .scale(xScale) // xScale is something like above
                .ticks(20);    // Can ignore .ticks(20) so that D3 will automatically choose the number of ticks
                               // NOTE: xAxis is just a function to generate svg for the axis. It still does NOT render the axis. 
 svg.append('g') // 'g': grouping svg elements
   .attr('transform', 'translate(0, ' + (height-30) + ')') // transate: x=0, y=(height-30) (in this case 30 is pixel) 
   .call(xAxis); // Render the axis

// Example 2. y axis
var yAxis = d3.axisLeft()
              .scale(yScale); // NOTE: (0,0) point is at the (top,left) so it will create a invert the axis.
                              // To make it as normal.  
                              //  var yScale = d3.scaleLinear()
                              //                 .domain([d3.max(some_thing), 0]) // NOTE from max to 0
                              //                 .range([number_1, number_2]);
svg.append('g')
   .attr('transform', 'translate(30,0)') // translate: x=30 (pixel) so that it will move to inside the canvas. y=0 (pixel)
   .call(yAxis);

/* 6. Positioning the axis */
var outerSize = {width: 800,  // 800 is 800 pixel
                 height: 600}; // they are svg width and height of the canvas
var outerAxisPadding=10, xAxisWidth=20, yAxisWidth=20;
var margin = {top: outerAxisPadding, 
              bottom: outerAxisPadding + xAxisWidth, 
              left: outerAxisPadding + yAxisWidth, 
              right: outerAxisPadding
             }; // In some ways, we may define margin (top, bottom, left, right) as a number 
            // (not throught the outerAxisPadding, xAxisWidth, and yAxisWidth)
var size = {width: outerSize.width - margin.left - margin.right,
            height: outerSize.height - margin.top - margin.bottom
           }; // size is inner size of the gragh (not including axes such as axis tick and axis label)

// Therefore, we can define "g" (grouping of svg elements in the inner size as below).
 g = svg.append('g') 
        .attr('transform', 'translate(margin.left, ' + margin.top + ')') // transate: x and y
        .attr('width', size.width)
        .attr('height', size.height)

/* 7. Styling Axese */
function stylingAxisElement(axisGroup){
   axisGroup.select('.domain') // meaning that searching for all svg elements in that group (yAxisGroup) 
                             // that has the "domain" css class assigned.
            .attr(stroke: 'red')
            .attr('stroke-width': 2);
   axisGroup.selectAll('.tick line')
            .atrr(stroke: 'green')
}

// The we can call function for xAxisGroup and yAxisGroup 
stylingAxisElement(xAxisGroup)
stylingAxisElement(yAxisGroup)

/* 8. Adding Tittle to Axese */

// x axis title
svg.append('text')
   .text('X title)
   .attr('transform',  // Need transform and translate (x and y) so that its position is on the good place.
         'translate(' + (margin.left + size.width/2) + ',' + (size.height - 15) + ')')
   .attr('text-anchor', 'middle'); // to make the text at the "middle"

// y axis title
svg.append('text')
   .text('Y title')
   .attr('transform', 
         'translate(20,' + (margin.top + size.height/2) + ') rotate(90)') // NOTE: rotate 90 degree fot Y title
   .attr('text-anchor', 'middle');
});







  





