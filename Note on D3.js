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

/* 8. Adding Tittle to Axes */
// x axis title
svg.append('text')
   .text('X title')
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

/* 9. Custom Tick Labels */
// For x axis (ver similar to y axis
 var xAxis = d3.axisBottom().scale(xScale)
               .ticks(30)
               .tickFormat(function (d){ // NOTE. Add a function to tickFormat so that we can customize ticks
                   return d + " Years"; // every tick will plus with " Years"
               });
var xAxisNodes = svg.append('g')
                    .attr('transform', 'translate(' + margin.left + ',' + (size.height - margin.bottom) + ')')
                    .call(xAxis);
xAxisNodes.selectAll('text')
           .attr('transform', 'rotate(120)') // NOTE: rotate ticks in 120 degree
           .attr('text-anchor', 'start') 
           .attr('dy', '-1.5em') // "dy" attribute is for the size of the text. (co-ordinate is still (0,0) is (top, left)
                                 // 1em is the number of pixels of a font size. 
                                 // Ex. for a base font size of 12px , a value of 1em is translated into 12px 
           .attr('dx', '0.5em');


/* 10. Legends */
var legendGroup = svg.append('g')
                     .attr('transform', 'translate(' + size.width + ',' + mangin.top + ')');

var legendBox = legendGroup  // a rectangle
   .append('rect')
   .attrs({
       fill: 'white',
       stroke: 'black',
       width: 300,
       height: regionColorMap.domain().length * 25 + 10, // number of unique items is regionColorMap.domain().length
       'fill-opacity': 0.5
   });
var subLegendGroup = legendGroup.append('g');
var legendSubGroups = subLegendGroup.selectAll('rect')
   .data(regionColorMap.domain())
   .enter()
   .append('g')
   .attr('transform', function (d,i){
       return 'translate(10,' + ((i*25)+5) + ')';
   });
legendSubGroups
   .append('rect')
   .attrs({
       x:0, y:0, 
       width: 20, height: 20,
       fill: function (d,i){
           return regionColorMap(d);
       }
   });
var legendTexts = legendSubGroups
   .append('text')
   .text(function (d) { return d; })
   .attrs({
       x: 25,
       y: 15
   });

var max = d3.max(legendTexts.nodes(), // get a longest text
   n=> n.getComputedTextLength());

legendBox.attr('width', max+25+20);
      
/* 11. Grid lines 
NOTE: at d3.js, grid lines are actually an axis with the ticks at the opposition direction of normal ticks
and furthermore its ticks accross the entire visualization.
In this example the css grid as below:
        .grid line {
            stroke: lightgrey;
            stroke-opacity: 0.75;
            shape-rendering: crispEdges;
        }
        .grid path {
            stroke-width: 0;
        }
*/
svg.append('g')
   .call(xAxis.tickFormat("") // set to empty string because we don't need any lables on ticks.
               .tickSize(-size.height)) // tickSize is over all the graph
   .attr('transform', 'translate(' + margin.left + ',' + margin.bottom +')')
   .attr('class', 'grid');

svg.append('g')
   .call(yAxis.tickFormat("").tickSize(-size.width))
   .attr('transform', 'translate(' + margins.left + ',' + margin.top +')')
   .attr('class', 'grid');

/* 12. nest(), key(), map() and, get() vs filter() 
   Supposing we want to filter data at year=2000 of test.json file
*/
d3.json("../../data/test.json",
    function (error, rawData) {
        var allData = rawData.map(function (d) {
            return {
                CountryName: d.CountryName,
                LifeExp: +d.LifeExp,
                Year: +d.Year
            }});
   
      // Method 1: Filtering data of year=2000. 
      // It works but less efficient since it has to scan all objects (rows) every time we want to check Year=2000 or 2001, ...
      dataAtyear2000 = allData.filter(function(d){ // run for every objects at data
                                                return d.Year===2000  // get object at which Year=2000
                                               });

     // Method 2: Filtering data of year=2000. 
     // It works in a more efficient way.
     var nested = d3.nest()
                    .key(function (d) { return d.Year; }) // will use the "Year" as a key
                    .map(allData); // Making nested as for every year. (key is a year)
     dataAtyear2000 = nested.get(2000);

/* 13. Making a reusable D3.js code
- Method 1. Build as an object.
- Method 2: Make a some (big) functions
- NOTE: using "var x=svg.append('g')....."  may make it not visible to other functions. So sometimes just remove "var".
 */

/* 14. Animation with timers  */
 maxYear = 2018, minYear=1950, currentYear=minYear;
 var timer = d3.interval(function(elapsed){
                    console.log(elapsed); // will run every 500ms (see below)
                    currentYear++;
                    if (currentYear <= maxYear){
                       render_a_plot(nested.get(currentYear)); // Run a render_a_plot() function of data at which Year=currentYear
                    } else {
                       console.log("stop");
                       timer.stop();
                    }
                }, 500);
            });
// NOTE: Sometimes we can remove plot. Ex. bubblesGroup.selectAll("*").remove(); 

