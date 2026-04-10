# checklist_items.py
# ─────────────────────────────────────────────────────────────────────────────
# Master data for all Daily, Weekly, and Monthly checklist items
# Derived from Dunhill Consulting LLD specifications (April 2026)
# ─────────────────────────────────────────────────────────────────────────────

# input_type values used by the form renderer:
#   yes_no     → radio Yes / No  (status = Done/Issue/N/A separately)
#   decimal    → number input (float)
#   integer    → number input (int)
#   text       → textarea
#   date       → date input
#   dropdown   → selectbox  (options defined in DROPDOWN_OPTIONS)
#   time       → time input

DROPDOWN_OPTIONS = {
    "borehole_status": ["Operational", "Dry", "Under Maintenance", "N/A"],
    "fire_alarm": ["No Faults", "Minor Fault", "Active Alert", "N/A"],
    "maintenance_status": ["Open", "In Progress", "Completed", "On Hold"],
}

# ─── DAILY ITEMS ─────────────────────────────────────────────────────────────
DAILY_ITEMS = [
    # ── Commercial: Utilities — Generator ────────────────────
    {"id": "C-U1", "portfolio": "Commercial", "module": "Utilities — Generator",
     "control_item": "Confirm generator is operational and on standby",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "C-U2", "portfolio": "Commercial", "module": "Utilities — Generator",
     "control_item": "Record generator fuel level (%)",
     "input_type": "decimal", "escalation": "AM", "threshold": {"op": "<", "value": 30, "unit": "%"}},
    {"id": "C-U3", "portfolio": "Commercial", "module": "Utilities — Generator",
     "control_item": "Record generator running hours",
     "input_type": "decimal", "escalation": None, "threshold": None},
    {"id": "C-U6", "portfolio": "Commercial", "module": "Utilities — Generator",
     "control_item": "Check for fuel or oil leaks around generator",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "leak", "value": "Yes"}},

    # ── Commercial: Utilities — Water & Pumps ────────────────
    {"id": "C-W1", "portfolio": "Commercial", "module": "Utilities — Water & Pumps",
     "control_item": "Check water supply is flowing (city council / borehole)",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "C-W2", "portfolio": "Commercial", "module": "Utilities — Water & Pumps",
     "control_item": "Record overhead / underground water tank levels (%)",
     "input_type": "decimal", "escalation": "AM", "threshold": {"op": "<", "value": 25, "unit": "%"}},
    {"id": "C-W3", "portfolio": "Commercial", "module": "Utilities — Water & Pumps",
     "control_item": "Confirm domestic water pumps are operational",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "C-W4", "portfolio": "Commercial", "module": "Utilities — Water & Pumps",
     "control_item": "Confirm fire pump is operational and primed",
     "input_type": "decimal", "escalation": "AM", "threshold": None},
    {"id": "C-W5", "portfolio": "Commercial", "module": "Utilities — Water & Pumps",
     "control_item": "Check sump/basement drainage pumps are operational",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "no_op", "value": "No"}},
    {"id": "C-W6", "portfolio": "Commercial", "module": "Utilities — Water & Pumps",
     "control_item": "Check basement / pump room for flooding",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "flood", "value": "Yes"}},
    {"id": "C-W7", "portfolio": "Commercial", "module": "Utilities — Water & Pumps",
     "control_item": "Record borehole pump status (where applicable)",
     "input_type": "dropdown", "escalation": None, "threshold": None,
     "dropdown_key": "borehole_status"},

    # ── Commercial: Utilities — Electricity & Meters ─────────
    {"id": "C-E3", "portfolio": "Commercial", "module": "Utilities — Electricity & Meters",
     "control_item": "Check main switch room — no tripped breakers, burnt smell, or unusual sounds",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "fault", "value": "No"}},
    {"id": "C-E6", "portfolio": "Commercial", "module": "Utilities — Electricity & Meters",
     "control_item": "Confirm all common area lighting is functional",
     "input_type": "yes_no", "escalation": None, "threshold": None},

    # ── Commercial: Lifts & Vertical Transport ────────────────
    {"id": "C-L1", "portfolio": "Commercial", "module": "Lifts & Vertical Transport",
     "control_item": "Confirm all lifts are operational",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "fault", "value": "No"}},
    {"id": "C-L2", "portfolio": "Commercial", "module": "Lifts & Vertical Transport",
     "control_item": "Check lift interior for cleanliness and damage",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "C-L5", "portfolio": "Commercial", "module": "Lifts & Vertical Transport",
     "control_item": "Confirm goods lift is operational and access is controlled (where applicable)",
     "input_type": "yes_no", "escalation": None, "threshold": None},

    # ── Commercial: Fire Safety & Compliance ─────────────────
    {"id": "C-F3", "portfolio": "Commercial", "module": "Fire Safety & Compliance",
     "control_item": "Confirm fire alarm panel has no active faults or alerts",
     "input_type": "dropdown", "escalation": "AM", "threshold": None,
     "dropdown_key": "fire_alarm"},
    {"id": "C-F5", "portfolio": "Commercial", "module": "Fire Safety & Compliance",
     "control_item": "Confirm all emergency exit doors are functional and unobstructed",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "fault", "value": "No"}},

    # ── Commercial: Security ──────────────────────────────────
    {"id": "C-S1", "portfolio": "Commercial", "module": "Security",
     "control_item": "Confirm all security guards are on duty at their posts",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "absent", "value": "No"}},
    {"id": "C-S2", "portfolio": "Commercial", "module": "Security",
     "control_item": "Confirm CCTV system is recording on all cameras",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "offline", "value": "No"}},
    {"id": "C-S3", "portfolio": "Commercial", "module": "Security",
     "control_item": "Confirm access control system is operational",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "fault", "value": "No"}},
    {"id": "C-S4", "portfolio": "Commercial", "module": "Security",
     "control_item": "Confirm perimeter fence / wall is intact — no damage or breach",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "breach", "value": "No"}},
    {"id": "C-S5", "portfolio": "Commercial", "module": "Security",
     "control_item": "Confirm visitor sign-in process is being followed by security",
     "input_type": "yes_no", "escalation": None, "threshold": None},

    # ── Commercial: Cleaning & Common Areas ──────────────────
    {"id": "C-C1", "portfolio": "Commercial", "module": "Cleaning & Common Areas",
     "control_item": "Confirm cleaning staff are present and on duty",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "absent", "value": "No"}},
    {"id": "C-C2", "portfolio": "Commercial", "module": "Cleaning & Common Areas",
     "control_item": "Inspect all common area corridors, lobbies, and stairwells for cleanliness",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "C-C3", "portfolio": "Commercial", "module": "Cleaning & Common Areas",
     "control_item": "Inspect all common area washrooms — clean, stocked, no blockages",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "C-C4", "portfolio": "Commercial", "module": "Cleaning & Common Areas",
     "control_item": "Confirm garbage collection area is clean and bins not overflowing",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},
    {"id": "C-C5", "portfolio": "Commercial", "module": "Cleaning & Common Areas",
     "control_item": "Inspect external grounds and car park — clean, no litter, no dumping",
     "input_type": "yes_no", "escalation": None, "threshold": None},

    # ── Commercial: Maintenance & Contractor Management ───────
    {"id": "C-M1", "portfolio": "Commercial", "module": "Maintenance & Contractor Management",
     "control_item": "Log all new maintenance issues identified during daily inspection",
     "input_type": "text", "escalation": "AM", "threshold": None},
    {"id": "C-M2", "portfolio": "Commercial", "module": "Maintenance & Contractor Management",
     "control_item": "Update status of all open maintenance issues",
     "input_type": "dropdown", "escalation": None, "threshold": None,
     "dropdown_key": "maintenance_status"},

    # ── Commercial: Tenant Management ────────────────────────
    {"id": "C-T2", "portfolio": "Commercial", "module": "Tenant Management",
     "control_item": "Follow up on all open tenant complaints",
     "input_type": "text", "escalation": "AM", "threshold": None},
    {"id": "C-T4", "portfolio": "Commercial", "module": "Tenant Management",
     "control_item": "Enforce building rules and regulations (signage, parking, delivery times)",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},

    # ── Warehousing: Security ─────────────────────────────────
    {"id": "W-S1", "portfolio": "Warehousing", "module": "Security — Warehousing Specific",
     "control_item": "Confirm entry and exit gates are operational and manned",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "unmanned", "value": "No"}},
    {"id": "W-S2", "portfolio": "Warehousing", "module": "Security — Warehousing Specific",
     "control_item": "Confirm vehicle gate pass / access log is being maintained",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "W-S3", "portfolio": "Warehousing", "module": "Security — Warehousing Specific",
     "control_item": "Confirm armed police / K9 handlers are on duty as contracted (where applicable)",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "absent", "value": "No"}},
    {"id": "W-S4", "portfolio": "Warehousing", "module": "Security — Warehousing Specific",
     "control_item": "Confirm electric fence is operational and alarmed",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "fault", "value": "No"}},
    {"id": "W-S5", "portfolio": "Warehousing", "module": "Security — Warehousing Specific",
     "control_item": "Walk entire perimeter fence — check for damage, gaps, or attempted breach",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "breach", "value": "No"}},
    {"id": "W-S6", "portfolio": "Warehousing", "module": "Security — Warehousing Specific",
     "control_item": "Confirm all CCTV cameras covering go-downs and gates are recording",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "offline", "value": "No"}},

    # ── Warehousing: Tenant & Go-Down Management ─────────────
    {"id": "W-T1", "portfolio": "Warehousing", "module": "Tenant & Go-Down Management",
     "control_item": "Walk all go-down common areas — check cleanliness and access",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "W-T3", "portfolio": "Warehousing", "module": "Tenant & Go-Down Management",
     "control_item": "Confirm tenants are not encroaching on common areas or neighbours' bays",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},
    {"id": "W-T5", "portfolio": "Warehousing", "module": "Tenant & Go-Down Management",
     "control_item": "Confirm go-down roller doors / access doors for vacant units are locked and secure",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "unsecured", "value": "No"}},

    # ── Warehousing: Utilities ────────────────────────────────
    {"id": "W-U3", "portfolio": "Warehousing", "module": "Utilities — Warehousing Specific",
     "control_item": "Confirm common area lighting (roads, security lights, gate lights) is operational",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "W-U4", "portfolio": "Warehousing", "module": "Utilities — Warehousing Specific",
     "control_item": "Confirm water supply to common area ablutions is flowing",
     "input_type": "yes_no", "escalation": None, "threshold": None},

    # ── Warehousing: Waste & Hygiene ─────────────────────────
    {"id": "W-WH2", "portfolio": "Warehousing", "module": "Waste & Hygiene",
     "control_item": "Confirm waste collection area is clean and bins not overflowing",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},

    # ── Residential: Water Supply & Quality ──────────────────
    {"id": "R-W1", "portfolio": "Residential", "module": "Water Supply & Quality",
     "control_item": "Check borehole pump operational status and water level (where applicable)",
     "input_type": "dropdown", "escalation": "AM", "threshold": None,
     "dropdown_key": "borehole_status"},
    {"id": "R-W2", "portfolio": "Residential", "module": "Water Supply & Quality",
     "control_item": "Record overhead and underground tank levels (%)",
     "input_type": "decimal", "escalation": "AM", "threshold": {"op": "<", "value": 30, "unit": "%"}},
    {"id": "R-W3", "portfolio": "Residential", "module": "Water Supply & Quality",
     "control_item": "Confirm RO (Reverse Osmosis) plant is operational (where installed)",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "fault", "value": "No"}},
    {"id": "R-W4", "portfolio": "Residential", "module": "Water Supply & Quality",
     "control_item": "Confirm booster pumps / speed drives are operational",
     "input_type": "decimal", "escalation": "AM", "threshold": None},
    {"id": "R-W5", "portfolio": "Residential", "module": "Water Supply & Quality",
     "control_item": "Confirm water is available at upper floor units (pressure test)",
     "input_type": "decimal", "escalation": "AM", "threshold": None},

    # ── Residential: Lifts ────────────────────────────────────
    {"id": "R-L1", "portfolio": "Residential", "module": "Lifts",
     "control_item": "Confirm all residential lifts are operational",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "fault", "value": "No"}},

    # ── Residential: Swimming Pool & Recreational ─────────────
    {"id": "R-P1", "portfolio": "Residential", "module": "Swimming Pool & Recreational Facilities",
     "control_item": "Confirm pool is clean and water is clear",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},
    {"id": "R-P2", "portfolio": "Residential", "module": "Swimming Pool & Recreational Facilities",
     "control_item": "Record pool chemical levels — chlorine (ppm) and pH",
     "input_type": "decimal", "escalation": "AM", "threshold": None},
    {"id": "R-P3", "portfolio": "Residential", "module": "Swimming Pool & Recreational Facilities",
     "control_item": "Confirm pool pumps and filtration system are operational",
     "input_type": "decimal", "escalation": "AM", "threshold": None},
    {"id": "R-P4", "portfolio": "Residential", "module": "Swimming Pool & Recreational Facilities",
     "control_item": "Confirm pool area is clean (deck, surrounding tiles, changing rooms)",
     "input_type": "yes_no", "escalation": None, "threshold": None},

    # ── Residential: Gym & Fitness Facilities ─────────────────
    {"id": "R-G1", "portfolio": "Residential", "module": "Gym & Fitness Facilities",
     "control_item": "Inspect all gym equipment for damage or malfunction",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},
    {"id": "R-G2", "portfolio": "Residential", "module": "Gym & Fitness Facilities",
     "control_item": "Confirm gym is clean — floors, mirrors, equipment surfaces",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "R-G3", "portfolio": "Residential", "module": "Gym & Fitness Facilities",
     "control_item": "Confirm gym access is controlled per building policy",
     "input_type": "yes_no", "escalation": None, "threshold": None},

    # ── Residential: Steam, Sauna & Spa ───────────────────────
    {"id": "R-SS1", "portfolio": "Residential", "module": "Steam, Sauna & Spa Facilities",
     "control_item": "Confirm steam generator / boiler is operational",
     "input_type": "decimal", "escalation": "AM", "threshold": None},
    {"id": "R-SS2", "portfolio": "Residential", "module": "Steam, Sauna & Spa Facilities",
     "control_item": "Confirm sauna heater is operational and timer-controlled",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "fault", "value": "No"}},
    {"id": "R-SS3", "portfolio": "Residential", "module": "Steam, Sauna & Spa Facilities",
     "control_item": "Confirm steam and sauna rooms are clean and hygienic",
     "input_type": "yes_no", "escalation": None, "threshold": None},

    # ── Residential: Resident & Apartment Management ──────────
    {"id": "R-A2", "portfolio": "Residential", "module": "Resident & Apartment Management",
     "control_item": "Confirm all resident communications responded to within 24 hours",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},
    {"id": "R-A4", "portfolio": "Residential", "module": "Resident & Apartment Management",
     "control_item": "Confirm parking rules are being enforced",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},
    {"id": "R-A5", "portfolio": "Residential", "module": "Resident & Apartment Management",
     "control_item": "Confirm garbage chutes / bin rooms are clean and not overflowing",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},

    # ── Residential: Security — Residential Specific ──────────
    {"id": "R-SR1", "portfolio": "Residential", "module": "Security — Residential Specific",
     "control_item": "Confirm patrol system is being used by security (where patrol logger installed)",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},
    {"id": "R-SR3", "portfolio": "Residential", "module": "Security — Residential Specific",
     "control_item": "Confirm perimeter wall/fence and access gate are intact",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "breach", "value": "No"}},
    {"id": "R-SR4", "portfolio": "Residential", "module": "Security — Residential Specific",
     "control_item": "Confirm visitor management process is followed",
     "input_type": "yes_no", "escalation": None, "threshold": None},

    # ── S&F: Reservations & Occupancy ────────────────────────
    {"id": "SF-R1", "portfolio": "S&F", "module": "Reservations & Occupancy",
     "control_item": "Confirm booking system is reviewed for arrivals and departures today",
     "input_type": "yes_no", "escalation": "AM", "threshold": None},
    {"id": "SF-R2", "portfolio": "S&F", "module": "Reservations & Occupancy",
     "control_item": "Record current occupancy rate (%)",
     "input_type": "decimal", "escalation": "AM", "threshold": {"op": "<", "value": 50, "unit": "%"}},

    # ── S&F: Room & Unit Condition ────────────────────────────
    {"id": "SF-U4", "portfolio": "S&F", "module": "Room & Unit Condition",
     "control_item": "Confirm all linen, towels, and consumables (toiletries, kitchen supplies) are stocked",
     "input_type": "decimal", "escalation": "AM", "threshold": None},

    # ── S&F: Housekeeping ─────────────────────────────────────
    {"id": "SF-HK1", "portfolio": "S&F", "module": "Housekeeping",
     "control_item": "Confirm housekeeping staff are present and on duty",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "absent", "value": "No"}},
    {"id": "SF-HK2", "portfolio": "S&F", "module": "Housekeeping",
     "control_item": "Confirm laundry service is operational (in-house laundry where applicable)",
     "input_type": "yes_no", "escalation": "AM", "threshold": {"op": "fault", "value": "No"}},

    # ── S&F: Spa & Wellness Facilities ───────────────────────
    {"id": "SF-SP1", "portfolio": "S&F", "module": "Spa & Wellness Facilities",
     "control_item": "Confirm spa treatment rooms are clean and prepared for bookings",
     "input_type": "yes_no", "escalation": None, "threshold": None},
    {"id": "SF-SP2", "portfolio": "S&F", "module": "Spa & Wellness Facilities",
     "control_item": "Confirm steam room is operational and clean",
     "input_type": "decimal", "escalation": "AM", "threshold": None},
    {"id": "SF-SP3", "portfolio": "S&F", "module": "Spa & Wellness Facilities",
     "control_item": "Confirm sauna is operational and clean",
     "input_type": "decimal", "escalation": "AM", "threshold": None},
    {"id": "SF-SP4", "portfolio": "S&F", "module": "Spa & Wellness Facilities",
     "control_item": "Confirm jacuzzi / hot tub is clean, chemical levels correct, jets operational",
     "input_type": "decimal", "escalation": "AM", "threshold": None},
    {"id": "SF-SP5", "portfolio": "S&F", "module": "Spa & Wellness Facilities",
     "control_item": "Confirm spa booking system / schedule is up to date",
     "input_type": "yes_no", "escalation": None, "threshold": None},
]

