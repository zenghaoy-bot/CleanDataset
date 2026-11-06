from faker import Faker
import random
import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

fake = Faker('en_US')
Faker.seed(42)
random.seed(42)

OUTPUT_ROOT = "simulated_leak_dataset_docx"
folders = {
    "nda": os.path.join(OUTPUT_ROOT, "nda"),
    "vendor_contract": os.path.join(OUTPUT_ROOT, "vendor_contract"),
    "email": os.path.join(OUTPUT_ROOT, "email"),
    "finance": os.path.join(OUTPUT_ROOT, "finance"),
}
for fp in folders.values():
    os.makedirs(fp, exist_ok=True)


def set_para(doc, text, bold=False, size=11, align=None, space_after=6):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(0, 0, 0)
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p


def add_title(doc, text):
    set_para(doc, text, bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)


def add_section(doc, title, body_lines):
    set_para(doc, title, bold=True, size=12, space_after=4)
    for line in body_lines:
        set_para(doc, line, size=11, space_after=2)


# ---------- Template 1: NDA ----------
def generate_nda(doc, doc_id):
    party_a, party_b = fake.company(), fake.company()
    eff_date = fake.date_between(start_date="-2y", end_date="today")
    term = random.randint(2, 5)
    juris = random.choice(["British Columbia, Canada", "Ontario, Canada", "Delaware, USA", "Washington, USA"])
    purpose = random.choice(["product integration", "supply chain negotiation",
                             "technical audit", "joint research project"])

    add_title(doc, f"NON-DISCLOSURE AGREEMENT (NDA)  NDA-{doc_id:06d}")
    set_para(doc, f"Effective Date: {eff_date}", size=11)
    set_para(doc, f"Disclosing Party: {party_a}", size=11)
    set_para(doc, f"Receiving Party: {party_b}", size=11, space_after=8)

    add_section(doc, "1. DEFINITION OF CONFIDENTIAL INFORMATION", [
        "Confidential Information includes all non-public technical specifications, pricing, vendor lists, "
        "internal roadmaps, customer data, business plans, and negotiation records disclosed in writing or verbally."
    ])
    add_section(doc, "2. OBLIGATION OF RECEIVING PARTY", [
        "Receiving Party shall hold all Confidential Information in strict confidence, shall not disclose to any "
        "third party without prior written consent, and shall use the same degree of care as it uses to protect "
        "its own confidential information."
    ])
    add_section(doc, "3. TERM", [
        f"This Agreement shall remain effective for {term} years from the Effective Date. Confidentiality "
        "obligations survive termination of this Agreement."
    ])
    add_section(doc, "4. EXCLUSIONS", [
        "Information that is publicly available, independently developed by Receiving Party, or lawfully obtained "
        "from a third party without restriction is not considered Confidential Information."
    ])
    add_section(doc, "5. REMEDIES", [
        "Parties acknowledge that breach of this NDA may cause irreparable harm, and the Disclosing Party may "
        "seek injunctive relief in addition to monetary damages."
    ])
    add_section(doc, "6. GOVERNING LAW", [
        f"This Agreement is governed by the laws of {juris}."
    ])
    set_para(doc, "", space_after=4)
    set_para(doc, f"{party_a} Representative: {fake.name()}", size=11)
    set_para(doc, f"{party_b} Representative: {fake.name()}", size=11)


# ---------- Template 2: Vendor Contract ----------
def generate_vendor_contract(doc, doc_id):
    buyer, supplier = fake.company(), fake.company()
    start = fake.date_between(start_date="-18m", end_date="+6m")
    end = fake.date_between(start_date=start, end_date="+24m")
    total = round(random.uniform(15000, 750000), 2)
    svc = random.choice([
        "managed IT hardware supply", "cloud infrastructure support service",
        "office supply and logistics service", "software license subscription",
        "network security monitoring service"])
    pay = random.choice(["Net 30", "Net 45", "50% upfront, 50% upon delivery acceptance"])

    add_title(doc, f"SUPPLIER SERVICE CONTRACT  VEND-{doc_id:06d}")
    set_para(doc, f"Date: {start}", size=11)
    set_para(doc, f"Buyer: {buyer}", size=11)
    set_para(doc, f"Supplier: {supplier}", size=11, space_after=8)

    add_section(doc, "1. SCOPE OF SERVICES", [
        f"Supplier agrees to provide {svc} as described in Schedule A attached. All deliverables must meet the "
        "agreed service level requirements."
    ])
    add_section(doc, "2. CONTRACT VALUE", [
        f"Total contract value: CAD ${total:,.2f}",
        f"Payment terms: {pay}"
    ])
    add_section(doc, "3. CONTRACT PERIOD", [
        f"Term starts: {start}", f"Term ends: {end}"
    ])
    add_section(doc, "4. SLA AND ACCEPTANCE", [
        "Supplier shall maintain service availability of minimum 99.5%. Buyer has 10 business days after "
        "delivery to submit written rejection of non-conforming goods/services."
    ])
    add_section(doc, "5. TERMINATION", [
        "Either party may terminate this agreement with 30 days written notice if the other party materially "
        "breaches the contract and fails to cure within 15 days."
    ])
    add_section(doc, "6. INDEMNIFICATION", [
        "Supplier shall indemnify Buyer against third-party claims arising from Supplier's negligence or "
        "breach of warranty."
    ])
    add_section(doc, "7. CONFIDENTIALITY", [
        "All pricing, technical details and business terms under this contract are Confidential Information."
    ])
    set_para(doc, "", space_after=4)
    set_para(doc, f"Authorized Signatory Buyer: {fake.name()}", size=11)
    set_para(doc, f"Authorized Signatory Supplier: {fake.name()}", size=11)


