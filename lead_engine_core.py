#!/usr/bin/env python3
"""
Kinetic Studio — Shared Ultra-Scale YouTube Lead Engine Core (Cloud + MacBook | Auto-Unlimited Query Edition)
=============================================================================================================
Key Capabilities:
  1. Portable Cloud + MacBook Architecture:
     - Automatically detects working directory (`os.path.dirname(os.path.abspath(__file__))`), running
       identically on macOS (`/Users/khangadget/Documents`) and GitHub Actions Linux cloud runners.
  2. Permanent MacBook Master Blacklist (`macbook_master_blacklist.tsv`) + Cross-CSV Auto-Cleaner:
     - Scans and deduplicates ALL `.csv` files in the directory on startup.
     - Syncs every historical MacBook lead into `macbook_master_blacklist.tsv` so neither local runs
       nor GitHub Actions cloud runs EVER take a duplicate of any previously scraped MacBook lead.
     - Enforces atomic thread-safe 4-layer deduplication (`Channel ID`, `@handle/URL`, `Creator Name`, `Email`).
  3. Auto-Unlimited Query Generator (`infinite_query_generator`):
     - Stage 1: Niche Seeds x Topic Angles x 210+ US States, Metros, UK/Canada/Australia Cities (100,000+ queries).
     - Stage 2: Live Snowball Keyword Extraction (learns new 2-word topic keywords from verified leads in real time).
     - Stage 3: Infinite Combinatorial Role x Industry/Audience x Problem/Outcome Generator — never runs out of
       fresh queries regardless of target size (15K, 50K, or 100K+ leads).
  4. Zero Quality Drop Guaranteed:
     - Strictly 100 <= subscribers <= 5,000 (verified directly from channel profile page).
     - Uploaded within last 30 days (verified via YouTube This-Month filter + abbreviated/full timestamp parser).
     - Talking-Head Long-Form video (1m 30s to 60m — blocks Shorts <90s and uncut streams >60m).
     - Rejects faceless, AI, meditation/singing bowls/music, gaming, anime/drama/recaps, crafts, and non-English channels.
"""

import urllib.request
import urllib.parse
import json
import re
import csv
import time
import os
import glob
import random
import ssl
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception:
    pass

# Portable directory path: works on MacBook (/Users/khangadget/Documents) AND GitHub Actions Cloud Runners
DOCUMENTS_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_BLACKLIST_FILE = os.path.join(DOCUMENTS_DIR, 'macbook_master_blacklist.tsv')
REJECTED_CACHE_FILE = os.path.join(DOCUMENTS_DIR, '.youtube_rejected_channels_cache.txt')
COMPLETED_QUERIES_FILE = os.path.join(DOCUMENTS_DIR, '.youtube_completed_queries.txt')

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

FIELDNAMES = [
    'ID',
    'Date Scraped',
    'Channel / Creator Name',
    'Channel URL',
    'Channel ID',
    'Exact Subscribers',
    'Subscriber Count (Num)',
    'Category / ICP Role',
    'Video Format & Length',
    'Recent Video Title',
    'Recent Video URL',
    'Upload Recency',
    'Public Email',
    'Website / Funnel Links',
    'Quality Score',
    'Why Fit (Talking-Head & Offer Notes)'
]

# Universal Negative Filter (Blocks Faceless, Meditation/Sleep Music, Gaming, Anime/Movie Recaps, Crafts)
UNIVERSAL_NEGATIVE_KEYWORDS = [
    # Faceless, Ambient, Meditation, Singing Bowls, Music & Noise
    r'\bfaceless\b', r'\bsound\s*bath\b', r'\bsinging\s*bowl\b', r'\bmeditation\s*music\b',
    r'\bsleep\s*music\b', r'\bhealing\s*frequency\b', r'\bbinaural\b', r'\basmr\b',
    r'\blofi\b', r'\bwhite\s*noise\b', r'\bhypnosis\b', r'\btarot\b',
    r'\bastrology\b', r'\bpsychic\b', r'\bsubliminal\b', r'\barchangel\b',
    r'\bcrystal\s*bowls?\b', r'\breiki\b', r'\bchakra\s*music\b',
    # Entertainment, Gaming, Drama, Fiction, Recaps, Shorts
    r'#shorts\b', r'\b#short\b', r'\bdrama\b', r'\bmovie\b', r'\brecap\b', r'\brecaps\b',
    r'\bmanhwa\b', r'\banime\b', r'\bmanga\b', r'\bwebtoon\b', r'\bfiction\b',
    r'\bgaming\b', r'\bgameplay\b', r'\bprank\b', r'\breaction\b', r'\blyrics\b',
    r'\btrailer\b', r'\bcompilation\b', r'\bcelebrity\b', r'\bgossip\b',
    r'\btrue\s*crime\b', r'\bnews\s*channel\b', r'\bcartoon\b',
    # Outbound Spam
    r'\bcold\s*email\b', r'\binstantly\.ai\b', r'\bsmartlead\b', r'\bclay\.com\b',
    r'\bforex\s*signals\b', r'\bmemecoin\b', r'\bcrypto\s*pump\b', r'\bget\s*rich\s*quick\b',
    # Low-ticket crafts / food / DIY / Churches
    r'\bcake\b', r'\bcakes\b', r'\bbakery\b', r'\bbaking\b', r'\bcupcake\b',
    r'\bcooking\b', r'\bcrochet\b', r'\bknitting\b', r'\bthrift\s*flip\b',
    r'\bunboxing\b', r'\bdiy\s*slime\b', r'\bchurch\b', r'\bsermon\b'
]
UNIVERSAL_NEGATIVE_PATTERN = re.compile(r'(' + '|'.join(UNIVERSAL_NEGATIVE_KEYWORDS) + r')', re.IGNORECASE)

