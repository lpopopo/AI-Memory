import unittest
from backtest_v8_institutional_long_history import flow_fragility
from backtest_market_sentiment_overlay import load_data

class LongHistoryInstitutionalTests(unittest.TestCase):
 def test_flow_score_is_bounded(self):
  d=load_data();d["SMH"]=d["QQQ"]
  s=flow_fragility(d.dropna(subset=["SPY","QQQ"]));self.assertGreaterEqual(s.dropna().min(),0);self.assertLessEqual(s.dropna().max(),12)

if __name__=="__main__":unittest.main()