# ---------- Template 3: Internal Business Email ----------
def generate_email(doc, doc_id):
    sender, receiver = fake.name(), fake.name()
    s_email, r_email = fake.email(), fake.email()
    date = fake.date_time_between(start_date="-1y", end_date="now")
    subject = random.choice([
        "Re: vendor pricing negotiation update", "Confidential: quarterly cost forecast",
        "Follow-up on contract review", "Risk note for supplier onboarding",
        "Internal discussion about budget adjustment"])
    body = random.choice([
        "Please review the attached vendor draft before we send it over tomorrow. Do not forward this to external parties.",
        "We are seeing a 12% increase in supply cost from this supplier; we need to decide whether to renew the contract.",
        "This email contains preliminary financial figures, not for public distribution.",
        "The legal team raised concerns about the limitation of liability clause in the NDA.",
        "Let's schedule a quick sync to discuss the supplier's security questionnaire response."])

    set_para(doc, f"From: {sender} <{s_email}>", size=10)
    set_para(doc, f"To: {receiver} <{r_email}>", size=10)
    set_para(doc, f"Date: {date}", size=10)
    set_para(doc, f"Subject: {subject}", size=10, bold=True, space_after=8)
    set_para(doc, f"Hi {receiver.split()[0]},", size=11)
    set_para(doc, body, size=11)
    set_para(doc, "", space_after=4)
    set_para(doc, "Best regards,", size=11)
    set_para(doc, sender, size=11, bold=True)
    set_para(doc, fake.job(), size=10)


# ---------- Template 4: Financial Report ----------
def generate_finance(doc, doc_id):
    company = fake.company()
    month = fake.date_between(start_date="-24m", end_date="today")
    revenue = round(random.uniform(80000, 2200000), 2)
    cogs = round(revenue * random.uniform(0.35, 0.65), 2)
    opex = round(random.uniform(20000, 450000), 2)
    net = revenue - cogs - opex

    add_title(doc, f"MONTHLY FINANCIAL SUMMARY  FIN-{doc_id:06d}")
    set_para(doc, f"Company: {company}", size=11)
    set_para(doc, f"Report Month: {month.strftime('%B %Y')}", size=11, space_after=8)

    set_para(doc, f"Revenue: CAD ${revenue:,.2f}", size=11)
    set_para(doc, f"Cost of Goods Sold (COGS): CAD ${cogs:,.2f}", size=11)
    set_para(doc, f"Operating Expenses: CAD ${opex:,.2f}", size=11)
    set_para(doc, f"Net Profit (Pre-tax): CAD ${net:,.2f}", size=11, bold=True, space_after=8)

    add_section(doc, "Notes", [
        "This is an internal confidential financial report for management only.",
        "Figures are preliminary and subject to final audit adjustment.",
        "Do not share with vendors or external third parties without finance approval."
    ])


# ---------- Batch generation ----------
counts = {"nda": 150, "vendor_contract": 150, "email": 150, "finance": 50}
generators = {
    "nda": generate_nda,
    "vendor_contract": generate_vendor_contract,
    "email": generate_email,
    "finance": generate_finance,
}

for typ, total in counts.items():
    for i in range(total):
        doc = Document()
        generators[typ](doc, i + 1)
        doc.save(os.path.join(folders[typ], f"{typ}_{i+1:04d}.docx"))

print("All 500 simulated .docx documents generated successfully!")
print(f"Output folder: {os.path.abspath(OUTPUT_ROOT)}")
