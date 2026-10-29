#!/usr/bin/env python3
"""
Kinetic Studio — Niche #2: Cash-Pay Doctors, Functional Medicine & Clinics (20,000+ Query Ultra-Scale Edition)
==============================================================================================================
Dedicated Output CSV: /Users/khangadget/Documents/medical_cash_clinics_15k_new.csv
"""

import os
import re
import time
import argparse
from lead_engine_core import run_turbo_harvester, DOCUMENTS_DIR

DEFAULT_OUTPUT_CSV = os.path.join(DOCUMENTS_DIR, 'medical_cash_clinics_15k_new.csv')
LOG_FILE = os.path.join(DOCUMENTS_DIR, 'scrape_medical_cash_clinics.log')


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
    r'\bdoctor\b', r'\bdr\.?\b', r'\bmd\b', r'\bdo\b', r'\bnd\b', r'\bdc\b', r'\bdds\b', r'\bdmd\b',
    r'\bclinic\b', r'\bmedspa\b', r'\bmedical\b', r'\bphysician\b', r'\bsurgeon\b', r'\bdentist\b',
    r'\bdental\b', r'\bchiropractor\b', r'\bchiropractic\b', r'\bphysical\s*therap\b', r'\bpt\b',
    r'\bfunctional\s*medicine\b', r'\bintegrative\b', r'\bhormone\b', r'\blongevity\b',
    r'\bdermatolog\b', r'\baesthetic\b', r'\bpatient\b', r'\bpatients\b', r'\bpractice\b'
]
POSITIVE_PATTERN = re.compile(r'(' + '|'.join(POSITIVE_KEYWORDS) + r')', re.IGNORECASE)

