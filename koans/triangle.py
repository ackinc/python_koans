#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Triangle Project Code.

# Triangle analyzes the lengths of the sides of a triangle
# (represented by a, b and c) and returns the type of triangle.
#
# It returns:
#   'equilateral'  if all sides are equal
#   'isosceles'    if exactly 2 sides are equal
#   'scalene'      if no sides are equal
#
# The tests for this method can be found in
#   about_triangle_project.py
# and
#   about_triangle_project_2.py
#
def triangle(a, b, c):
    # DELETE 'PASS' AND WRITE THIS CODE
    if a <= 0 or b <= 0 or c <= 0:
        raise TriangleError('Sides must have positive length')
    elif a + b <= c or b + c <= a or c + a <= b:
        raise TriangleError('Sum of any two sides must be greater than the third')
    elif a == b == c:
        return 'equilateral'
    elif a != b and b != c and c != a:
        return 'scalene'
    else:
        return 'isosceles'

# Error class used in part 2.  No need to change this code.
class TriangleError(Exception):
    pass
