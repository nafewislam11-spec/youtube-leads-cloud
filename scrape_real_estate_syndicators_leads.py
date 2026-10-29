#!/usr/bin/env python3
"""
Kinetic Studio — Niche #3: Relocation Realtors, Syndicators & Custom Builders (20,000+ Query Ultra-Scale Edition)
=================================================================================================================
Dedicated Output CSV: /Users/khangadget/Documents/real_estate_syndicators_15k_new.csv
"""

import os
import re
import time
import argparse
from lead_engine_core import run_turbo_harvester, DOCUMENTS_DIR

DEFAULT_OUTPUT_CSV = os.path.join(DOCUMENTS_DIR, 'real_estate_syndicators_15k_new.csv')
LOG_FILE = os.path.join(DOCUMENTS_DIR, 'scrape_real_estate_syndicators.log')


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
    r'\btrue\s*crime\b', r'\bnews\s*channel\b', r'\bcake\b', r'\bbakery\b', r'\bcooking\b',
    r'\bcrochet\b', r'\buniversity\b', r'\bchurch\b', r'\bsermon\b', r'\bcold\s*email\b',
    r'\bforex\s*signals\b', r'\bmemecoin\b', r'\bget\s*rich\s*quick\b'
]
NEGATIVE_PATTERN = re.compile(r'(' + '|'.join(NEGATIVE_KEYWORDS) + r')', re.IGNORECASE)

POSITIVE_KEYWORDS = [
    r'\brealtor\b', r'\breal\s*estate\b', r'\bbroker\b', r'\bsyndication\b', r'\bmultifamily\b',
    r'\bcustom\s*home\b', r'\barchitect\b', r'\bbuilder\b', r'\brelocation\b', r'\bmoving\s*to\b',
    r'\bliving\s*in\b', r'\bhousing\s*market\b', r'\bproperty\b', r'\binvestor\b', r'\bcommercial\b',
    r'\binterior\s*design\b', r'\bremodel\b', r'\bhome\s*tour\b', r'\bluxury\s*homes?\b'
]
POSITIVE_PATTERN = re.compile(r'(' + '|'.join(POSITIVE_KEYWORDS) + r')', re.IGNORECASE)