# 145+ Deep Medical, Dental, Aesthetic & Cash-Pay Clinic Micro-Niches
TARGET_NICHES = [
    # --- 1. FUNCTIONAL, INTEGRATIVE & LONGEVITY MEDICINE DOCTORS ---
    ("functional medicine doctor gut health", "Functional Medicine Doctor"),
    ("sibo leaky gut functional medicine doctor", "Functional GI & Gut Clinic"),
    ("microbiome stool test functional doctor", "Functional Medicine Practice"),
    ("integrative medicine physician root cause", "Integrative Medicine Physician"),
    ("naturopathic doctor hormone balance", "Naturopathic Medical Clinic"),
    ("longevity medicine physician peptides", "Longevity & Anti-Aging Doctor"),
    ("peter attia style medicine 3.0 concierge doctor", "Longevity & Preventive MD"),
    ("dexa scan vo2 max longevity clinic", "Performance & Longevity Clinic"),
    ("concierge medicine physician practice", "Concierge Medical Practice"),
    ("direct primary care doctor membership", "Direct Primary Care Clinic"),
    ("executive physical health clinic doctor", "Executive Health Clinic"),
    ("trt testosterone replacement clinic doctor", "HRT & Men's Health Clinic"),
    ("enclomiphene hcg trt doctor clinic", "Men's Hormone Optimization Clinic"),
    ("bioidentical hormone replacement doctor menopause", "Women's Hormone & HRT Clinic"),
    ("perimenopause hormone pellet therapy doctor", "Women's Hormone Clinic"),
    ("pcos endometriosis integrative doctor", "Women's Functional Health Clinic"),
    ("thyroid hashimotos functional medicine doctor", "Thyroid & Autoimmune Clinic"),
    ("hypothyroidism reverse t3 functional doctor", "Thyroid Specialty Clinic"),
    ("autoimmune root cause functional doctor", "Autoimmune Functional Clinic"),
    ("mold mycotoxin illness functional doctor", "Environmental Medicine Clinic"),
    ("chronic lyme coinfections integrative doctor", "Complex Chronic Illness Clinic"),
    ("mast cell mcas pots functional doctor", "Specialty Integrative Clinic"),
    ("heavy metal detox chelation doctor", "Integrative Detox & Wellness Clinic"),
    ("metabolic health insulin resistance doctor", "Metabolic Health Physician"),
    ("medical weight loss glp1 semaglutide clinic", "Medical Weight Loss Clinic"),
    ("peptide therapy bpc 157 longevity doctor", "Peptide & Regenerative Clinic"),
    ("nad+ iv vitamin therapy longevity clinic", "IV Therapy & Longevity Lounge"),
    ("hyperbaric oxygen therapy hbot clinic doctor", "Hyperbaric & Recovery Clinic"),
    ("red light ozone therapy integrative clinic", "Biohacking & Integrative Clinic"),
    ("regenerative medicine stem cell exosome doctor", "Regenerative Medicine Clinic"),
    ("prp prolotherapy orthopedic sports doctor", "Regenerative Orthopedics Clinic"),
    ("knee shoulder osteoarthritis non surgical doctor", "Joint Preservation Clinic"),
    ("functional neurology concussion brain doctor", "Functional Neurology Clinic"),
    ("adhd brain mapping neurofeedback clinic doctor", "Neurofeedback & Brain Clinic"),

    # --- 2. COSMETIC, IMPLANT & BIOLOGICAL DENTISTS ---
    ("cosmetic dentist porcelain veneers smile", "Cosmetic Dental Practice"),
    ("no prep minimal prep veneers dentist", "Luxury Cosmetic Dentist"),
    ("digital smile design makeover dentist", "Smile Makeover Dental Studio"),
    ("all on 4 dental implants surgeon dentist", "Full-Arch Implant Dentist"),
    ("zirconia full arch dental implants clinic", "Dental Implant Center"),
    ("zygomatic dental implants oral surgeon", "Oral & Maxillofacial Surgery"),
    ("full mouth reconstruction prosthodontist", "Prosthodontic & Implant Clinic"),
    ("biological holistic dentist safe mercury removal", "Biological & Holistic Dentist"),
    ("smart certified biological dentist cavitation", "Holistic Dental Practice"),
    ("ceramic zirconia dental implants holistic dentist", "Ceramic Implant Dentist"),
    ("ozone therapyprf holistic dentist", "Integrative Dental Studio"),
    ("airway dentist sleep apnea oral appliance", "Airway & Sleep Dentistry"),
    ("vivos palate expander airway dentist", "Airway & Craniofacial Dentist"),
    ("myofunctional therapy tongue tie dentist", "Pediatric & Airway Dentist"),
    ("tmj disorder jaw pain neuromuscular dentist", "TMJ & Facial Pain Clinic"),
    ("invisalign diamond provider orthodontist", "Orthodontic Practice"),
    ("adult braces clear aligner orthodontist", "Cosmetic Orthodontics Clinic"),
    ("marpe mse airway orthodontist", "Airway Orthodontist"),
    ("periodontist pinhole gum rejuvenation", "Periodontal & Implant Practice"),
    ("laser gum treatment lanap periodontist", "Laser Periodontal Clinic"),
    ("sedation dentistry dental anxiety clinic", "Sedation & Cosmetic Dentistry"),

    # --- 3. MEDSPAS, PLASTIC SURGERY, DERMATOLOGY & HAIR RESTORATION ---
    ("medspa owner aesthetic nurse injector", "Medical Spa & Aesthetics"),
    ("facial balancing dermal filler injector", "Facial Aesthetics MedSpa"),
    ("sculptra biostimulator aesthetic clinic", "Regenerative MedSpa"),
    ("prf ez gel under eye aesthetic injector", "Natural Aesthetics Clinic"),
    ("morpheus8 rf microneedling medspa", "Laser & Skin MedSpa"),
    ("co2 laser resurfacing dermatologist surgeon", "Laser Dermatology Clinic"),
    ("bbl moxi halo laser skin clinic", "Aesthetic Laser Center"),
    ("melasma hyperpigmentation dermatologist clinic", "Cosmetic Dermatology Practice"),
    ("acne scar subcision laser dermatologist", "Acne & Scar Dermatology Clinic"),
    ("facial plastic surgeon deep plane facelift", "Facial Plastic Surgery Practice"),
    ("preservation rhinoplasty facial plastic surgeon", "Rhinoplasty Surgery Clinic"),
    ("upper lower blepharoplasty eyelid surgeon", "Oculoplastic & Facial Surgery"),
    (" endoscopic brow lift lip lift surgeon", "Facial Cosmetic Surgeon"),
    ("mommy makeover breast augmentation plastic surgeon", "Plastic & Reconstructive Surgery"),
    ("hd liposuction body contouring surgeon", "Body Contouring Surgery Center"),
    ("hair transplant surgeon fue dhi restoration", "Hair Restoration Surgery Clinic"),
    ("female hair loss trichologist medical clinic", "Hair Restoration & Trichology"),
    ("prp exosome hair restoration doctor", "Non-Surgical Hair Clinic"),
    ("vein clinic sclerotherapy vascular doctor", "Vein & Vascular Aesthetics Clinic"),

    # --- 4. CHIROPRACTIC, CASH-PAY PT & SPECIALTY CASH CLINICS ---
    ("upper cervical chiropractor nucca blair", "Upper Cervical Chiropractic"),
    ("atlas orthogonal craniocervical chiropractor", "Specialty Upper Cervical Clinic"),
    ("corrective chiropractic biophysics cbp", "Posture & Spine Correction Clinic"),
    ("gonstead chiropractor disc herniation", "Gonstead Chiropractic Clinic"),
    ("non surgical spinal decompression clinic", "Spinal Decompression Center"),
    ("scoliosis bracing schroth method clinic", "Scoliosis Specialty Clinic"),
    ("peripheral neuropathy pain relief clinic", "Neuropathy Treatment Center"),
    ("shockwave therapy softwave chiropractic pt", "Regenerative Rehab Clinic"),
    ("cash based physical therapy clinic owner", "Cash-Pay Physical Therapy"),
    ("crossfit powerlifting physical therapist", "Barbell & Strength PT Clinic"),
    ("acl return to sport physical therapist", "Sports Rehab & Performance PT"),
    ("marathon runner gait physical therapist", "Running & Endurance PT Clinic"),
    ("golf tpi physical therapist swing pain", "Golf Performance & Rehab Clinic"),
    ("baseball pitcher overhead athlete pt", "Athletic Performance PT"),
    ("pelvic floor physical therapist postpartum", "Pelvic Health PT Practice"),
    ("diastasis recti prolapse pelvic pt", "Women's Pelvic Rehab Clinic"),
    ("tmj headache physical therapist dry needling", "Craniofacial & Manual PT"),
    ("vestibular vertigo concussion physical therapist", "Vestibular & Neuro Rehab"),
    ("direct care podiatrist foot ankle surgeon", "Concierge Podiatry Clinic"),
    ("minimally invasive bunion surgery podiatrist", "Specialty Foot & Ankle Surgery"),
    ("custom orthotics sports podiatrist", "Sports Podiatry Practice"),
    ("lasik smile evo icl refractive surgeon", "Refractive & LASIK Eye Center"),
    ("ipl intense pulsed light dry eye optometrist", "Specialty Dry Eye Clinic"),
    ("myopia control orthok optometrist clinic", "Vision & Myopia Specialty Clinic"),
    ("tinnitus retraining audiologist hearing clinic", "Audiology & Tinnitus Center"),
    ("fertility ivf reproductive endocrinologist", "Fertility & IVF Center"),
    ("egg freezing fertility clinic doctor", "Reproductive Medicine Practice"),
    ("integrative holistic psychiatrist mental health", "Integrative Psychiatry Practice"),
    ("tms ketamine therapy depression clinic", "Interventional Psychiatry Clinic"),
    ("mens ed acoustic wave urology clinic", "Men's Vitality & Urology Clinic")
]

ANGLES = [
    "", "what you need to know", "mistakes to avoid", "patient case study",
    "before and after breakdown", "honest doctor review", "cost and recovery",
    "root cause explained", "treatment options", "questions to ask", "my protocol",
    "explained", "pros and cons", "2026 update", "step by step"
]

FIT_NOTE_TEMPLATE = (
    "Verified {category} ({subs}) posting talking-head patient education ({length}); "
    "High-ticket cash-pay patient LTV ($3k-$25k+). {funnel}"
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Niche #2: Cash-Pay Doctors, Functional Medicine & Clinics Scraper (20K+ Queries)")
    parser.add_argument('--target', type=int, default=15000)
    parser.add_argument('--min-subs', type=int, default=100)
    parser.add_argument('--max-subs', type=int, default=5000)
    parser.add_argument('--workers', type=int, default=12)
    parser.add_argument('--delay', type=float, default=0.15)
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT_CSV)
    args = parser.parse_args()

    run_turbo_harvester(
        script_title="NICHE #2: CASH-PAY DOCTORS, FUNCTIONAL MEDICINE & AESTHETIC CLINICS (ULTRA-SCALE)",
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
