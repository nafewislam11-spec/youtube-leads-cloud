#!/usr/bin/env python3
"""
Kinetic Studio — Niche #4: Boutique B2B Agency & Service Founders (20,000+ Query Ultra-Scale Edition)
=====================================================================================================
Dedicated Output CSV: /Users/khangadget/Documents/b2b_boutique_agencies_15k_new.csv
"""

import os
import re
import time
import argparse
from lead_engine_core import run_turbo_harvester, DOCUMENTS_DIR

DEFAULT_OUTPUT_CSV = os.path.join(DOCUMENTS_DIR, 'b2b_boutique_agencies_15k_new.csv')
LOG_FILE = os.path.join(DOCUMENTS_DIR, 'scrape_b2b_boutique_agencies.log')


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
    r'\binstantly\.ai\b', r'\bsmartlead\b', r'\bclay\.com\b', r'\bforex\s*signals\b',
    r'\bmemecoin\b', r'\bget\s*rich\s*quick\b'
]
NEGATIVE_PATTERN = re.compile(r'(' + '|'.join(NEGATIVE_KEYWORDS) + r')', re.IGNORECASE)

POSITIVE_KEYWORDS = [
    r'\bagency\b', r'\bfounder\b', r'\bseo\b', r'\bcro\b', r'\bwebflow\b', r'\bframer\b',
    r'\bshopify\b', r'\bklaviyo\b', r'\bhubspot\b', r'\bsalesforce\b', r'\brevops\b',
    r'\bpaid\s*media\b', r'\bgoogle\s*ads\b', r'\bmeta\s*ads\b', r'\bdesign\s*studio\b',
    r'\bbranding\b', r'\bsoftware\b', r'\brecruiting\b', r'\bstaffing\b', r'\bclient\b', r'\bcase\s*study\b'
]
POSITIVE_PATTERN = re.compile(r'(' + '|'.join(POSITIVE_KEYWORDS) + r')', re.IGNORECASE)

