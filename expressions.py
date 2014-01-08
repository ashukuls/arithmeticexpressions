#!/usr/bin/python
"""
Build single digit arithmetic expressions that use basic operations - add,
subtract, multiply, divide, power and modulo. For example, 2014 = 5^5 - 5555/5.

Author: Ashutosh Kulshreshtha
"""

import argparse
import math

class SingleDigitExpressions(object):
  """Build possible (expression, value) sets with a given digit."""

  def __init__(self, digit, args):
    """Get expressions using a single digit. args control the exploration."""
    self.digit = digit
    # In order to make the problem tractable, rather than exploring the N*N
    # combinations, we keep the set of small expressions, which would be finite
    # say K. And try only K*N combinations.
    self.small = self.Initialize(self.digit)
    self.full = self.Initialize(self.digit)

    # Arguments to control the exploration.
    self.max_value = args.max_value
    self.small_expression_len = args.max_small_expression_length
    self.max_expression_len = args.max_expression_length

    for i in range(args.iterations):
      self.ExploreCombinations()
      print "digit %d iteration %d small %d dict size %d" % (self.digit, i, len(self.small), len(self.full))

  def GetExpression(self, value):
    """Find expression for the value, if available."""
    return self.full.get(value, None)

  def Initialize(self, digit):
    """Initial set of expressions for the digit."""
    bag = {}
    bag[digit] = str(digit)
    bag[11 * digit] = str(11 * digit)
    bag[111 * digit] = str(111 * digit)
    bag[1111 * digit] = str(1111 * digit)
    bag[11111 * digit] = str(11111 * digit)
    bag[111111 * digit] = str(111111 * digit)
    return bag

  def MayBeAddExpression(self, value, expr):
    """Possible add the new (value, expression) combination to the sets."""
    if (value < 0 or value > self.max_value
        or len(expr) > self.max_expression_len):
      return

    # Add to the set of small expressions.
    if len(expr) <= self.small_expression_len:
      old_expr = self.small.get(value, None)
      if not old_expr or len(old_expr) > expr:
        self.small[value] = expr

    # Add to full set.
    if len(expr) <= self.max_expression_len:
      old_expr = self.full.get(value, None)
      if not old_expr or len(old_expr) > expr:
        self.full[value] = expr

  def ExploreCombinations(self):
    """Combine expressions from the current sets to generate more values."""
    bag = {}
    for (k1, v1) in self.small.iteritems():
      for (k2, v2) in self.full.iteritems():
        if len(v1) + len(v2) > self.max_expression_len:
          continue
        bag[k1 + k2] = "(%s+%s)" % (v1, v2)
        if k1 < 1000 or k2 < 1000:
          bag[k1 * k2] = "(%s*%s)" % (v1, v2)
        # Only build positive values.
        if k1 > k2:
          bag[k1 - k2] = "(%s-%s)" % (v1, v2)
        # Only consider divisions resulting in integers.
        if k2 > 0 and k1 > k2 and not k1 % k2:
          bag[k1 / k2] = "(%s/%s)" % (v1, v2)
        try:
          # x^y could potentially result in Overflow error. Also only one power
          # per expressions should be good enough. 3^3^3 ~ 10^12, and
          # multiplication will take care of ^2.
          if k2 < 20 and "^" not in v1 and "^" not in v2:
            p = math.pow(k1, k2)
            bag[p] = "(%s^%s)" % (v1, v2)
        except OverflowError:
          pass
        except ValueError:
          pass
    current_size = len(self.full)
    for (k, v) in bag.iteritems():
      self.MayBeAddExpression(k, v)
    print "current %d new %d added %d" % (
        current_size, len(bag), len(self.full) - current_size)

def GetExpressions(values, digits, args):
  """Get expressions for given values using provided digits."""
  for i in digits:
    sde = SingleDigitExpressions(i, args)
    for x in values:
      print x, sde.GetExpression(x)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--max_value', default=100000,
                      help='max expression value to consider.')
  parser.add_argument('--max_small_expression_length', default=16,
                      help='max length for small expressions.')
  parser.add_argument('--max_expression_length', default=40,
                      help='max length for any expression.')
  parser.add_argument('--iterations', default=6,
                      help='Number of iterations to explore expression sets.')
  args = parser.parse_args()

  digits = range(1, 10)
  values = range(2010, 2020)
  GetExpressions(values, digits, args)

if __name__ == "__main__":
  main()
