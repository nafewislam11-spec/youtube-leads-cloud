#!/usr/bin/env python3
"""
Kinetic Studio — Niche #1: Tax Strategists, CPAs, Wealth Advisors & Attorneys (20,000+ Query Ultra-Scale Edition)
=================================================================================================================
Dedicated Output CSV: /Users/khangadget/Documents/tax_legal_wealth_15k_new.csv
"""

import os
import re
import time
import argparse
from lead_engine_core import run_turbo_harvester, DOCUMENTS_DIR

DEFAULT_OUTPUT_CSV = os.path.join(DOCUMENTS_DIR, 'tax_legal_wealth_15k_new.csv')
LOG_FILE = os.path.join(DOCUMENTS_DIR, 'scrape_tax_legal_wealth.log')


def log(msg):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(formatted + '\n')
    except Exception:
        pass


NEGATIVE_KEYWORDS = [
    r'\bfaceless\b', r'\bsound\s*bath\b', r'\bsinging\s*bowl\b', r'\bmeditation\s*music\b',
    r'\bsleep\s*music\b', r'\bbinaural\b', r'\basmr\b', r'\blofi\b', r'\bhypnosis\b', r'\btarot\b',
    r'\bastrology\b', r'#shorts\b', r'\b#short\b', r'\bdrama\b', r'\bmovie\b', r'\brecap\b',
    r'\bmanhwa\b', r'\banime\b', r'\bmanga\b', r'\bgaming\b', r'\bgameplay\b', r'\bprank\b',
    r'\breaction\b', r'\blyrics\b', r'\btrailer\b', r'\bcompilation\b', r'\bgossip\b',
    r'\btrue\s*crime\b', r'\bnews\s*channel\b', r'\bpolice\s*bodycam\b', r'\bcourt\s*cam\b',
    r'\blaw\s*&\s*crime\b', r'\bcake\b', r'\bbakery\b', r'\bcooking\b', r'\bcrochet\b',
    r'\buniversity\b', r'\bchurch\b', r'\bsermon\b', r'\bcold\s*email\b', r'\bforex\s*signals\b',
    r'\bmemecoin\b', r'\bcrypto\s*pump\b', r'\bget\s*rich\s*quick\b'
]
NEGATIVE_PATTERN = re.compile(r'(' + '|'.join(NEGATIVE_KEYWORDS) + r')', re.IGNORECASE)

POSITIVE_KEYWORDS = [
    r'\bcpa\b', r'\btax\b', r'\battorney\b', r'\blawyer\b', r'\blaw\s*firm\b',
    r'\bestate\s*planning\b', r'\btrust\b', r'\bwealth\b', r'\bfiduciary\b', r'\badvisor\b',
    r'\bcfp\b', r'\bretirement\b', r'\baccounting\b', r'\bcfo\b', r'\blegal\b',
    r'\bimmigration\b', r'\btrademark\b', r'\bpatent\b', r'\besq\b', r'\bclient\b'
]
POSITIVE_PATTERN = re.compile(r'(' + '|'.join(POSITIVE_KEYWORDS) + r')', re.IGNORECASE)

