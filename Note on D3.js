/* This file is to give some notes on D3.js so that it will reduce the time when developing a data visualization
dashboard using D3.js.
   For a full code of one particular example, please refer to https://bl.ocks.org/
*/

// 1. Loading data *.json, *.csv, *.tsv,... Using map() function
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