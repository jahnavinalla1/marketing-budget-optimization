import math
import sqlite3
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import run
lift=budget=reporting=run

class AllocationTests(unittest.TestCase):
    def test_budget_constraints_and_dominates_equal_split(self):
        params={c:(500+100*i,8000+2000*i) for i,c in enumerate(budget.CHANNELS)}
        gain,allocation=budget.optimize(params)
        self.assertEqual(sum(allocation),40000)
        self.assertTrue(all(4000<=s<=16000 for s in allocation))
        self.assertGreaterEqual(gain,sum(budget.response(10000,*params[c]) for c in budget.CHANNELS))

    def test_symmetric_optimum_is_equal(self):
        params={c:(600,8000) for c in budget.CHANNELS}
        self.assertEqual(budget.optimize(params)[1],(10000,10000,10000,10000))

    def test_infeasible_budget(self):
        with self.assertRaises(ValueError):budget.optimize({c:(600,8000) for c in budget.CHANNELS},budget=1000)

    def test_curve_recovery(self):
        rows=[dict(spend_usd=x,incremental_members=budget.response(x,700,10000)) for x in range(4000,19000,2000)]
        a,b=budget.fit(rows)
        self.assertAlmostEqual(a,700)
        self.assertEqual(b,10000)

if __name__=='__main__':unittest.main()