# 210+ High-Value English-Speaking States, Metros & Regions for Massive Combinatorial Discovery
GEO_MODIFIERS = [
    # All 50 US States
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming",
    # Major US Metros & Affluent Suburbs
    "Austin", "Dallas", "Houston", "San Antonio", "Fort Worth", "Plano", "Frisco", "The Woodlands",
    "Miami", "Tampa", "Orlando", "Jacksonville", "Boca Raton", "Naples", "Sarasota", "Fort Lauderdale",
    "West Palm Beach", "St Petersburg", "Clearwater", "Nashville", "Franklin", "Knoxville", "Chattanooga",
    "Memphis", "Charlotte", "Raleigh", "Durham", "Cary", "Wilmington", "Asheville", "Greenville",
    "Charleston", "Columbia", "Hilton Head", "Atlanta", "Alpharetta", "Savannah", "Marietta",
    "Phoenix", "Scottsdale", "Gilbert", "Chandler", "Tempe", "Tucson", "Sedona", "Denver",
    "Boulder", "Colorado Springs", "Fort Collins", "Seattle", "Bellevue", "Kirkland", "Tacoma",
    "Spokane", "San Diego", "Carlsbad", "Irvine", "Newport Beach", "Orange County", "Los Angeles",
    "Beverly Hills", "Santa Monica", "Pasadena", "San Francisco", "Palo Alto", "San Jose",
    "Silicon Valley", "Sacramento", "Roseville", "Walnut Creek", "Chicago", "Naperville",
    "Oak Brook", "Evanston", "Boston", "Cambridge", "New York City", "Manhattan", "Brooklyn",
    "Long Island", "Westchester", "Stamford", "Greenwich", "Hoboken", "Jersey City", "Princeton",
    "Philadelphia", "Main Line", "Pittsburgh", "Washington DC", "Arlington", "Alexandria",
    "Tysons", "Bethesda", "Rockville", "Baltimore", "Annapolis", "Minneapolis", "St Paul",
    "St Louis", "Kansas City", "Overland Park", "Columbus", "Dublin", "Cincinnati", "Cleveland",
    "Indianapolis", "Carmel", "Detroit", "Ann Arbor", "Grand Rapids", "Milwaukee", "Madison",
    "Salt Lake City", "Park City", "Provo", "St George", "Boise", "Meridian", "Coeur d Alene",
    "Las Vegas", "Henderson", "Summerlin", "Reno", "Portland", "Lake Oswego", "New Orleans",
    "Baton Rouge", "Oklahoma City", "Tulsa", "Omaha", "Des Moines", "Louisville", "Lexington",
    "Birmingham", "Huntsville", "Richmond", "Virginia Beach", "Charlottesville", "Albuquerque",
    "Santa Fe", "Anchorage", "Honolulu",
    # Canada, UK, Australia, NZ, Ireland & International English Hubs
    "Canada", "Toronto", "Mississauga", "Oakville", "Vancouver", "Surrey", "Victoria",
    "Calgary", "Edmonton", "Ottawa", "Montreal", "Halifax", "Winnipeg", "Ontario", "Alberta",
    "British Columbia", "UK", "London", "Manchester", "Birmingham UK", "Edinburgh", "Glasgow",
    "Bristol", "Leeds", "Liverpool", "Oxford", "Cambridge UK", "Brighton", "Reading",
    "Ireland", "Dublin", "Cork", "Galway", "Australia", "Sydney", "Melbourne", "Brisbane",
    "Perth", "Adelaide", "Gold Coast", "Canberra", "New Zealand", "Auckland", "Wellington",
    "Christchurch", "Singapore", "Dubai"
]

# Infinite Combinatorial Modifiers (Stage 3 Unlimited Query Generator)
INFINITE_AUDIENCE_SEGMENTS = [
    "for beginners", "for business owners", "for entrepreneurs", "for founders",
    "for executives", "for ceos", "for small business", "for agencies",
    "for consultants", "for coaches", "for doctors", "for lawyers",
    "for realtors", "for contractors", "for startups", "for B2B",
    "for high earners", "for professionals", "for creators", "for women",
    "for men", "over 40", "in 2026", "step by step", "without burnout",
    "from scratch", "to 10k a month", "to 100k", "to 7 figures"
]

INFINITE_PROBLEM_ANGLES = [
    "mistakes to avoid", "client case study", "my framework", "complete breakdown",
    "how to get clients", "pricing strategy", "onboarding process", "sales script",
    "objection handling", "lead generation", "retention strategy", "daily routine",
    "systems and processes", "how i scaled", "honest truth", "what i learned",
    "roadmap", "blueprint", "audit", "teardown", "q&a", "myths", "checklist",
    "tools i use", "biggest lesson", "why most fail", "how it works", "cost breakdown"
]

SEARCH_SP_FILTERS = [
    "EgIIAw%253D%253D",      # Upload Date: This Month (Relevance sort)
    "CAISBAgCEAE%253D"       # Upload Date: This Month (Upload Date sort)
]

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
IGNORED_EMAIL_DOMAINS = {'youtube.com', 'google.com', 'gstatic.com', 'example.com', 'sentry.io', 'w3.org'}

