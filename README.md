Sudocubes
=========

The goal of this project is to extract data from "3D" sudoku images, and solve them. This was used for a project for which we had a robot that had to navigate to a sudoku image, extract the data, solve the puzzle and then draw the digit that is supposed to be in the sudoku's red square.

Here's what a "3D" sudoku looks like.

<img src="https://raw.github.com/pobed2/sudocubes/master/images/cube_front1.jpg" alt="Sudocube" width=" 200px"/>

The sudokus are constructed as 3 4x4 grid of numbers. Just like a regular sudoku, the same number cannot appear twice in the same row, the same column and, in this case, the same blue rectangle.

The Algorithm
==============

There are two main parts to the algorithm solving this problem. The first one extracts the data from the image, while the second solves the puzzle.

Extracting the Data
-------------------

1. First of all, we have to keep in mind that the images of the sudokus come from a robot that had to navigate a long way    to get there. Therefore, we cannot guarantee that the image will be perfect. We have to take into account that the        sudoku will be warped and that we may even get other stuff in the picture.

  With that in mind, the first step of the process is to unwarp the image, in order to get a consistent image even if the   robot was slightly off its course. To do so, we are lucky enough to have a green square around the puzzle. All we have    to do is get the four corners of this square, and unwarp the square.

  Here's an example of how that's done (in strange pinkinsh colors...)


  <img src="https://raw.github.com/pobed2/sudocubes/master/images/begin.png" alt="Sudocube" width=" 200px" float="left"/>
  <img src="https://raw.github.com/pobed2/sudocubes/master/images/begin-square.png" alt="Sudocube" width=" 200px"           float="left"/>
  <img src="https://raw.github.com/pobed2/sudocubes/master/images/unwarped.png" alt="Sudocube" width=" 200px" float="left"/>