# 160+ Deep Micro-Niches & Technical Problem Topics (x 65 Geo Modifiers + 25 Angles = 15,000+ Unique Queries!)
TARGET_NICHES = [
    # --- 1. TAX STRATEGISTS & CPAs (55 Micro-Niches & Technical Topics) ---
    ("tax strategist business owner", "Tax Strategist"),
    ("cpa tax planning s corp", "CPA & Tax Planning"),
    ("s corp reasonable compensation cpa", "CPA & S-Corp Tax"),
    ("llc taxed as s corp cpa", "Business CPA"),
    ("augusta rule 14 day rental tax cpa", "Tax Strategist"),
    ("section 179 bonus depreciation cpa", "Tax Strategist"),
    ("qbi deduction 199a tax planning", "CPA & Tax Advisor"),
    ("real estate cpa tax strategy", "Real Estate CPA"),
    ("real estate professional status reps tax", "Real Estate Tax CPA"),
    ("short term rental tax loophole cpa", "STR Tax Strategist"),
    ("cost segregation study cpa tax", "Real Estate Tax Strategist"),
    ("1031 exchange tax rules cpa", "Real Estate Tax Advisor"),
    ("passive activity loss rules real estate cpa", "Real Estate CPA"),
    ("small business tax advisor cpa", "Small Business Tax Advisor"),
    ("high income earner tax reduction", "High-Net-Worth Tax Strategist"),
    ("w2 high earner tax strategy cpa", "Executive Tax Advisor"),
    ("physician doctor tax strategy cpa", "Medical & Physician CPA"),
    ("dentist medical practice cpa tax", "Dental & Healthcare CPA"),
    ("law firm accounting cpa tax", "Legal Accounting & CPA"),
    ("ecommerce shopify amazon cpa tax", "E-commerce CPA Firm"),
    ("construction contractor cpa accounting", "Construction CPA"),
    ("restaurant hospitality cpa accounting", "Hospitality CPA"),
    ("saas tech startup cpa r&d tax credit", "Startup & SaaS CPA"),
    ("qsbs 1202 capital gains exclusion tax", "M&A & Startup Tax Advisor"),
    ("83b election startup founder tax", "Startup Tax Strategist"),
    ("crypto capital gains tax cpa", "Crypto & Tax CPA"),
    ("day trader mark to market 475f cpa", "Trader Tax CPA"),
    ("international expat foreign earned income tax", "International Tax CPA"),
    ("fbar fatca foreign bank account cpa", "Cross-Border Tax Advisor"),
    ("canadian cross border tax cpa", "Cross-Border CPA"),
    ("irs tax resolution offer in compromise", "Tax Resolution Specialist"),
    ("irs audit defense tax attorney cpa", "Tax Controversy Advisor"),
    ("back taxes unfiled returns cpa", "Tax Resolution Firm"),
    ("payroll tax trust fund recovery cpa", "Business Tax Resolution"),
    ("virtual cfo accounting firm owner", "Virtual CFO & CPA Firm"),
    ("fractional cfo cash flow forecasting", "Fractional CFO & Advisory"),
    ("outsourced accounting controller firm", "Outsourced CFO & Accounting"),
    ("bookkeeping tax advisory firm", "Accounting & Tax Advisory"),
    ("quickbooks cleanup advisory cpa", "Accounting Advisory Firm"),
    ("partnership tax form 1065 cpa", "Partnership & Business CPA"),
    ("c corp vs s corp tax strategy", "Corporate Tax Advisor"),
    ("holding company wyoming delaware llc tax", "Asset & Tax Strategist"),
    ("hiring your kids tax strategy cpa", "Family Business Tax Advisor"),
    ("accountable plan reimbursement s corp", "S-Corp Tax Advisor"),
    ("defined benefit cash balance plan tax", "High-Income Tax Strategist"),
    ("solo 401k mega backdoor roth cpa", "Retirement Tax Strategist"),
    ("self directed ira real estate cpa", "SDIRA & Tax Advisor"),
    ("nonprofit 501c3 cpa accounting", "Nonprofit CPA Firm"),
    ("estate and gift tax return cpa", "Trust & Estate CPA"),
    ("fiduciary trust accounting cpa", "Trust & Estate Tax Advisor"),
    ("state residency tax audit california new york", "State & SALT Tax Advisor"),
    ("multistate nexus sales tax cpa", "SALT & Sales Tax CPA"),
    ("business exit tax planning cpa", "Exit & M&A Tax Advisor"),
    ("installment sale capital gains tax cpa", "Capital Gains Tax Strategist"),
    ("opportunity zone capital gains tax", "Investment Tax Advisor"),

    # --- 2. FIDUCIARY WEALTH ADVISORS & CFPs (45 Micro-Niches & Technical Topics) ---
    ("fiduciary financial advisor retirement", "Fiduciary Wealth Advisor"),
    ("certified financial planner cfp retirement", "Certified Financial Planner (CFP)"),
    ("fee only financial advisor ria", "Fee-Only RIA Wealth Advisor"),
    ("independent wealth management firm founder", "Private Wealth Manager"),
    ("retirement income planning advisor", "Retirement Planning Advisor"),
    ("roth conversion ladder retirement cfp", "Retirement & Tax Planner"),
    ("rmd required minimum distribution strategy", "Retirement Tax Planner"),
    ("irmaa medicare surcharge retirement planning", "Retirement Healthcare & Tax Planner"),
    ("social security claiming strategy 62 67 70", "Retirement Income Specialist"),
    ("401k rollover ira retirement advisor", "401(k) & Retirement Advisor"),
    ("sequence of returns risk retirement", "Retirement Portfolio Advisor"),
    ("bucket strategy retirement income cfp", "Retirement Income Planner"),
    ("guardrails withdrawal strategy retirement", "Fiduciary Retirement Planner"),
    ("high net worth wealth management advisor", "Private Wealth Advisor"),
    ("ultra high net worth family office advisor", "Family Office Advisor"),
    ("physician financial planner white coat", "Physician Wealth Advisor"),
    ("dentist practice owner wealth advisor", "Dental Wealth Advisor"),
    ("attorney law partner wealth advisor", "Legal Executive Wealth Advisor"),
    ("tech executive rsu iso stock options advisor", "Tech Equity Wealth Advisor"),
    ("concentrated stock position tax loss harvesting", "Executive Portfolio Strategist"),
    ("direct indexing tax efficient investing advisor", "Tax-Aware Wealth Manager"),
    ("business owner exit wealth planner", "Exit & Liquidity Wealth Planner"),
    ("pre liquidity event wealth planning", "Founder Wealth Advisor"),
    ("federal employee fers tsp retirement planner", "Federal Retirement Advisor"),
    ("military retirement pension financial planner", "Military & Veteran Wealth Advisor"),
    ("airline pilot retirement financial advisor", "Pilot & Executive Wealth Advisor"),
    ("educator 403b 457b retirement planner", "Educator Retirement Planner"),
    ("widow divorce financial planner cdfa", "Life Transition Wealth Advisor"),
    ("sudden wealth inheritance financial advisor", "Inheritance & Trust Advisor"),
    ("donor advised fund charitable giving advisor", "Philanthropic & Wealth Advisor"),
    ("charitable remainder trust wealth planner", "Legacy & Estate Wealth Advisor"),
    ("529 college funding financial planner", "Family Wealth Planner"),
    ("long term care insurance retirement planner", "Longevity & Retirement Advisor"),
    ("private credit alternative investments advisor", "Private Wealth Strategist"),
    ("christian financial advisor biblical stewardship", "Faith-Based Wealth Advisor"),
    ("halal investing islamic financial advisor", "Ethical & Specialty Wealth Advisor"),
    ("womens wealth financial advisor", "Women's Wealth Strategist"),
    ("late starter retirement catch up advisor", "Retirement Catch-Up Planner"),
    ("early retirement fire financial planner", "Early Retirement CFP"),
    ("expat cross border financial planner", "International Wealth Advisor"),

    # --- 3. NICHE ATTORNEYS & LAW FIRMS (60 Micro-Niches & Technical Topics) ---
    ("estate planning attorney living trust", "Estate Planning Attorney"),
    ("revocable living trust vs will lawyer", "Trusts & Estates Attorney"),
    ("irrevocable trust asset protection attorney", "Asset Protection & Trust Lawyer"),
    ("avoiding probate estate planning lawyer", "Probate & Estate Attorney"),
    ("step up in basis living trust attorney", "Estate & Tax Planning Lawyer"),
    ("lady bird deed transfer on death attorney", "Real Estate & Estate Lawyer"),
    ("special needs trust estate attorney", "Special Needs Estate Lawyer"),
    ("elder law medicaid asset protection attorney", "Elder Law & Medicaid Attorney"),
    ("nursing home medicaid spend down lawyer", "Elder Law Firm"),
    ("probate estate administration attorney", "Probate Litigation & Estate Lawyer"),
    ("trust contest inheritance dispute lawyer", "Trust & Probate Litigation Firm"),
    ("dynasty trust generation skipping attorney", "High-Net-Worth Estate Lawyer"),
    ("domestic asset protection trust lawyer", "Asset Protection Law Firm"),
    ("offshore cook islands trust attorney", "International Asset Protection Lawyer"),
    ("llc piercing the corporate veil attorney", "Corporate & Asset Protection Lawyer"),
    ("llc operating agreement business attorney", "Business Formation Attorney"),
    ("wyoming vs delaware llc holding company lawyer", "Corporate Structuring Attorney"),
    ("series llc real estate asset protection lawyer", "Real Estate Asset Protection Lawyer"),
    ("immigration lawyer eb2 niw green card", "Immigration Attorney (EB-2/NIW)"),
    ("eb1a extraordinary ability immigration lawyer", "EB-1A / O-1 Immigration Lawyer"),
    ("o1 visa artist founder immigration attorney", "Business Immigration Attorney"),
    ("e2 treaty investor visa lawyer", "Investor Visa Immigration Lawyer"),
    ("l1a executive transfer visa attorney", "Corporate Immigration Law Firm"),
    ("eb5 immigrant investor visa attorney", "EB-5 Investment Immigration Lawyer"),
    ("h1b perm labor certification lawyer", "Employment Immigration Lawyer"),
    ("marriage green card adjustment of status lawyer", "Family Immigration Law Firm"),
    ("k1 fiance visa consular processing lawyer", "Family Immigration Attorney"),
    ("uscis rfe response immigration attorney", "Immigration Law Firm"),
    ("deportation defense cancellation of removal lawyer", "Immigration Defense Attorney"),
    ("trademark attorney uspto registration", "Trademark & IP Attorney"),
    ("trademark office action likelihood of confusion lawyer", "USPTO Trademark Lawyer"),
    ("amazon brand registry trademark attorney", "E-commerce IP & Brand Lawyer"),
    ("patent attorney provisional utility patent", "Patent & IP Attorney"),
    ("software ai patent attorney", "Tech Patent Law Firm"),
    ("copyright infringement dmca entertainment lawyer", "Entertainment & Media Lawyer"),
    ("music publishing recording contract lawyer", "Music & Entertainment Attorney"),
    ("influencer creator brand deal contract lawyer", "Creator Economy Attorney"),
    ("saas master services agreement technology lawyer", "SaaS & Tech Transactions Lawyer"),
    ("data privacy gdpr ccpa compliance attorney", "Privacy & Cybersecurity Lawyer"),
    ("mergers and acquisitions lawyer buying a business", "M&A & Business Acquisition Lawyer"),
    ("sba 7a business acquisition attorney", "SMB Acquisition & M&A Lawyer"),
    ("letter of intent loi purchase agreement lawyer", "M&A Transaction Attorney"),
    ("seller financing earnout m&a attorney", "Corporate M&A Law Firm"),
    ("franchise law attorney fdd review", "Franchise Attorney"),
    ("how to franchise your business lawyer", "Franchise Development Lawyer"),
    ("real estate syndication 506b 506c securities attorney", "SEC & Real Estate Syndication Lawyer"),
    ("private placement memorandum ppm attorney", "Private Equity & Securities Lawyer"),
    ("commercial real estate lease review attorney", "Commercial Real Estate Lawyer"),
    ("construction defect mechanic lien attorney", "Construction Law Firm"),
    ("hoa condo association real estate lawyer", "Real Estate & Property Lawyer"),
    ("landlord tenant eviction real estate attorney", "Real Estate Litigation Lawyer"),
    ("employment law attorney employer defense", "Employer Defense & HR Lawyer"),
    ("non compete severance agreement employment lawyer", "Executive Employment Attorney"),
    ("healthcare stark law hipaa medical attorney", "Healthcare & Medical Practice Lawyer"),
    ("medspa medical director compliance attorney", "Aesthetic & Healthcare Lawyer"),
    ("physician employment contract review attorney", "Medical Contract Attorney"),
    ("high net worth divorce family law attorney", "High-Asset Family Law Firm"),
    ("prenuptial postnuptial agreement lawyer", "Matrimonial & Family Lawyer"),
    ("business valuation in divorce family lawyer", "Complex Divorce Attorney"),
    ("child custody mediation family law attorney", "Family & Custody Law Firm"),
    ("chapter 11 subchapter v small business bankruptcy lawyer", "Business Restructuring Lawyer"),
    ("veterans va disability appeals attorney", "VA Disability Law Firm"),
    ("erisa long term disability insurance attorney", "Disability Insurance Lawyer"),
    ("personal injury commercial truck accident lawyer", "Personal Injury Trial Firm")
]