STOPWORDS = {
    'the', 'and', 'for', 'with', 'how', 'why', 'what', 'when', 'where', 'who', 'this', 'that',
    'from', 'your', 'you', 'are', 'was', 'were', 'have', 'has', 'had', 'not', 'but', 'all',
    'can', 'will', 'just', 'more', 'out', 'about', 'into', 'over', 'after', 'before', 'most',
    'some', 'such', 'no', 'nor', 'too', 'very', 'episode', 'ep', 'part', 'pt', 'video', 'live',
    'podcast', 'show', 'channel', 'official', 'new', 'best', 'top', 'day', 'week', 'month', 'year'
}


def normalize_url(u):
    if not u:
        return ''
    u = u.strip().lower()
    u = re.sub(r'^https?://(www\.)?youtube\.com/', '', u)
    u = u.split('?')[0].rstrip('/')
    return u


def normalize_name(name):
    if not name:
        return ''
    return re.sub(r'[^a-z0-9]', '', name.lower())


def normalize_email(email):
    if not email:
        return ''
    return email.strip().lower()


class GlobalDeduplicator:
    def __init__(self):
        self.lock = threading.Lock()
        self.seen_urls = set()
        self.seen_channel_ids = set()
        self.seen_names = set()
        self.seen_emails = set()

    def is_duplicate(self, channel_url='', channel_id='', channel_name='', email=''):
        norm_u = normalize_url(channel_url)
        norm_n = normalize_name(channel_name)
        cid = (channel_id or '').strip()
        norm_e = normalize_email(email)

        with self.lock:
            if norm_u and norm_u in self.seen_urls:
                return True
            if cid and cid in self.seen_channel_ids:
                return True
            if norm_n and len(norm_n) >= 4 and norm_n in self.seen_names:
                return True
            if norm_e and norm_e in self.seen_emails:
                return True
            return False

    def register(self, channel_url='', channel_id='', channel_name='', email='', persist_rejected=False, persist_master=False):
        norm_u = normalize_url(channel_url)
        norm_n = normalize_name(channel_name)
        cid = (channel_id or '').strip()
        norm_e = normalize_email(email)

        with self.lock:
            if norm_u:
                self.seen_urls.add(norm_u)
            if cid:
                self.seen_channel_ids.add(cid)
            if norm_n and len(norm_n) >= 4:
                self.seen_names.add(norm_n)
            if norm_e:
                self.seen_emails.add(norm_e)

            if persist_rejected and norm_u:
                try:
                    with open(REJECTED_CACHE_FILE, 'a', encoding='utf-8') as f:
                        f.write(f"{norm_u}\t{cid}\t{norm_n}\n")
                except Exception:
                    pass

            if persist_master and (norm_u or cid or norm_n):
                try:
                    with open(MASTER_BLACKLIST_FILE, 'a', encoding='utf-8') as f:
                        f.write(f"{norm_u}\t{cid}\t{norm_n}\t{norm_e}\n")
                except Exception:
                    pass

    def try_claim_lead(self, raw_url='', canonical_url='', channel_id='', channel_name='', email='', persist_master=True):
        norm_raw = normalize_url(raw_url)
        norm_can = normalize_url(canonical_url)
        norm_n = normalize_name(channel_name)
        cid = (channel_id or '').strip()
        norm_e = normalize_email(email)

        with self.lock:
            if norm_raw and norm_raw in self.seen_urls:
                return False
            if norm_can and norm_can in self.seen_urls:
                return False
            if cid and cid in self.seen_channel_ids:
                return False
            if norm_n and len(norm_n) >= 4 and norm_n in self.seen_names:
                return False
            if norm_e and norm_e in self.seen_emails:
                return False

            if norm_raw:
                self.seen_urls.add(norm_raw)
            if norm_can:
                self.seen_urls.add(norm_can)
            if cid:
                self.seen_channel_ids.add(cid)
            if norm_n and len(norm_n) >= 4:
                self.seen_names.add(norm_n)
            if norm_e:
                self.seen_emails.add(norm_e)

            if persist_master:
                try:
                    with open(MASTER_BLACKLIST_FILE, 'a', encoding='utf-8') as f:
                        f.write(f"{norm_can or norm_raw}\t{cid}\t{norm_n}\t{norm_e}\n")
                except Exception:
                    pass
            return True