# 150+ Deep Relocation Realtor, Syndicator, Commercial Broker & Custom Builder Micro-Niches
TARGET_NICHES = [
    # --- 1. RELOCATION & LOCAL MARKET REALTORS ---
    ("moving to realtor", "Relocation Realtor"),
    ("living in pros and cons realtor", "Relocation Realtor"),
    ("best suburbs to live in realtor", "Suburban Relocation Realtor"),
    ("relocating to real estate agent", "Relocation Real Estate Specialist"),
    ("new construction homes tour realtor", "New Construction Realtor"),
    ("builder incentives new homes realtor", "New Construction Specialist"),
    ("master planned community tour realtor", "Master-Planned Community Realtor"),
    ("55+ active adult community realtor", "Active Adult & Retirement Realtor"),
    ("luxury home listing agent tour", "Luxury Listing Agent"),
    ("waterfront lakefront homes realtor", "Waterfront Luxury Realtor"),
    ("golf course community homes realtor", "Golf & Country Club Realtor"),
    ("equestrian acreage homes realtor", "Ranch & Land Real Estate Agent"),
    ("historic homes neighborhood realtor", "Luxury & Historic Realtor"),
    ("downtown high rise condo realtor", "Urban Condo & Luxury Realtor"),
    ("housing market update realtor", "Local Market Realtor"),
    ("is the housing market crashing realtor", "Real Estate Market Analyst"),
    ("first time home buyer local realtor", "Buyer Specialist Realtor"),
    ("va loan military relocation realtor", "Military Relocation Realtor"),
    ("physician loan relocation realtor", "Luxury & Relocation Realtor"),
    ("selling your home listing agent tips", "Listing Specialist Realtor"),
    ("downsizer empty nester realtor", "Downsizing & Luxury Realtor"),
    ("vacation home second home realtor", "Resort & Second-Home Realtor"),
    ("mountain town resort real estate agent", "Resort & Mountain Realtor"),
    ("coastal beach homes real estate agent", "Coastal Luxury Realtor"),

    # --- 2. REAL ESTATE SYNDICATORS, FUNDS & COMMERCIAL BROKERS ---
    ("multifamily syndication capital raising", "Multifamily Real Estate Syndicator"),
    ("passive real estate investing syndication lp", "Real Estate Private Equity"),
    ("apartment syndication underwriting deal", "Apartment Syndicator"),
    ("value add multifamily acquisition", "Multifamily Investment Firm"),
    ("506c accredited investor real estate fund", "Real Estate Fund Manager"),
    ("preferred return waterfall syndication", "Real Estate Capital Raiser"),
    ("self storage investing syndication", "Self-Storage Syndicator"),
    ("mobile home park investing syndication", "MHP Fund & Syndicator"),
    ("rv park campground real estate investing", "Hospitality & RV Park Investor"),
    ("industrial warehouse flex space investing", "Industrial Real Estate Developer"),
    ("small bay industrial real estate broker", "Industrial Commercial Broker"),
    ("medical office building real estate investing", "Healthcare Real Estate Investor"),
    ("senior living assisted living real estate", "Senior Housing Syndicator"),
    ("student housing real estate investing", "Student Housing Developer"),
    ("build to rent btr community developer", "Build-To-Rent Developer"),
    ("land entitlement subdivision developer", "Land Development Firm"),
    ("infill spec home builder developer", "Spec Home Developer"),
    ("commercial real estate broker market update", "Commercial Real Estate Broker"),
    ("triple net lease nnn commercial broker", "NNN Commercial Broker"),
    ("retail strip center commercial broker", "Commercial Retail Broker"),
    ("multifamily investment sales broker", "Multifamily Commercial Broker"),
    ("tenant representation commercial broker", "Commercial Tenant Rep Broker"),
    ("1031 exchange Delaware statutory trust dst", "1031 Exchange & DST Advisor"),
    ("real estate debt fund hard money lender", "Private Real Estate Lender"),
    ("commercial mortgage broker dscr loan", "Commercial Mortgage Advisor"),
    ("hotel boutique hospitality investment", "Hospitality Real Estate Group"),

    # --- 3. CUSTOM HOME BUILDERS, REMODELERS, ARCHITECTS & DESIGNERS ---
    ("custom luxury home builder walkthrough", "Custom Luxury Home Builder"),
    ("cost to build a custom home builder", "Custom Home Builder"),
    ("build on your lot custom home builder", "Custom Home Builder"),
    ("modern farmhouse custom home builder", "Custom Home Builder"),
    ("contemporary luxury home builder", "Luxury Custom Builder"),
    ("barndominium custom builder walkthrough", "Specialty Custom Builder"),
    ("passive house net zero custom builder", "High-Performance Home Builder"),
    ("icf insulated concrete form home builder", "Custom Home Builder"),
    ("timber frame mountain home builder", "Luxury Timber Home Builder"),
    ("design build remodeling contractor", "Design-Build Remodeling Firm"),
    ("whole house luxury renovation contractor", "Luxury Renovation Builder"),
    ("kitchen and bath design build remodeler", "Kitchen & Bath Design-Build"),
    ("home addition second story builder", "Residential Design-Build Firm"),
    ("ADU backyard cottage builder contractor", "ADU & Custom Builder"),
    ("basement finishing design build contractor", "Specialty Remodeling Firm"),
    ("residential architect custom home design", "Residential Architecture Firm"),
    ("luxury home architect floor plan review", "Architecture Studio"),
    ("modern residential architect walkthrough", "Modern Architecture Firm"),
    ("coastal waterfront home architect", "Coastal Architecture Studio"),
    ("historic renovation residential architect", "Architecture & Restoration Firm"),
    ("luxury interior designer project reveal", "Luxury Interior Design Firm"),
    ("full service interior design studio tour", "Full-Service Interior Designer"),
    ("new build interior design selections", "Custom Home Interior Designer"),
    ("boutique hospitality commercial interior designer", "Commercial Interior Design Studio"),
    ("luxury landscape architect pool outdoor living", "Landscape Architecture Firm"),
    ("custom gunite pool builder outdoor kitchen", "Luxury Pool & Outdoor Builder")
]

ANGLES = [
    "", "pros and cons", "cost of living", "housing market update",
    "what you need to know", "mistakes to avoid", "neighborhood tour",
    "new construction", "complete breakdown", "2026 update", "honest truth",
    "case study", "cost breakdown", "step by step", "walkthrough"
]

FIT_NOTE_TEMPLATE = (
    "Verified {category} ({subs}) posting talking-head market/property videos ({length}); "
    "High commission/investor deal LTV ($15k-$100k+). {funnel}"
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Niche #3: Relocation Realtors, Syndicators & Custom Builders Scraper (20K+ Queries)")
    parser.add_argument('--target', type=int, default=15000)
    parser.add_argument('--min-subs', type=int, default=100)
    parser.add_argument('--max-subs', type=int, default=5000)
    parser.add_argument('--workers', type=int, default=12)
    parser.add_argument('--delay', type=float, default=0.15)
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT_CSV)
    args = parser.parse_args()

    run_turbo_harvester(
        script_title="NICHE #3: RELOCATION REALTORS, SYNDICATORS & CUSTOM BUILDERS (ULTRA-SCALE)",
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
