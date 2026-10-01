"""Constrained allocation using concave response curves and held-out evaluation."""
import itertools
import math
import random
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import database, export_query, report, table, write_csv

ROOT=Path(__file__).resolve().parent
CHANNELS=['Search','Social','Display','Affiliate']


def response(spend,a,b): return a*(1-math.exp(-spend/b))


def fit(rows):
    """Grid-search b, solve least-squares a analytically; train rows only."""
    best=None
    for b in range(2000,30001,250):
        x=[1-math.exp(-r['spend_usd']/b) for r in rows]
        a=sum(v*r['incremental_members'] for v,r in zip(x,rows))/sum(v*v for v in x)
        loss=sum((a*v-r['incremental_members'])**2 for v,r in zip(x,rows))
        if best is None or loss<best[0]: best=(loss,a,b)
    return best[1:]


def optimize(params,budget=40000,minimum=4000,maximum=16000,step=1000):
    """Exact search at declared $1,000 granularity; all constraints explicit."""
    best=None
    for first in itertools.product(range(minimum,maximum+1,step),repeat=3):
        last=budget-sum(first)
        if last<minimum or last>maximum or last%step: continue
        allocations=(*first,last)
        gain=sum(response(s,*params[c]) for c,s in zip(CHANNELS,allocations))
        if best is None or gain>best[0]: best=(gain,allocations)
    if best is None: raise ValueError('Budget cannot satisfy allocation constraints')
    return best


def main():
    rng=random.Random(63)
    truth={'Search':(650,8500),'Social':(1100,18000),'Display':(450,15000),'Affiliate':(550,7000)}
    rows=[]
    for channel in CHANNELS:
        for week in range(1,17):
            spend=4000+((week-1)%8)*2000
            y=max(0,round(response(spend,*truth[channel])+rng.gauss(0,12),2))
            rows.append(dict(channel=channel,week=week,spend_usd=spend,incremental_members=y,split='train' if week<=12 else 'test'))
    write_csv(ROOT/'data/calibration.csv',rows)
    db=database(ROOT/'outputs/analysis.sqlite',{'calibration':rows})
    calibration=export_query(db,ROOT/'analysis.sql',ROOT/'outputs/calibration_summary.csv')
    params={c:fit([r for r in rows if r['channel']==c and r['split']=='train']) for c in CHANNELS}
    fitted=[]
    for c,(a,b) in params.items():
        test=[r for r in rows if r['channel']==c and r['split']=='test']
        mae=sum(abs(response(r['spend_usd'],a,b)-r['incremental_members']) for r in test)/len(test)
        fitted.append(dict(channel=c,saturation_members=round(a,2),scale_spend_usd=b,holdout_mae_members=round(mae,2)))
    gain,allocation=optimize(params)
    base=sum(response(10000,*params[c]) for c in CHANNELS)
    plan=[dict(channel=c,baseline_spend_usd=10000,recommended_spend_usd=s,change_usd=s-10000,
               expected_incremental_members=round(response(s,*params[c]),2),
               marginal_members_per_1000=round(response(s+1000,*params[c])-response(s,*params[c]),2)) for c,s in zip(CHANNELS,allocation)]
    scenarios=[]
    # Re-evaluate the same proposed allocation under response uncertainty.
    for label,multipliers in [('Base',[1,1,1,1]),('Social response -20%',[1,.8,1,1]),('Search response -20%',[.8,1,1,1]),('Affiliate response -20%',[1,1,1,.8])]:
        b=sum(m*response(10000,*params[c]) for c,m in zip(CHANNELS,multipliers))
        g=sum(m*response(s,*params[c]) for c,s,m in zip(CHANNELS,allocation,multipliers))
        scenarios.append(dict(scenario=label,baseline_members=round(b,2),proposed_members=round(g,2),expected_gain_pct=round(100*(g/b-1),2)))
    for filename,data in [('allocation',plan),('model_validation',fitted),('sensitivity',scenarios)]: write_csv(ROOT/f'outputs/{filename}.csv',data)
    report(ROOT,'Marketing Investment & Budget Allocation',{'Weekly budget':'$40,000','Modeled member gain':f'{gain/base-1:.1%}','Allocation step':'$1,000','Holdout points':16},
           [table('Budget recommendation',plan,'channel','recommended_spend_usd'),table('Held-out model checks',fitted,'channel','holdout_mae_members'),table('Sensitivity scenarios',scenarios,'scenario','expected_gain_pct'),table('Calibration evidence',calibration,'channel','pooled_incremental_cac')],
           [f"The model projects {gain/base-1:.1%} more incremental members than an equal $10,000-per-channel allocation at the same total spend. This is a scenario estimate, not an achieved improvement.",
            'Respect $4,000 channel floors and $16,000 caps; saturation prevents allocating everything to the channel with the lowest historical average CAC.',
            f"Under the modeled response shocks, gains range from {min(s['expected_gain_pct'] for s in scenarios):.2f}% to {max(s['expected_gain_pct'] for s in scenarios):.2f}%. Approve a small, measured reallocation before scaling.",
            'Ask Growth Marketing to confirm inventory limits, Finance to confirm spend ceilings, and the measurement owner to supply real incrementality calibrations.'],
           'Response curves are fitted to synthetic calibration points representing hypothetical experiments. There are 12 training and 4 held-out points per channel. Noise is deliberately mild; real-world confounding, seasonality, overlap, and interaction effects are absent. Results assume independent channel responses and stable curves. Sensitivity cases are stress tests, not confidence intervals. Exact optimum applies only to the stated discrete grid. No advertising money was spent.')
    db.close()


if __name__=='__main__': main()
