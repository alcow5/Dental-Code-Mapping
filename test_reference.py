# Test cases reference file for CDT Code Mapper
# This file contains comprehensive test cases with expected results

TEST_CASES = [
    {
        "name": "Standard Adult Checkup + Cleaning",
        "input": "Patient came in for a routine dental checkup. We did a full oral exam and a cleaning. No radiographs needed.",
        "expected_codes": ["D0120", "D1110"],
        "expected_descriptions": [
            "Periodic oral evaluation - established patient",
            "Prophylaxis - adult"
        ]
    },
    {
        "name": "Pediatric Sealants + Fluoride",
        "input": "Applied fluoride varnish and sealants on molars for an 8-year-old patient during a preventive visit.",
        "expected_codes": ["D1206", "D1351"],
        "expected_descriptions": [
            "Topical application of fluoride varnish",
            "Sealant - per tooth"
        ]
    },
    {
        "name": "Bitewing X-rays and Composite Filling",
        "input": "Patient had decay on the lower left molar. We took two bitewing X-rays and placed a composite restoration on one surface.",
        "expected_codes": ["D0272", "D2391"],
        "expected_descriptions": [
            "Bitewings – two radiographic images",
            "Resin-based composite – one surface, posterior"
        ]
    },
    {
        "name": "Root Canal – Premolar",
        "input": "Completed root canal on upper premolar due to chronic pain. Patient was advised to return for crown placement.",
        "expected_codes": ["D3320"],
        "expected_descriptions": [
            "Endodontic therapy, bicuspid tooth (excluding final restoration)"
        ]
    },
    {
        "name": "Tooth Extraction",
        "input": "Extracted an erupted tooth with forceps under local anesthesia. Simple procedure.",
        "expected_codes": ["D7140"],
        "expected_descriptions": [
            "Extraction, erupted tooth or exposed root (elevation and/or forceps removal)"
        ]
    },
    {
        "name": "Scaling and Root Planing (SRP)",
        "input": "Patient diagnosed with periodontal disease. SRP performed on lower left quadrant affecting four teeth.",
        "expected_codes": ["D4341"],
        "expected_descriptions": [
            "Periodontal scaling and root planing – four or more teeth per quadrant"
        ]
    },
    {
        "name": "Full Denture Delivery",
        "input": "Delivered a complete upper denture to the patient after impressions were made last visit.",
        "expected_codes": ["D5110"],
        "expected_descriptions": [
            "Complete denture – maxillary"
        ]
    },
    {
        "name": "Limited Emergency Exam",
        "input": "Patient presented with severe toothache. Limited exam focused on the area of pain.",
        "expected_codes": ["D0140"],
        "expected_descriptions": [
            "Limited oral evaluation – problem focused"
        ]
    },
    {
        "name": "Panoramic Radiograph for Assessment",
        "input": "Took a panoramic X-ray to assess jaw and sinus structure prior to implant evaluation.",
        "expected_codes": ["D0330"],
        "expected_descriptions": [
            "Panoramic radiographic image"
        ]
    },
    {
        "name": "Fluoride Treatment + Hygiene Instruction",
        "input": "Applied fluoride varnish after cleaning. Reviewed brushing technique and flossing with the patient.",
        "expected_codes": ["D1206", "D1330"],
        "expected_descriptions": [
            "Topical application of fluoride varnish",
            "Oral hygiene instructions"
        ]
    },
    {
        "name": "Anterior Composite – Two Surfaces",
        "input": "Placed composite restoration on two surfaces of tooth #8. Patient chipped the incisal edge and had decay interproximally.",
        "expected_codes": ["D2331"],
        "expected_descriptions": [
            "Resin-based composite – two surfaces, anterior"
        ]
    },
    {
        "name": "Resin Crown Placement",
        "input": "Delivered an indirect resin crown on lower right second premolar after prior root canal.",
        "expected_codes": ["D2710"],
        "expected_descriptions": [
            "Crown – resin (indirect)"
        ]
    },
    {
        "name": "Incision and Drainage",
        "input": "Patient presented with facial swelling and pain. Performed extraoral incision and drainage of abscess.",
        "expected_codes": ["D7520"],
        "expected_descriptions": [
            "Incision and drainage of abscess – extraoral soft tissue"
        ]
    },
    {
        "name": "Full Mouth Debridement",
        "input": "Heavy calculus present. Full mouth debridement performed to allow better diagnostic evaluation on next visit.",
        "expected_codes": ["D4355"],
        "expected_descriptions": [
            "Full mouth debridement to enable a comprehensive periodontal evaluation and diagnosis on a subsequent visit"
        ]
    },
    {
        "name": "Stainless Steel Crown on Child",
        "input": "Placed a preformed stainless steel crown on primary molar with deep decay.",
        "expected_codes": ["D2930"],
        "expected_descriptions": [
            "Prefabricated stainless steel crown – primary tooth"
        ]
    },
    {
        "name": "Biteguard Delivery",
        "input": "Delivered a hard full-arch nightguard for bruxism. Patient has history of grinding and TMJ discomfort.",
        "expected_codes": ["D9944"],
        "expected_descriptions": [
            "Occlusal guard – hard appliance, full arch"
        ]
    },
    {
        "name": "Post and Core with Crown",
        "input": "Placed a cast post and core on tooth #19, followed by porcelain fused to metal crown.",
        "expected_codes": ["D2954", "D2750"],
        "expected_descriptions": [
            "Prefabricated post and core in addition to crown",
            "Crown – porcelain fused to high noble metal"
        ]
    },
    {
        "name": "Emergency Palliative Treatment",
        "input": "Provided palliative care for severe tooth pain, including temporary dressing and occlusal adjustment.",
        "expected_codes": ["D9110"],
        "expected_descriptions": [
            "Palliative treatment of dental pain – per visit"
        ]
    },
    # New test cases
    {
        "name": "Crown Lengthening",
        "input": "Performed crown lengthening around tooth #3 to expose more structure for crown placement.",
        "expected_codes": ["D4249"],
        "expected_descriptions": [
            "Clinical crown lengthening - hard tissue"
        ]
    },
    {
        "name": "Nitrous Oxide Sedation",
        "input": "Administered nitrous oxide to patient prior to restorative procedure.",
        "expected_codes": ["D9230"],
        "expected_descriptions": [
            "Inhalation of nitrous oxide/analgesia, anxiolysis"
        ]
    },
    {
        "name": "Interim Partial Denture",
        "input": "Delivered interim removable partial denture for anterior teeth while patient awaits implant placement.",
        "expected_codes": ["D5820"],
        "expected_descriptions": [
            "Interim partial denture (maxillary)"
        ]
    },
    {
        "name": "Flap Surgery - One to Three Teeth",
        "input": "Flap surgery performed in the upper right quadrant on three teeth to access root surfaces.",
        "expected_codes": ["D4240"],
        "expected_descriptions": [
            "Gingival flap procedure, including root planing - one to three teeth per quadrant"
        ]
    },
    {
        "name": "Custom Abutment with Implant Crown",
        "input": "Placed a custom abutment and screw-retained implant crown on tooth #30.",
        "expected_codes": ["D6057", "D6065"],
        "expected_descriptions": [
            "Custom fabricated abutment - includes placement",
            "Implant supported porcelain/ceramic crown"
        ]
    },
    {
        "name": "Full Mouth X-rays",
        "input": "Performed a complete full-mouth radiographic series to evaluate dental condition.",
        "expected_codes": ["D0210"],
        "expected_descriptions": [
            "Intraoral - complete series of radiographic images"
        ]
    },
    {
        "name": "Frenulectomy",
        "input": "Performed frenectomy on upper labial frenum due to speech and spacing issues.",
        "expected_codes": ["D7960"],
        "expected_descriptions": [
            "Frenulectomy (frenectomy or frenotomy) - separate procedure"
        ]
    },
    {
        "name": "Pulpotomy on Primary Molar",
        "input": "Performed pulpotomy on primary molar with carious pulp exposure.",
        "expected_codes": ["D3220"],
        "expected_descriptions": [
            "Therapeutic pulpotomy (excluding final restoration) - removal of pulp coronal to the dentinocemental junction and application of medicament"
        ]
    },
    {
        "name": "Re-cement Bridge",
        "input": "Re-cemented a 3-unit fixed partial denture that had become loose.",
        "expected_codes": ["D6930"],
        "expected_descriptions": [
            "Re-cement or re-bond fixed partial denture"
        ]
    },
    {
        "name": "Space Maintainer Delivery",
        "input": "Delivered a unilateral space maintainer after extraction of primary molar.",
        "expected_codes": ["D1510"],
        "expected_descriptions": [
            "Space maintainer - fixed, unilateral"
        ]
    }
]

# Test case categories for organization
TEST_CATEGORIES = {
    "preventive": [0, 1, 9],  # Checkup, sealants, fluoride
    "restorative": [2, 10, 11, 16],  # Fillings, crowns, post/core
    "endodontic": [3, 25],  # Root canals, pulpotomy
    "surgical": [4, 12, 18, 24],  # Extractions, incision/drainage, crown lengthening, frenulectomy
    "periodontal": [5, 13, 21],  # SRP, debridement, flap surgery
    "prosthodontic": [6, 20, 26],  # Dentures, partial dentures, bridges
    "diagnostic": [7, 8, 23],  # Exams, radiographs, full mouth x-rays
    "pediatric": [1, 14, 25, 27],  # Child-specific procedures
    "emergency": [7, 17],  # Emergency procedures
    "implant": [22],  # Implant procedures
    "sedation": [19],  # Sedation procedures
    "orthodontic": [27]  # Space maintainers
}

def get_test_cases_by_category(category):
    """Get test cases for a specific category"""
    if category in TEST_CATEGORIES:
        return [TEST_CASES[i] for i in TEST_CATEGORIES[category]]
    return []

def get_all_categories():
    """Get list of all available test categories"""
    return list(TEST_CATEGORIES.keys()) 