import unittest
import numpy as np,pandas as pd
from v86_heat_fear_regime import V86Allocator,V86Config
class Tests(unittest.TestCase):
 def setUp(self):
  i=pd.bdate_range("2018-01-01",periods=400);self.c=pd.DataFrame({"SPY":np.linspace(100,180,400),"QQQ":np.linspace(100,230,400)},index=i);self.v=pd.DataFrame({"^VIX":15.,"^VIX3M":18.},index=i)
 def test_hot(self):
  a=V86Allocator(self.c,self.v,V86Config(.7,5,4,.25,1));t=a.target(self.c.index[-1]);self.assertEqual(a.state,"hot");self.assertAlmostEqual(t["QQQ"],.7)
 def test_fear_overrides_heat(self):
  v=self.v.copy();v.iloc[-6:,0]=40;v.iloc[-6:,1]=30;a=V86Allocator(self.c,v,V86Config(.7,5,3,.25,1));t=a.target(self.c.index[-1]);self.assertEqual(a.state,"fear");self.assertLessEqual(sum(t.values()),.25)
 def test_confirmation(self):
  a=V86Allocator(self.c,self.v,V86Config(.7,5,4,.25,2));a.target(self.c.index[-1]);self.assertEqual(a.state,"normal")
 def test_no_leverage(self):
  a=V86Allocator(self.c,self.v,V86Config());self.assertLessEqual(sum(a.target(self.c.index[-1]).values()),1)
if __name__=="__main__":unittest.main()
