import unittest
import numpy as np,pandas as pd
from v85_heat_regime import V85Allocator,V85Config
class Tests(unittest.TestCase):
 def setUp(self):
  i=pd.bdate_range("2018-01-01",periods=400);self.up=pd.DataFrame({"SPY":np.linspace(100,180,400),"QQQ":np.linspace(100,240,400)},index=i)
 def test_hot_tilt(self):
  a=V85Allocator(self.up,V85Config(.7,0,None,.25,1));t=a.target(self.up.index[-1]);self.assertAlmostEqual(t["QQQ"],.7);self.assertAlmostEqual(sum(t.values()),1)
 def test_confirmation_delays_switch(self):
  a=V85Allocator(self.up,V85Config(.7,0,None,.25,2));t=a.target(self.up.index[-1]);self.assertEqual(a.state,"normal");self.assertAlmostEqual(t["QQQ"],.5)
 def test_no_leverage(self):
  a=V85Allocator(self.up,V85Config());self.assertLessEqual(sum(a.target(self.up.index[-1]).values()),1)
 def test_invalid(self):
  with self.assertRaises(ValueError):V85Config(.9)
if __name__=="__main__":unittest.main()