# 120+ Deep Boutique B2B Agency & Specialized Service Founder Micro-Niches
TARGET_NICHES = [
    # --- 1. SEO, CONTENT & ORGANIC GROWTH AGENCIES ---
    ("b2b seo agency founder", "B2B SEO Agency"),
    ("saas seo content marketing agency", "SaaS SEO & Content Agency"),
    ("ecommerce seo agency shopify", "E-commerce SEO Agency"),
    ("local seo agency multi location", "Local & Multi-Location SEO Agency"),
    ("programmatic seo agency founder", "Technical SEO Agency"),
    ("digital pr link building agency", "Digital PR & Link Building Agency"),
    ("answer engine optimization aeo geo agency", "AI Search & SEO Agency"),
    ("law firm seo marketing agency", "Legal Marketing Agency"),
    ("medical practice dental seo agency", "Healthcare Marketing Agency"),
    ("home services hvac roofing seo agency", "Home Services Marketing Agency"),
    ("b2b content marketing agency founder", "B2B Content Agency"),
    ("founder led linkedin ghostwriting agency", "Executive Branding Agency"),
    ("b2b newsletter media agency", "B2B Media & Newsletter Agency"),

    # --- 2. E-COMMERCE, CRO, RETENTION & PAID MEDIA AGENCIES ---
    ("shopify cro conversion rate agency", "Shopify CRO Agency"),
    ("ecommerce landing page cro agency", "Conversion Optimization Agency"),
    ("advertorial listicle funnel agency dtc", "Direct-Response Funnel Agency"),
    ("shopify plus development agency founder", "Shopify Plus Dev Agency"),
    ("shopify migration headless ecommerce agency", "E-commerce Engineering Agency"),
    ("dtc email marketing klaviyo agency", "Klaviyo Retention Agency"),
    ("ecommerce sms retention marketing agency", "DTC Retention Agency"),
    ("subscription retention churn agency dtc", "Ecommerce LTV & Retention Agency"),
    ("paid social meta ads agency dtc", "Paid Social & Meta Ads Agency"),
    ("ugc performance creative ad agency", "Performance Creative Agency"),
    ("tiktok shop affiliate agency dtc", "TikTok Shop & Social Agency"),
    ("google ads ppc agency founder", "Google Ads & PPC Agency"),
    ("ecommerce google shopping pmax agency", "Google Shopping PPC Agency"),
    ("b2b paid media linkedin ads agency", "B2B Paid Media Agency"),
    ("saas demand generation paid media agency", "B2B Demand Gen Agency"),
    ("youtube ads performance marketing agency", "YouTube Ads Agency"),
    ("connected tv ctv programmatic ad agency", "Programmatic & Media Buying Agency"),
    ("amazon brand management ppc agency", "Amazon Full-Service Agency"),
    ("amazon dsp vendor central agency", "Amazon Enterprise Agency"),
    ("walmart marketplace omnichannel agency", "Omnichannel Marketplace Agency"),

    # --- 3. WEBFLOW, FRAMER, UI/UX & BRAND DESIGN STUDIOS ---
    ("webflow design agency founder", "Webflow Design Agency"),
    ("enterprise webflow partner studio", "Enterprise Webflow Studio"),
    ("framer web design studio founder", "Framer & Web Design Studio"),
    ("b2b saas website redesign agency", "B2B Website Design Studio"),
    ("ui ux product design agency founder", "UI/UX Product Design Studio"),
    ("design systems figma product studio", "Product Design Consultancy"),
    ("b2b brand identity design studio", "Brand Identity & Strategy Studio"),
    ("rebranding strategy agency founder", "Brand Transformation Agency"),
    ("cpg packaging brand design studio", "CPG & Retail Brand Studio"),
    ("pitch deck investor presentation agency", "Strategic Presentation Studio"),
    ("3d motion design product studio", "Motion & Visual Design Studio"),

    # --- 4. REVOPS, CRM, ERP & SYSTEMS IMPLEMENTATION FIRMS ---
    ("hubspot partner agency revops", "HubSpot Elite/Partner Agency"),
    ("hubspot enterprise onboarding agency", "HubSpot Consulting Firm"),
    ("salesforce consulting partner firm", "Salesforce Implementation Partner"),
    ("salesforce cpq revenue cloud consultant", "Enterprise CRM Consultancy"),
    ("revenue operations revops agency b2b", "B2B RevOps Consultancy"),
    ("gtm engineering inbound revops agency", "GTM & RevOps Agency"),
    ("netsuite erp implementation partner", "NetSuite ERP Consultancy"),
    ("odoo erp implementation partner", "Odoo ERP Consulting Firm"),
    ("microsoft dynamics 365 partner firm", "Enterprise ERP Partner"),
    ("sap business one implementation partner", "ERP Systems Consultancy"),
    ("monday clickup Asana implementation partner", "Work OS Implementation Agency"),
    ("airtable smartsuite operations agency", "No-Code Operations Consultancy"),
    ("servicetitan housecall pro implementation", "Field Service Systems Consultancy"),

    # --- 5. CUSTOM SOFTWARE, DATA, AI & CYBERSECURITY FIRMS ---
    ("custom software development agency founder", "Custom Software Dev Shop"),
    ("mvp product development studio startup", "Product Engineering Studio"),
    ("react native flutter mobile app agency", "Mobile App Development Studio"),
    ("enterprise ai implementation consulting firm", "Enterprise AI Consultancy"),
    ("rag llm custom ai development agency", "AI Engineering Firm"),
    ("data engineering snowflake databricks agency", "Data Engineering Consultancy"),
    ("powerbi tableau business intelligence agency", "BI & Analytics Consultancy"),
    ("google analytics ga4 tag manager agency", "Marketing Analytics Consultancy"),
    ("managed service provider msp founder", "Managed IT Services (MSP)"),
    ("co managed it services cybersecurity firm", "Enterprise IT & Security Firm"),
    ("soc2 iso27001 compliance advisory firm", "Cybersecurity & Compliance Firm"),
    ("cmmc dod cybersecurity compliance consultant", "Defense & Cybersecurity Advisory"),
    ("aws azure cloud migration consulting partner", "Cloud Infrastructure Consultancy"),
    ("finops cloud cost optimization consultant", "Cloud FinOps Consultancy"),

    # --- 6. RECRUITING, PR, MEDIA & SPECIALIZED B2B FIRMS ---
    ("executive search recruiting firm founder", "Executive Search Firm"),
    ("retained c-suite executive search firm", "Retained Executive Search"),
    ("saas sales recruiting firm headhunter", "GTM & Sales Recruiting Firm"),
    ("technical engineering staffing agency", "Technical Staffing Firm"),
    ("healthcare physician nurse staffing agency", "Healthcare Recruiting Firm"),
    ("accounting finance executive recruiting", "Finance & Accounting Search Firm"),
    ("private equity portfolio recruiting firm", "PE Talent Advisory Firm"),
    ("b2b public relations pr agency founder", "B2B PR & Communications Firm"),
    ("fintech b2b tech pr agency", "Tech Media Relations Agency"),
    ("crisis communications public affairs firm", "Strategic Communications Firm"),
    ("b2b podcast production agency founder", "B2B Podcast & Media Agency"),
    ("corporate video production agency b2b", "B2B Video Production Studio"),
    ("employer branding recruitment marketing agency", "Employer Branding Agency"),
    ("commercial insurance brokerage founder", "Commercial Insurance Brokerage"),
    ("captive insurance risk management advisor", "Corporate Risk & Insurance Firm"),
    ("employee benefits self funded health broker", "Corporate Benefits Consultancy"),
    ("commercial real estate tenant rep firm", "Commercial Tenant Rep Firm"),
    ("3pl ecommerce fulfillment warehouse founder", "3PL & Logistics Provider"),
    ("freight brokerage supply chain firm", "Logistics & Freight Brokerage"),
    ("govcon federal proposal consulting firm", "GovCon Proposal Consultancy"),
    ("r&d tax credit cost seg consulting firm", "Specialized Tax Credit Firm")
]

ANGLES = [
    "", "case study", "client breakdown", "mistakes to avoid",
    "how we helped", "complete breakdown", "audit", "strategy",
    "behind the scenes", "lessons learned", "2026", "framework",
    "teardown", "step by step", "how it works"
]

FIT_NOTE_TEMPLATE = (
    "Verified {category} ({subs}) posting founder-led case studies & breakdowns ({length}); "
    "High B2B retainer LTV ($3k-$15k/mo). {funnel}"
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Niche #4: Boutique B2B Agency & Service Founders Scraper (20K+ Queries)")
    parser.add_argument('--target', type=int, default=15000)
    parser.add_argument('--min-subs', type=int, default=100)
    parser.add_argument('--max-subs', type=int, default=5000)
    parser.add_argument('--workers', type=int, default=12)
    parser.add_argument('--delay', type=float, default=0.15)
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT_CSV)
    args = parser.parse_args()

    run_turbo_harvester(
        script_title="NICHE #4: BOUTIQUE B2B AGENCY & SERVICE FOUNDERS (ULTRA-SCALE)",
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
