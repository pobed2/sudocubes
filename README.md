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

### Unwarping

  First of all, we have to keep in mind that the images of the sudokus come from a robot that had to navigate a long way    to get there. Therefore, we cannot guarantee that the image will be perfect. We have to take into account that the        sudoku will be warped and that we may even get other stuff in the picture.

  With that in mind, the first step of the process is to unwarp the image, in order to get a consistent image even if the   robot was slightly off its course. To do so, we are lucky enough to have a green square around the puzzle. All we have    to do is get the four corners of this square, and unwarp the square.

  Here's an example of how that's done (in strange pinkinsh colors...)


  <img src="https://raw.github.com/pobed2/sudocubes/master/images/begin.png" alt="Sudocube" width=" 200px" float="left"/>
  <img src="https://raw.github.com/pobed2/sudocubes/master/images/begin-square.png" alt="Sudocube" width=" 200px"           float="left"/>
  <img src="https://raw.github.com/pobed2/sudocubes/master/images/unwarped.png" alt="Sudocube" width=" 200px" float="left"/>

### Finding the corners
  We then have to find the corners to the "box". Doing so will enable us to define the puzzle's boundaries and the placement of the digits' squares. To do so, we have to use a few tricks.
  1. We first isolate the puzzle's box by its color.
  2. Then, we use OpenCV's power to find possible corners.
  3. By simple geometry, we are able to find the best matches for possible corners.
  
  <img src="https://raw.github.com/pobed2/sudocubes/master/images/lines.png" alt="Sudocube" width=" 200px" float="left"/>
  <img src="https://raw.github.com/pobed2/sudocubes/master/images/all-points.png" alt="Sudocube" width=" 200px"           float="left"/>
  <img src="https://raw.github.com/pobed2/sudocubes/master/images/corners.png" alt="Sudocube" width=" 200px" float="left"/>

### Extracting the digits
  Once we have the box's corners, it's a simple matter of geometry to find the possible places where digits might be. Therefore, the harder part is to actually get the right digit from the image. 
  
  In order to keep it simple, we simply trained a regular classifier using the k-nearest neighboors algorithm. To do so, we fed the classifier a series a images containing digits that were manually identified beforehand. This enabled the classifier to compare the digits in the puzzle to the digits it already knew. Because it is a simple OCR problem (same font, same size), the KNN classifier works like a charm.
  
Solving the sudoku
------------------
Sudoku solving solutions are abundant on the Internet. However, this particular puzzle is quite different from a regular sudoku. Therefore, we had to write a specific solving algorithm.

The algorithm used is largely based on a sudoku solving algorithm written by Peter Norvig. We were able to reuse a sudoky solving algorithm because both sukodus and "3D" sudokus are constraint satisfaction problems. Therefore, all we had to do was modify the constraints. The algorithm works in two ways.
  1. Constraints are propagated troughout the problem set to find a solution
  2. Depth first searches aretried, whenever we try a new solution.

A solution is usually found within a few milliseconds (on the robot's computer: an old mac mini).