/* 15. General Update Pattern */

/* 16. Navigation using Buttons 
Inside body make:
   <div>
        <button id="decrement">-</button>  <!-- make decrement button with symbol -  -->
        <label style="text-align: center;" id="currentYearLabel"></label>  <!-- id is currentYearLabel -->
        <button id="increment">+</button>
   </div>
*/
d3.select("button#increment").on("click", 
    function handleClick(){
        if (currentYear++ >= maxYear) currentYear = maxYear
        update(currentYear, nested.get(currentYear)); // call update() function
    });
d3.select("button#decrement").on("click", 
    function handleClick(){
        if (--currentYear < minYear) currentYear = minYear
        update(currentYear, nested.get(currentYear));
    });

 function update(year, data){
    console.log("rendering: " + year);
    d3.select("label#currentYearLabel").html(year); // NOTE: using html() function
    //... some code below...
    
/* 17. Navigation using Slider 
Inside body make:
   <div>
        <button id="decrement">-</button>  <!-- make decrement button with symbol -  -->
        <label style="text-align: center;" id="currentYearLabel"></label>  <!-- id is currentYearLabel -->
        <button id="increment">+</button>
   </div>
   
   <div>
         <input type="range" id="slider"></input>  <!-- id is slider -->
   </div>
*/
 slider = d3.select("input#slider");
 slider.attrs({
     "min": minYear,
     "max": maxYear,
     "value": currentYear
 });
 console.log(slider);

 update(currentYear, nested.get(currentYear));
//...Some code here...
    
d3.select("input#slider").on("input",  // "input" control is "slider"
       function handleClick(){
           currentYear = this.value;
           update(currentYear, nested.get(this.value));
       });    
    
    
/* 18. Animation using Transition 
In the body make:
  <div style="position: relative; left:100px; top:10px;">
       <button onclick="transitionPosition()">Position</button> <!-- will call transitionPosition() when click on Position -->
       <button onclick="transitionSize()">Size</button>
       <button onclick="transitionColor()">Color</button>
       <button onclick="transitionOpacity()">Opacity</button>
       <button onclick="interrupt()">Interrupt</button>
       <button onclick="chainedTransition()">Chained</button>
    </div>
 Refer to: Transition Easing Comparision https://bl.ocks.org/d3noob/1ea51d03775b9650e8dfd03474e202fe
           https://github.com/d3/d3-transition  
*/
function transitionPosition(){
   console.log("starting position transition")
   var transitionDuration = 1000;
   var select = svg.select("circle");
   select.transition()
         .duration(transitionDuration)
         .attrs({ "cx": 300 });
}
    
function transitionSize(){
   console.log("starting size transition")
   var transitionDuration = 5000;
   var select = svg.select("circle");
   select
       .transition()
       .duration(transitionDuration)
       .attrs({ "r": 50 });
   console.log("exiting size transition");
}

function transitionOpacity(){
   console.log("starting transition")
   var transitionDuration = 5000;
   var select = svg.select("circle");
   select
       .transition()
       .duration(transitionDuration)
       .attr("opacity", 0.0)
       .on("interrupt", function(d) { console.log("interrupted"); });
   console.log("exiting transition");
}

function interruptedTransition(){
   console.log("starting transition")
   var transitionDuration = 5000;
   var select = svg.select("circle");
   select
       .transition()
       .duration(transitionDuration)
       .attr("opacity", 0.0)
       .on("interrupt", function(d) { 
           console.log("interrupted"); 
       });
   console.log("exiting transition")
}

function chainedTransition(){
   console.log("starting transition")
   var transitionDuration = 5000;
   var select = svg.select("circle");
   select
       .transition()
       .duration(transitionDuration)
       .attr("opacity", 0.0);
   console.log("exiting transition")
}

function chainedInterruptTransition(){
   console.log("starting transition")
   var transitionDuration = 5000;
   var select = svg.select("circle");
   select
       .transition()
       .duration(transitionDuration)
       .attr("opacity", 0.0)
       .on("interrupt", function(d) { 
           console.log("interrupted 1"); 
       })
       .transition()
       .duration(transitionDuration)
       .attr("opacity", 1.0)
       .on("interrupt", function(d) { 
           console.log("interrupted 2"); 
       });
}
    
function interrupt()
   {
      svg.selectAll("*").interrupt(); // select all the visuals and for all of them, call interupt()
   }    

/* 19. Interactivity using the Mouse */
var select = svg.selectAll("circle")
                 .data(data);
select.enter()
      .append("circle")
      .on("mousemove", function (d) { 
           console.log(d3.event); // display all events
           console.log(d3.event.pageX, d3.event.pageY) // display position of mouse
      .on("mouseover", function (d) { console.log("mouseover")})
      .on("mouseout", function (d) { console.log("mouseout")})
      .on("mouseup", function (d) { console.log("mouseup")})
      .on("mousedown", function (d) { console.log("mousedown")})
      .on("click", function (d) { console.log("click")})
      .on("doubleclick", function (d) { console.log("doubleclick")})
})
    