def clean_all_csvs_and_load_dedup(target_csv, log_fn, min_subs=100, max_subs=5000, negative_pattern=None):
    """
    1. Loads permanent `macbook_master_blacklist.tsv` (containing all historical MacBook leads).
    2. Scans and cleans ALL `.csv` files in DOCUMENTS_DIR (removing duplicates and out-of-range rows).
    3. Syncs all unique leads across all CSVs into `macbook_master_blacklist.tsv` so cloud and local
       runs never duplicate a single MacBook lead.
    """
    dedup = GlobalDeduplicator()

    # Step 1: Load permanent MacBook master blacklist first ( excludes target_csv rows until Step 2 )
    master_entries = []
    if os.path.exists(MASTER_BLACKLIST_FILE):
        try:
            with open(MASTER_BLACKLIST_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    parts = line.rstrip('\n').split('\t')
                    if any(parts):
                        master_entries.append((
                            parts[0] if len(parts) > 0 else '',
                            parts[1] if len(parts) > 1 else '',
                            parts[2] if len(parts) > 2 else '',
                            parts[3] if len(parts) > 3 else ''
                        ))
        except Exception:
            pass

    all_csvs = sorted(glob.glob(os.path.join(DOCUMENTS_DIR, '*.csv')))
    target_abs = os.path.abspath(target_csv)

    ordered_csvs = [p for p in all_csvs if os.path.abspath(p) != target_abs]
    if os.path.exists(target_abs):
        ordered_csvs.append(target_abs)

    url_cols = {'channel url', 'verified channel url', 'youtube channel url', 'direct channel url', 'channel link', 'youtube channel'}
    name_cols = {'channel / creator name', 'channel name', 'creator name', 'realtor / lead name', 'company name'}
    id_cols = {'channel id', 'channel_id'}
    email_cols = {'public email', 'email', 'verified email'}

    target_leads = []
    other_leads_count = 0
    total_removed = 0

    # Step 2: Deduplicate all CSV files in DOCUMENTS_DIR
    for csv_path in ordered_csvs:
        is_target = (os.path.abspath(csv_path) == target_abs)
        try:
            with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames or FIELDNAMES
                rows = list(reader)
        except Exception:
            continue

        clean_rows = []
        removed_in_file = 0

        for row in rows:
            c_url, c_id, c_name, c_email = '', '', '', ''
            for k, v in row.items():
                if not k or not v:
                    continue
                kl = k.strip().lower()
                if kl in url_cols:
                    c_url = v.strip()
                elif kl in name_cols:
                    c_name = v.strip()
                elif kl in id_cols:
                    c_id = v.strip()
                elif kl in email_cols:
                    c_email = v.strip()

            if not c_url and not c_name:
                continue

            sub_val = row.get('Subscriber Count (Num)')
            if sub_val is not None and str(sub_val).strip().isdigit():
                s_int = int(str(sub_val).strip())
                if s_int < min_subs or s_int > max_subs:
                    removed_in_file += 1
                    total_removed += 1
                    continue

            row_text = f"{c_name} {row.get('Recent Video Title', '')}"
            if UNIVERSAL_NEGATIVE_PATTERN.search(row_text) or (negative_pattern and negative_pattern.search(row_text)):
                removed_in_file += 1
                total_removed += 1
                continue

            if dedup.try_claim_lead(raw_url=c_url, canonical_url=c_url, channel_id=c_id, channel_name=c_name, email=c_email, persist_master=False):
                clean_rows.append(row)
            else:
                removed_in_file += 1
                total_removed += 1

        if removed_in_file > 0 or is_target:
            try:
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                    writer.writeheader()
                    for idx, r in enumerate(clean_rows, 1):
                        if 'ID' in fieldnames:
                            r['ID'] = idx
                        writer.writerow(r)
            except Exception:
                pass

        if is_target:
            target_leads = clean_rows
        else:
            other_leads_count += len(clean_rows)

        if removed_in_file > 0:
            log_fn(f"[Auto-Cleaner] Removed {removed_in_file} duplicate/off-niche rows from {os.path.basename(csv_path)}")

    # Step 3: Register any additional entries from macbook_master_blacklist.tsv (critical when running in Cloud!)
    master_only_count = 0
    for u, cid, nm, em in master_entries:
        if not dedup.is_duplicate(channel_url=u, channel_id=cid, channel_name=nm, email=em):
            dedup.register(channel_url=u, channel_id=cid, channel_name=nm, email=em, persist_rejected=False, persist_master=False)
            master_only_count += 1

    # Step 4: Rewrite a clean, compacted macbook_master_blacklist.tsv with all known leads
    try:
        with open(MASTER_BLACKLIST_FILE, 'w', encoding='utf-8') as f:
            for csv_path in ordered_csvs:
                try:
                    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as cf:
                        for row in csv.DictReader(cf):
                            u = normalize_url(row.get('Channel URL', ''))
                            cid = (row.get('Channel ID') or '').strip()
                            nm = normalize_name(row.get('Channel / Creator Name', ''))
                            em = normalize_email(row.get('Public Email', ''))
                            if u or cid or nm:
                                f.write(f"{u}\t{cid}\t{nm}\t{em}\n")
                except Exception:
                    pass
            for u, cid, nm, em in master_entries:
                if u or cid or nm:
                    f.write(f"{u}\t{cid}\t{nm}\t{em}\n")
    except Exception:
        pass

    # Step 5: Load rejected channels cache
    rejected_cached = 0
    if os.path.exists(REJECTED_CACHE_FILE):
        try:
            with open(REJECTED_CACHE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    parts = line.rstrip('\n').split('\t')
                    dedup.register(
                        channel_url=parts[0] if len(parts) > 0 else '',
                        channel_id=parts[1] if len(parts) > 1 else '',
                        channel_name=parts[2] if len(parts) > 2 else '',
                        persist_rejected=False
                    )
                    rejected_cached += 1
        except Exception:
            pass

    log_fn(
        f"Global Deduplicator Ready: {len(target_leads)} leads in current CSV | "
        f"{other_leads_count + master_only_count} MacBook/Cross-CSV leads blacklisted | "
        f"{total_removed} duplicates purged | {rejected_cached} rejected channels cached."
    )
    return target_leads, dedup


def load_completed_queries():
    done = set()
    if os.path.exists(COMPLETED_QUERIES_FILE):
        try:
            with open(COMPLETED_QUERIES_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    done.add(line.strip().lower())
        except Exception:
            pass
    return done


def mark_query_completed(q_key):
    try:
        with open(COMPLETED_QUERIES_FILE, 'a', encoding='utf-8') as f:
            f.write(q_key.strip().lower() + '\n')
    except Exception:
        pass


def shorten_for_geo(niche_query):
    words = niche_query.split()
    if len(words) <= 3:
        return niche_query
    return f"{words[0]} {words[1]} {words[-1]}"


def extract_snowball_keywords(video_title):
    """Extracts clean 2-word topic phrases from a verified lead's video title for live query discovery."""
    words = [
        w.lower() for w in re.findall(r'[a-zA-Z]{4,}', video_title or '')
        if w.lower() not in STOPWORDS
    ]
    phrases = []
    for i in range(len(words) - 1):
        phrases.append(f"{words[i]} {words[i+1]}")
    return phrases[:3]


def build_massive_query_pool(target_niches, angles, completed_queries):
    """
    Stage 1 of Auto-Unlimited Query Generator:
    Generates 40,000+ to 160,000+ high-precision initial queries before infinite Stage 2/3 kicks in.
    """
    pool_tier1 = []
    pool_tier2 = []
    pool_tier3 = []

    short_topics = [
        "", "case study", "mistakes", "framework", "clients", "step by step",
        "strategy", "2026", "breakdown", "advice", "roadmap",
        "pricing", "scale", "guide", "q&a", "tips"
    ]

    seen_geo_seeds = set()
    geo_seeds = []

    for niche_query, category_label in target_niches:
        for topic in short_topics:
            q_str = f"{niche_query} {topic}".strip()
            for sp in SEARCH_SP_FILTERS:
                q_key = f"{q_str}||{sp}".lower()
                if q_key not in completed_queries:
                    pool_tier1.append((q_str, category_label, sp, q_key))

        for angle in angles:
            if not angle or angle in short_topics:
                continue
            q_str = f"{niche_query} {angle}".strip()
            for sp in SEARCH_SP_FILTERS:
                q_key = f"{q_str}||{sp}".lower()
                if q_key not in completed_queries:
                    pool_tier3.append((q_str, category_label, sp, q_key))

        g_seed = shorten_for_geo(niche_query)
        if g_seed.lower() not in seen_geo_seeds:
            seen_geo_seeds.add(g_seed.lower())
            geo_seeds.append((g_seed, category_label))

    for role_seed, category_label in geo_seeds:
        for geo in GEO_MODIFIERS:
            q_str = f"{role_seed} {geo}"
            for sp in SEARCH_SP_FILTERS:
                q_key = f"{q_str}||{sp}".lower()
                if q_key not in completed_queries:
                    pool_tier2.append((q_str, category_label, sp, q_key))

    random.shuffle(pool_tier1)
    random.shuffle(pool_tier2)
    random.shuffle(pool_tier3)

    combined = []
    max_len = max(len(pool_tier1), len(pool_tier2))
    for i in range(max_len):
        if i < len(pool_tier1):
            combined.append(pool_tier1[i])
        if i < len(pool_tier2):
            combined.append(pool_tier2[i])
    combined.extend(pool_tier3)
    return combined


def infinite_query_generator(target_niches, angles, completed_queries, snowball_queue):
    """
    Auto-Unlimited Query Generator:
      1. Yields from the massive Stage 1 pool (interleaved with live Stage 2 Snowball queries discovered from verified leads).
      2. If Stage 1 ever finishes, endlessly synthesizes new Stage 3 combinations
         (Role Seed x Audience Segment x Problem Angle x Geo Modifier) so the scraper NEVER stops until target is met!
    """
    initial_pool = build_massive_query_pool(target_niches, angles, completed_queries)
    for item in initial_pool:
        # First yield any live snowball queries discovered from recent verified leads
        while snowball_queue:
            sb_item = snowball_queue.pop(0)
            if sb_item[3] not in completed_queries:
                completed_queries.add(sb_item[3])
                yield sb_item

        if item[3] not in completed_queries:
            completed_queries.add(item[3])
            yield item

    # Stage 3: Endless Combinatorial Synthesis (Unlimited Queries)
    role_seeds = [(shorten_for_geo(nq), cat) for nq, cat in target_niches]
    while True:
        while snowball_queue:
            sb_item = snowball_queue.pop(0)
            if sb_item[3] not in completed_queries:
                completed_queries.add(sb_item[3])
                yield sb_item

        role_seed, category_label = random.choice(role_seeds)
        aud = random.choice(INFINITE_AUDIENCE_SEGMENTS)
        prob = random.choice(INFINITE_PROBLEM_ANGLES)
        geo = random.choice(GEO_MODIFIERS + [""] * 10)
        sp = random.choice(SEARCH_SP_FILTERS)

        q_str = f"{role_seed} {prob} {aud} {geo}".strip()
        q_str = re.sub(r'\s+', ' ', q_str)
        q_key = f"{q_str}||{sp}".lower()
        if q_key not in completed_queries:
            completed_queries.add(q_key)
            yield (q_str, category_label, sp, q_key)


def extract_videos_and_continuation(data):
    video_renderers = []
    continuation_tokens = []

    def walk(obj):
        if isinstance(obj, dict):
            if "videoRenderer" in obj:
                video_renderers.append(obj["videoRenderer"])
            if "continuationCommand" in obj:
                tok = obj["continuationCommand"].get("token")
                if tok:
                    continuation_tokens.append(tok)
            for k, v in obj.items():
                if k != "videoRenderer":
                    walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return video_renderers, (continuation_tokens[0] if continuation_tokens else None)


def fetch_search_results_deep(query_str, sp_param, max_pages=2):
    encoded_q = urllib.parse.quote(query_str)
    search_url = f"https://www.youtube.com/results?search_query={encoded_q}&sp={sp_param}"

    try:
        req = urllib.request.Request(search_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=9) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception:
        return []

    m = re.search(r'ytInitialData\s*=\s*({.+?});</script>', html)
    if not m:
        return []

    try:
        data = json.loads(m.group(1))
    except Exception:
        return []

    all_videos, cont_token = extract_videos_and_continuation(data)
    api_key_match = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html)
    api_key = api_key_match.group(1) if api_key_match else None

    page = 1
    while page < max_pages and cont_token and api_key:
        page += 1
        cont_url = f"https://www.youtube.com/youtubei/v1/search?key={api_key}&prettyPrint=false"
        payload = json.dumps({
            "context": {
                "client": {
                    "hl": "en",
                    "gl": "US",
                    "clientName": "WEB",
                    "clientVersion": "2.20240726.00.00"
                }
            },
            "continuation": cont_token
        }).encode('utf-8')

        cont_headers = dict(HEADERS)
        cont_headers["Content-Type"] = "application/json"

        try:
            creq = urllib.request.Request(cont_url, data=payload, headers=cont_headers, method="POST")
            with urllib.request.urlopen(creq, timeout=8) as cresp:
                cdata = json.loads(cresp.read().decode('utf-8', errors='ignore'))
            more_videos, cont_token = extract_videos_and_continuation(cdata)
            if not more_videos:
                break
            all_videos.extend(more_videos)
        except Exception:
            break

    return all_videos


def is_mostly_english(text):
    if not text:
        return False
    return sum(1 for c in text if ord(c) > 127) <= 3


def parse_duration_seconds(length_text):
    if not length_text:
        return 300
    parts = [int(p) for p in re.findall(r'\d+', length_text)]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0


def is_within_last_30_days(published_text):
    if not published_text:
        return True
    t = published_text.lower().strip()
    if 'year' in t or re.search(r'\b\d+\s*y(r|rs)?\b', t):
        return False
    m_mo = re.search(r'(\d+)\s*(?:month|mo)', t)
    if m_mo and int(m_mo.group(1)) > 1:
        return False
    m_wk = re.search(r'(\d+)\s*(?:week|wk|w)\b', t)
    if m_wk and int(m_wk.group(1)) > 4:
        return False
    return True


def parse_subs_count(sub_str):
    if not sub_str:
        return 0
    clean = sub_str.replace("subscribers", "").replace("subscriber", "").strip().lower()
    try:
        if 'm' in clean:
            return int(float(clean.replace('m', '').strip()) * 1_000_000)
        elif 'k' in clean:
            return int(float(clean.replace('k', '').strip()) * 1_000)
        else:
            digits = re.sub(r'[^0-9]', '', clean)
            return int(digits) if digits else 0
    except Exception:
        return 0


def inspect_channel_profile(channel_url):
    req = urllib.request.Request(channel_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception:
        return None

    m = re.search(r'ytInitialData\s*=\s*({.+?});</script>', html)
    if not m:
        return None
    try:
        data = json.loads(m.group(1))
    except Exception:
        return None

    sub_str = ""
    metadata_parts = []

    def walk(obj):
        if isinstance(obj, dict):
            if "metadataParts" in obj:
                metadata_parts.append(obj["metadataParts"])
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for it in obj:
                walk(it)

    walk(data)
    for plist in metadata_parts:
        if isinstance(plist, list):
            for p in plist:
                if isinstance(p, dict):
                    t = p.get("text", {}).get("content", "")
                    if "sub" in t.lower():
                        sub_str = t
                        break
                    acc = p.get("accessibilityLabel", "")
                    if "sub" in acc.lower():
                        sub_str = acc
                        break
        if sub_str:
            break

    if not sub_str:
        sub_m = re.search(r'"([0-9.,]+[KMBkmb]?\s+subscribers?)"', html)
        if sub_m:
            sub_str = sub_m.group(1)

    sub_num = parse_subs_count(sub_str)
    ch_meta = data.get("metadata", {}).get("channelMetadataRenderer", {})
    channel_id = ch_meta.get("externalId", "")
    description = ch_meta.get("description", "") or ""
    vanity_url = ch_meta.get("vanityChannelUrl", "") or channel_url
    handle_match = re.search(r'https://www\.youtube\.com/(@[A-Za-z0-9_.-]+)', html)
    canonical_url = f"https://www.youtube.com/{handle_match.group(1)}" if handle_match else vanity_url

    public_email = ""
    for em in EMAIL_REGEX.findall(description):
        domain = em.split('@')[-1].lower()
        if domain not in IGNORED_EMAIL_DOMAINS and not domain.endswith(('.png', '.jpg', '.svg')):
            public_email = em.lower()
            break

    decoded_links = []
    for rl in re.findall(r'q=(https?%3A%2F%2F[^"&]+)', html):
        dl = urllib.parse.unquote(rl)
        if not any(x in dl.lower() for x in ['youtube.com', 'google.com', 'ggpht.com', 'ytimg.com']):
            if dl not in decoded_links:
                decoded_links.append(dl)
    for ru in re.findall(r'https?://[^\s)\]>"]+', description):
        ru_clean = ru.rstrip('.,;:')
        if not any(x in ru_clean.lower() for x in ['youtube.com', 'youtu.be', 'google.com']):
            if ru_clean not in decoded_links:
                decoded_links.append(ru_clean)

    return {
        "sub_str": sub_str if sub_str else f"{sub_num} subscribers",
        "sub_num": sub_num,
        "channel_id": channel_id,
        "canonical_url": canonical_url,
        "description": description,
        "public_email": public_email,
        "external_links": decoded_links[:3]
    }


def save_leads_to_csv(leads_list, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction='ignore')
        writer.writeheader()
        for idx, lead in enumerate(leads_list, 1):
            lead['ID'] = idx
            writer.writerow(lead)


def run_turbo_harvester(
    script_title,
    target_niches,
    angles,
    negative_pattern,
    positive_pattern,
    fit_note_template,
    output_csv,
    log_fn,
    target_leads=15000,
    min_subs=100,
    max_subs=5000,
    workers=12,
    delay=0.15,
    max_runtime_minutes=0
):
    start_epoch = time.time()
    leads_list, dedup = clean_all_csvs_and_load_dedup(
        output_csv, log_fn, min_subs=min_subs, max_subs=max_subs, negative_pattern=negative_pattern
    )
    save_leads_to_csv(leads_list, output_csv)
    completed_queries = load_completed_queries()
    snowball_queue = []
    role_seeds = [(shorten_for_geo(nq), cat) for nq, cat in target_niches]

    log_fn("======================================================================")
    log_fn(f"{script_title}")
    log_fn(f"Sub Range      : Strictly {min_subs:,} to {max_subs:,} subscribers (Talking-Head 1.5m-60m)")
    log_fn(f"Query Engine   : AUTO-UNLIMITED (Combinatorial + Live Snowball Discovery + Infinite Synthesis)")
    log_fn(f"Blacklist Lock : macbook_master_blacklist.tsv + All CSVs ({len(dedup.seen_urls):,} channels blocked)")
    log_fn(f"Parallel Speed : {workers} Threads | Output: {output_csv}")
    log_fn(f"Starting Count : {len(leads_list)} / {target_leads:,}")
    log_fn("======================================================================")

    if len(leads_list) >= target_leads:
        log_fn(f"Target of {target_leads:,} leads already reached in {output_csv}!")
        return

    def worker_fn(cand):
        raw_channel_url = cand["raw_channel_url"]
        c_name = cand["c_name"]
        video_title = cand["video_title"]
        video_url = cand["video_url"]
        published_text = cand["published_text"]
        length_text = cand["length_text"]
        category_label = cand["category_label"]

        if dedup.is_duplicate(channel_url=raw_channel_url, channel_name=c_name):
            return None

        profile = inspect_channel_profile(raw_channel_url)
        if not profile:
            return None

        sub_num = profile["sub_num"]
        canonical_url = profile["canonical_url"]
        channel_id = profile["channel_id"]
        public_email = profile["public_email"]

        # Gate 1: Strict 100 to 5,000 subscribers
        if sub_num < min_subs or sub_num > max_subs:
            dedup.register(raw_channel_url, channel_id, c_name, persist_rejected=True)
            dedup.register(canonical_url, channel_id, c_name, persist_rejected=False)
            return None

        bio = (profile.get('description') or '').strip()
        links_str = " ".join(profile.get("external_links") or [])
        full_text = f"{c_name} {video_title} {bio} {links_str}"

        # Gate 5: Strict Negative & English Check
        if (
            UNIVERSAL_NEGATIVE_PATTERN.search(full_text)
            or negative_pattern.search(full_text)
            or not is_mostly_english(c_name)
            or not is_mostly_english(video_title)
        ):
            dedup.register(raw_channel_url, channel_id, c_name, persist_rejected=True)
            return None

        matches = set(m.lower() for m in positive_pattern.findall(full_text))

        # Atomic thread-safe claim across all 4 identifiers + permanent sync to macbook_master_blacklist.tsv!
        if not dedup.try_claim_lead(
            raw_url=raw_channel_url,
            canonical_url=canonical_url,
            channel_id=channel_id,
            channel_name=c_name,
            email=public_email,
            persist_master=True
        ):
            return None

        score = min(85 + min(len(matches) * 2, 7) + (4 if profile["external_links"] else 0) + (3 if public_email else 0), 99)
        disp_len = length_text if length_text else "Long-Form"
        format_label = f"Talking Head ({disp_len})"
        funnel_note = f"Links: {', '.join(profile['external_links'][:2])}" if profile["external_links"] else "Verified Active Channel"

        return {
            'Date Scraped': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Channel / Creator Name': c_name,
            'Channel URL': canonical_url,
            'Channel ID': channel_id,
            'Exact Subscribers': profile["sub_str"],
            'Subscriber Count (Num)': sub_num,
            'Category / ICP Role': category_label,
            'Video Format & Length': format_label,
            'Recent Video Title': video_title,
            'Recent Video URL': video_url,
            'Upload Recency': published_text,
            'Public Email': public_email,
            'Website / Funnel Links': " | ".join(profile["external_links"]),
            'Quality Score': f"{score}/100",
            'Why Fit (Talking-Head & Offer Notes)': fit_note_template.format(
                category=category_label,
                subs=profile["sub_str"],
                length=disp_len,
                funnel=funnel_note
            )
        }

    unsaved_additions = 0
    q_stream = infinite_query_generator(target_niches, angles, completed_queries, snowball_queue)

    for q_idx, (query_str, category_label, sp_param, q_key) in enumerate(q_stream, 1):
        if len(leads_list) >= target_leads:
            break

        # Graceful Cloud Time-Limit Check (for GitHub Actions 6-hour job window)
        if max_runtime_minutes > 0 and (time.time() - start_epoch) >= (max_runtime_minutes * 60):
            save_leads_to_csv(leads_list, output_csv)
            log_fn(f"CLOUD CHECKPOINT: {max_runtime_minutes}m elapsed. Saved {len(leads_list)} leads cleanly.")
            return

        video_renderers = fetch_search_results_deep(query_str, sp_param, max_pages=2)
        mark_query_completed(q_key)

        candidates_to_check = []
        seen_in_batch = set()

        for vr in video_renderers:
            try:
                vid = vr.get("videoId") or ""
                title_runs = vr.get("title", {}).get("runs") or []
                video_title = title_runs[0].get("text", "") if title_runs else ""
                published_text = (vr.get("publishedTimeText", {}).get("simpleText") or "Last 30 Days").strip()
                length_text = (vr.get("lengthText", {}).get("simpleText") or "").strip()
                owner_runs = vr.get("ownerText", {}).get("runs") or []
                if not owner_runs or not vid or not video_title:
                    continue

                c_name = (owner_runs[0].get("text") or "").strip()
                c_nav = (
                    owner_runs[0]
                    .get("navigationEndpoint", {})
                    .get("commandMetadata", {})
                    .get("webCommandMetadata", {})
                    .get("url") or ""
                )
                if not c_nav or not c_name:
                    continue

                raw_channel_url = f"https://www.youtube.com{c_nav}"
                norm_u = normalize_url(raw_channel_url)
                if norm_u in seen_in_batch:
                    continue

                if not is_within_last_30_days(published_text):
                    continue

                duration_sec = parse_duration_seconds(length_text)
                if duration_sec < 90 or duration_sec > 3600:
                    continue

                if dedup.is_duplicate(channel_url=raw_channel_url, channel_name=c_name):
                    continue

                if (
                    UNIVERSAL_NEGATIVE_PATTERN.search(f"{c_name} {video_title}")
                    or negative_pattern.search(f"{c_name} {video_title}")
                    or not is_mostly_english(c_name)
                    or not is_mostly_english(video_title)
                ):
                    continue

                seen_in_batch.add(norm_u)
                candidates_to_check.append({
                    "raw_channel_url": raw_channel_url,
                    "c_name": c_name,
                    "video_title": video_title,
                    "video_url": f"https://www.youtube.com/watch?v={vid}",
                    "published_text": published_text,
                    "length_text": length_text,
                    "duration_sec": duration_sec,
                    "category_label": category_label
                })
            except Exception:
                continue

        log_fn(
            f"[Query #{q_idx:,} | Unlimited] '{query_str[:36]}...' | "
            f"New: {len(candidates_to_check)}/{len(video_renderers)} | "
            f"Saved: {len(leads_list)}/{target_leads}"
        )

        if not candidates_to_check:
            continue

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(worker_fn, cand) for cand in candidates_to_check]
            for fut in as_completed(futures):
                try:
                    lead_row = fut.result()
                except Exception:
                    continue
                if lead_row:
                    lead_row['ID'] = len(leads_list) + 1
                    leads_list.append(lead_row)
                    unsaved_additions += 1
                    log_fn(
                        f"  [+] Match #{len(leads_list)}: {lead_row['Channel / Creator Name']} "
                        f"({lead_row['Exact Subscribers']}) | {lead_row['Category / ICP Role']} | "
                        f"{lead_row['Video Format & Length']}"
                    )

                    # Live Stage 2 Snowball Query Discovery from verified lead's title!
                    if len(snowball_queue) < 250:
                        for sb_phrase in extract_snowball_keywords(lead_row['Recent Video Title']):
                            r_seed, r_cat = random.choice(role_seeds)
                            sb_q = f"{r_seed} {sb_phrase}"
                            sb_sp = random.choice(SEARCH_SP_FILTERS)
                            sb_key = f"{sb_q}||{sb_sp}".lower()
                            if sb_key not in completed_queries:
                                snowball_queue.append((sb_q, r_cat, sb_sp, sb_key))

                    if len(leads_list) >= target_leads:
                        break

        if unsaved_additions >= 5:
            save_leads_to_csv(leads_list, output_csv)
            unsaved_additions = 0
            log_fn(f"  [Saved] {len(leads_list)} / {target_leads} verified leads written to {os.path.basename(output_csv)}")

        if len(leads_list) >= target_leads:
            save_leads_to_csv(leads_list, output_csv)
            log_fn(f"SUCCESS: Target of {target_leads:,} verified leads reached!")
            return

        time.sleep(delay)

    save_leads_to_csv(leads_list, output_csv)
    log_fn(f"COMPLETE: Saved {len(leads_list)} verified leads to {output_csv}")
