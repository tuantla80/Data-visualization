This file is to give some notes on:
#### 1. D3.js: To reduce the time when developing a data visualization dashboard using D3.js.
#### 2. Mathjax (https://www.mathjax.org): </br> 
   Refer to file <b> math_equation.html </b> at the folder for all implementation. </br> To display math equation beaitifully on the browser do the following steps.
- Step 1. Getting and configure it to display math equation inline with text or in a new line. (http://docs.mathjax.org/en/latest/configuration.html) </br>
    ```<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML' async></script>``` 
  
  ```
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
   ```
  
   ```<script type="text/javascript" src="path-to-MathJax/MathJax.js"> </script>``` 
   
 - Step 2: Choose an editor to convert math equation to Latex. Use one of the following:
     - https://www.latex4technics.com/
     - https://www.tutorialspoint.com/latex_equation_editor.htm