ANGLES = [
    "", "mistakes to avoid", "what you need to know", "complete breakdown",
    "case study", "step by step", "my honest advice", "2026 update",
    "how it works", "questions to ask", "strategy breakdown", "explained",
    "pros and cons", "cost breakdown", "checklist", "common myths"
]

FIT_NOTE_TEMPLATE = (
    "Verified {category} ({subs}) posting talking-head advisory content ({length}); "
    "High-ticket client LTV ($5k-$30k+). {funnel}"
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Niche #1: Tax, CPA, Wealth & Legal YouTube Lead Scraper (20K+ Queries)")
    parser.add_argument('--target', type=int, default=15000)
    parser.add_argument('--min-subs', type=int, default=100)
    parser.add_argument('--max-subs', type=int, default=5000)
    parser.add_argument('--workers', type=int, default=12)
    parser.add_argument('--delay', type=float, default=0.15)
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT_CSV)
    args = parser.parse_args()

    run_turbo_harvester(
        script_title="NICHE #1: TAX STRATEGISTS, CPAs, WEALTH ADVISORS & ATTORNEYS (ULTRA-SCALE)",
        target_niches=TARGET_NICHES,
        angles=ANGLES,
        negative_pattern=NEGATIVE_PATTERN,
        positive_pattern=POSITIVE_PATTERN,
        fit_note_template=FIT_NOTE_TEMPLATE,
        output_csv=args.output,
        log_fn=log,
        target_leads=args.target,
        min_subs=args.min_subs,
        max_subs=args.max_subs,
        workers=args.workers,
        delay=args.delay
    )
