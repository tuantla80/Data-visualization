This file is to give some notes on:
1. D3.js: To reduce the time when developing a data visualization dashboard using D3.js.
2. Mathjax (https://www.mathjax.org): 
   Refer to file math_equation.html at the folder for all implementation
   To display math equation beaitifully on the browser.
   - Step 1. Getting and configure it 
            (to display math equation inline with text or in a new line. http://docs.mathjax.org/en/latest/configuration.html)
    <script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML' async></script>
    <script type="text/x-mathjax-config">
      MathJax.Hub.Config({
        extensions: ["tex2jax.js"],
        jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {
          inlineMath: [ ['$','$'], ["\\(","\\)"] ],
          displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
          processEscapes: true
        },
        "HTML-CSS": { fonts: ["TeX"] }
      });
    </script>
    <script type="text/javascript" src="path-to-MathJax/MathJax.js"> </script>
    - Step 2: Choose an editor to convert math equation to Latex. Use one of the following:
        - https://www.latex4technics.com/
        - https://www.tutorialspoint.com/latex_equation_editor.htm