# ─── WEEKLY ITEMS ─────────────────────────────────────────────────────────────
WEEKLY_ITEMS = [
    # ── Commercial: Utilities — Generator ────────────────────
    {"id": "C-U4", "portfolio": "Commercial", "module": "Utilities — Generator",
     "control_item": "Check engine oil level (must be between MIN and MAX)",
     "input_type": "text", "escalation": None, "evidence": "Photo of dipstick"},
    {"id": "C-U5", "portfolio": "Commercial", "module": "Utilities — Generator",
     "control_item": "Confirm coolant is visible and not below minimum mark",
     "input_type": "yes_no", "escalation": None, "evidence": "Photo"},

    # ── Commercial: Utilities — Electricity & Meters ─────────
    {"id": "C-E4", "portfolio": "Commercial", "module": "Utilities — Electricity & Meters",
     "control_item": "Check transformer room — no unusual sounds, heat, or oil leaks",
     "input_type": "yes_no", "escalation": "AM", "evidence": "Photo"},

    # ── Commercial: Fire Safety & Compliance ─────────────────
    {"id": "C-F1", "portfolio": "Commercial", "module": "Fire Safety & Compliance",
     "control_item": "Confirm all fire extinguishers are present, accessible, and within validity",
     "input_type": "date", "escalation": "AM", "evidence": "Photo of extinguisher + tag"},
    {"id": "C-F2", "portfolio": "Commercial", "module": "Fire Safety & Compliance",
     "control_item": "Confirm fire hose reels are accessible and undamaged",
     "input_type": "yes_no", "escalation": None, "evidence": "Photo"},
    {"id": "C-F4", "portfolio": "Commercial", "module": "Fire Safety & Compliance",
     "control_item": "Confirm smoke detectors are present and not obstructed",
     "input_type": "yes_no", "escalation": None, "evidence": "Photo of detector (sample floors)"},
    {"id": "C-F7", "portfolio": "Commercial", "module": "Fire Safety & Compliance",
     "control_item": "Confirm fire suppression system (sprinklers / fire pump) is operational",
     "input_type": "yes_no", "escalation": "AM", "evidence": "Photo of suppression panel"},

    # ── Commercial: Maintenance & Contractor Management ───────
    {"id": "CM6", "portfolio": "Commercial", "module": "Maintenance & Contractor Management",
     "control_item": "Maintain and update consumables/spare parts inventory (no critical item at zero or below reorder)",
     "input_type": "date", "escalation": "AM", "evidence": "Stock register / bin card"},

    # ── Commercial: Tenant Management ────────────────────────
    {"id": "C-T3", "portfolio": "Commercial", "module": "Tenant Management",
     "control_item": "Confirm notice board / building communication is up to date",
     "input_type": "date", "escalation": None, "evidence": "Photo of notice board"},

    # ── Warehousing: Tenant & Go-Down Management ─────────────
    {"id": "W-T6", "portfolio": "Warehousing", "module": "Tenant & Go-Down Management",
     "control_item": "Monitor heavy machinery, chemical storage, or boiler operations within go-downs",
     "input_type": "text", "escalation": "AM", "evidence": "Visual check + logbook note"},

    # ── Warehousing: Drainage & Flooding Prevention ───────────
    {"id": "WD1", "portfolio": "Warehousing", "module": "Drainage & Flooding Prevention",
     "control_item": "Inspect all drainage channels and gulley pots — no blockages",
     "input_type": "yes_no", "escalation": None, "evidence": "Photo"},
    {"id": "WD4", "portfolio": "Warehousing", "module": "Drainage & Flooding Prevention",
     "control_item": "Confirm any internal sump pump in pump room is operational",
     "input_type": "yes_no", "escalation": "AM", "evidence": "Photo of sump pump panel"},

    # ── Warehousing: Waste & Hygiene ─────────────────────────
    {"id": "WWH4", "portfolio": "Warehousing", "module": "Waste & Hygiene",
     "control_item": "Check for rodent activity (droppings, chewed wires, nesting)",
     "input_type": "text", "escalation": "AM", "evidence": "Photo if found"},

    # ── Residential: Swimming Pool & Recreational ─────────────
    {"id": "R-P5", "portfolio": "Residential", "module": "Swimming Pool & Recreational Facilities",
     "control_item": "Confirm pool area safety equipment is present (life ring, depth signs)",
     "input_type": "yes_no", "escalation": "AM", "evidence": "Photo"},
    {"id": "R-P6", "portfolio": "Residential", "module": "Swimming Pool & Recreational Facilities",
     "control_item": "Confirm pool maintenance contractor has serviced as scheduled",
     "input_type": "date", "escalation": "AM", "evidence": "Service report / invoice"},

    # ── Residential: Resident & Apartment Management ──────────
    {"id": "R-A3", "portfolio": "Residential", "module": "Resident & Apartment Management",
     "control_item": "Confirm notice board is current with relevant building communications",
     "input_type": "date", "escalation": None, "evidence": "Photo"},
    {"id": "R-A6", "portfolio": "Residential", "module": "Resident & Apartment Management",
     "control_item": "Confirm landscaping is maintained (grass, trees, flower beds)",
     "input_type": "yes_no", "escalation": "AM", "evidence": "Photo"},

    # ── Residential: Security — Residential Specific ──────────
    {"id": "RSR2", "portfolio": "Residential", "module": "Security — Residential Specific",
     "control_item": "Confirm intercom system is fully operational",
     "input_type": "yes_no", "escalation": "AM", "evidence": "Logbook"},

    # ── S&F: Room & Unit Condition ────────────────────────────
    {"id": "SFU5", "portfolio": "S&F", "module": "Room & Unit Condition",
     "control_item": "Confirm furniture condition — no broken chairs, tables, beds",
     "input_type": "yes_no", "escalation": "AM", "evidence": "Photo of any damage"},

    # ── S&F: Housekeeping ─────────────────────────────────────
    {"id": "SFHK3", "portfolio": "S&F", "module": "Housekeeping",
     "control_item": "Confirm linen inventory is adequate and no shortages (above minimum par)",
     "input_type": "integer", "escalation": "AM", "evidence": "Linen inventory count"},

    # ── S&F: Spa & Wellness Facilities ───────────────────────
    {"id": "SFSP6", "portfolio": "S&F", "module": "Spa & Wellness Facilities",
     "control_item": "Confirm spa consumables (oils, towels, disposables) are stocked above minimum par",
     "input_type": "integer", "escalation": "AM", "evidence": "Inventory sheet"},
]

