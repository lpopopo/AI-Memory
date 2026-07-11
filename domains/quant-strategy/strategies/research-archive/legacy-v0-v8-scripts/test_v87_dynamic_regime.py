import unittest
import numpy as np,pandas as pd
from v87_dynamic_regime import V87Allocator,V87Config,rolling_percentile
class Tests(unittest.TestCase):
 def test_percentile_is_causal(self):
  s=pd.Series(np.arange(300,dtype=float));p=rolling_percentile(s);self.assertAlmostEqual(p.iloc[-1],1);s2=s.copy();s2.loc[299]=0;self.assertLess(rolling_percentile(s2).iloc[-1],.1)
 def test_no_leverage(self):
  i=pd.bdate_range("2018-01-01",periods=900);c=pd.DataFrame({"SPY":np.linspace(100,200,900),"QQQ":np.linspace(100,260,900)},index=i);v=pd.DataFrame({"^VIX":15.,"^VIX3M":18.},index=i);a=V87Allocator(c,v,V87Config(.7,70,80,.5,1));self.assertLessEqual(sum(a.target(i[-1]).values()),1)
 def test_fear_requires_weak_trend(self):
  i=pd.bdate_range("2018-01-01",periods=900);c=pd.DataFrame({"SPY":np.linspace(100,200,900),"QQQ":np.linspace(100,260,900)},index=i);v=pd.DataFrame({"^VIX":np.r_[np.full(899,10.),40.],"^VIX3M":np.r_[np.full(899,15.),30.]},index=i);a=V87Allocator(c,v,V87Config(.7,70,75,.5,1));a.target(i[-1]);self.assertNotEqual(a.state,"fear")
if __name__=="__main__":unittest.main()
