import unittest
import numpy as np,pandas as pd
from v84_breadth_filter import V84Allocator,V84Config,build_breadth
class Tests(unittest.TestCase):
 def test_breadth_membership_and_overlay(self):
  idx=pd.bdate_range("2020-01-01",periods=260); stocks=pd.DataFrame({"A":np.arange(260)+100,"B":np.arange(260)[::-1]+100},index=idx)
  h=pd.DataFrame({"symbol":["A","B"],"opt-in":[idx[0],idx[0]],"opt-out":[pd.NaT,pd.NaT]}); b=build_breadth(stocks,h,100); self.assertAlmostEqual(b.dropna().iloc[-1],.5)
  close=pd.DataFrame({"SPY":np.arange(260)+100,"QQQ":np.arange(260)+100},index=idx); a=V84Allocator(close,V84Config(100,.6,.5),b);t=a.target(idx[-1]);self.assertAlmostEqual(sum(t.values()),.5)
 def test_no_leverage(self):
  idx=pd.bdate_range("2020-01-01",periods=260);c=pd.DataFrame({"SPY":np.arange(260)+100,"QQQ":np.arange(260)+100},index=idx);a=V84Allocator(c,V84Config());self.assertLessEqual(sum(a.target(idx[-1]).values()),1)
if __name__=="__main__":unittest.main()