# ─── MONTHLY ITEMS ────────────────────────────────────────────────────────────
MONTHLY_ITEMS = [
    # ── Commercial: Utilities — Generator ────────────────────
    {"id": "C-U7", "portfolio": "Commercial", "module": "Utilities — Generator",
     "control_item": "Confirm generator AMC service schedule is current",
     "input_type": "date", "escalation": "PH"},
    {"id": "C-U8", "portfolio": "Commercial", "module": "Utilities — Generator",
     "control_item": "Conduct generator load test (run under load)",
     "input_type": "yes_no", "escalation": "AM"},

    # ── Commercial: Utilities — Water & Pumps ────────────────
    {"id": "C-W8", "portfolio": "Commercial", "module": "Utilities — Water & Pumps",
     "control_item": "Record monthly water meter readings (common area)",
     "input_type": "decimal", "escalation": None},

    # ── Commercial: Utilities — Electricity & Meters ─────────
    {"id": "C-E1", "portfolio": "Commercial", "module": "Utilities — Electricity & Meters",
     "control_item": "Record electricity meter readings for all tenant sub-meters",
     "input_type": "decimal", "escalation": None},
    {"id": "C-E2", "portfolio": "Commercial", "module": "Utilities — Electricity & Meters",
     "control_item": "Record common area / landlord electricity meter reading",
     "input_type": "decimal", "escalation": None},
    {"id": "C-E5", "portfolio": "Commercial", "module": "Utilities — Electricity & Meters",
     "control_item": "Check power factor meter reading (where installed)",
     "input_type": "decimal", "escalation": "AM",
     "threshold": {"op": "<", "value": 0.85, "unit": "PF"}},

    # ── Commercial: Lifts & Vertical Transport ────────────────
    {"id": "C-L3", "portfolio": "Commercial", "module": "Lifts & Vertical Transport",
     "control_item": "Confirm lift service/inspection certificate is current and displayed",
     "input_type": "date", "escalation": "PH"},

    # ── Commercial: Fire Safety & Compliance ─────────────────
    {"id": "C-F6", "portfolio": "Commercial", "module": "Fire Safety & Compliance",
     "control_item": "Confirm fire certificate (from fire authority) is current",
     "input_type": "date", "escalation": "PH"},

    # ── Commercial: Maintenance & Contractor Management ───────
    {"id": "C-M5", "portfolio": "Commercial", "module": "Maintenance & Contractor Management",
     "control_item": "Confirm all AMC contractors have serviced within scheduled interval",
     "input_type": "date", "escalation": "AM"},

    # ── Commercial: Tenant Management ────────────────────────
    {"id": "C-T5", "portfolio": "Commercial", "module": "Tenant Management",
     "control_item": "Confirm utility meter readings distributed to tenants",
     "input_type": "decimal", "escalation": None},

    # ── Commercial: Statutory Compliance ─────────────────────
    {"id": "C-SC1", "portfolio": "Commercial", "module": "Statutory Compliance",
     "control_item": "Confirm fire certificate is valid and displayed",
     "input_type": "date", "escalation": "PH"},
    {"id": "C-SC2", "portfolio": "Commercial", "module": "Statutory Compliance",
     "control_item": "Confirm lift inspection certificate is valid",
     "input_type": "date", "escalation": "PH"},
    {"id": "C-SC3", "portfolio": "Commercial", "module": "Statutory Compliance",
     "control_item": "Confirm business/operating permit is valid",
     "input_type": "date", "escalation": "PH"},
    {"id": "C-SC5", "portfolio": "Commercial", "module": "Statutory Compliance",
     "control_item": "Confirm workplace/occupation certificate is held and valid",
     "input_type": "yes_no", "escalation": "PH"},

    # ── Warehousing: Tenant & Go-Down Management ─────────────
    {"id": "W-T2", "portfolio": "Warehousing", "module": "Tenant & Go-Down Management",
     "control_item": "Confirm go-down unit numbers are clearly marked",
     "input_type": "yes_no", "escalation": None},

    # ── Warehousing: Drainage & Flooding Prevention ───────────
    {"id": "W-D2", "portfolio": "Warehousing", "module": "Drainage & Flooding Prevention",
     "control_item": "Confirm down pipes from roofs are clear and directing water to drains",
     "input_type": "yes_no", "escalation": None},

    # ── Warehousing: Utilities ────────────────────────────────
    {"id": "W-U1", "portfolio": "Warehousing", "module": "Utilities — Warehousing Specific",
     "control_item": "Record water meter readings for each go-down (where sub-metered)",
     "input_type": "decimal", "escalation": None},
    {"id": "W-U2", "portfolio": "Warehousing", "module": "Utilities — Warehousing Specific",
     "control_item": "Record electricity meter readings for each go-down (where sub-metered)",
     "input_type": "decimal", "escalation": None},

    # ── Residential: Water Supply & Quality ──────────────────
    {"id": "R-W6", "portfolio": "Residential", "module": "Water Supply & Quality",
     "control_item": "Record water meter readings — common area and borehole (where metered)",
     "input_type": "decimal", "escalation": None},

    # ── Residential: Lifts ────────────────────────────────────
    {"id": "R-L2", "portfolio": "Residential", "module": "Lifts",
     "control_item": "Confirm lift inspection certificate is current",
     "input_type": "date", "escalation": "PH"},
    {"id": "R-L3", "portfolio": "Residential", "module": "Lifts",
     "control_item": "Confirm lift AMC service is current (Kone, Schindler, East African Elevator)",
     "input_type": "date", "escalation": "AM"},

    # ── Residential: Steam, Sauna & Spa ───────────────────────
    {"id": "R-SS4", "portfolio": "Residential", "module": "Steam, Sauna & Spa Facilities",
     "control_item": "Confirm steam/sauna maintenance contractor has serviced as scheduled",
     "input_type": "date", "escalation": "AM"},

    # ── S&F: Statutory — S&F Specific ────────────────────────
    {"id": "SF-SC1", "portfolio": "S&F", "module": "Statutory — S&F Specific",
     "control_item": "Confirm business permit (hospitality / short-term let) is valid",
     "input_type": "date", "escalation": "PH"},
    {"id": "SF-SC2", "portfolio": "S&F", "module": "Statutory — S&F Specific",
     "control_item": "Confirm food hygiene / food handling certificate is valid (where food served)",
     "input_type": "date", "escalation": "PH"},
    {"id": "SF-SC3", "portfolio": "S&F", "module": "Statutory — S&F Specific",
     "control_item": "Confirm music / entertainment license is valid",
     "input_type": "date", "escalation": "PH"},
    {"id": "SF-SC4", "portfolio": "S&F", "module": "Statutory — S&F Specific",
     "control_item": "Confirm advertisement permit is valid",
     "input_type": "date", "escalation": "PH"},
]

# ─── Helper: get items by frequency + portfolio ──────────────────────────────
def get_items(frequency: str, portfolio: str) -> list:
    source = {"daily": DAILY_ITEMS, "weekly": WEEKLY_ITEMS, "monthly": MONTHLY_ITEMS}
    items = source.get(frequency, [])
    _p = portfolio.strip()
    return [
        i for i in items
        if i["portfolio"].lower() == _p.lower()
        or (portfolio in ("S&F", "Serviced & Furnished") and i["portfolio"] == "S&F")
    ]

def get_modules(frequency: str, portfolio: str) -> list:
    """Return distinct module names in order for the given filter."""
    seen, modules = set(), []
    for item in get_items_for_frequency(frequency, portfolio):
        m = item["module"]
        if m not in seen:
            seen.add(m)
            modules.append(m)
    return modules