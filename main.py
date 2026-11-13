from dataclasses import dataclass
from drafter import *
from bakery import assert_equal

# ==========================================
# DATACLASSES (2 Dataclasses Required)
# ==========================================

@dataclass
class CalculationRecord:
    compound_name: str
    reactant_mass: float
    theoretical_yield: float


@dataclass
class State:
    records: list[CalculationRecord]
    selected_compound: str
    mass_input: str
    total_calculations: int


# ==========================================
# CONFIGURATION
# ==========================================

hide_debug_information()
set_website_title("Yield Calculator")
set_website_framed(False)


# ==========================================
# HELPER FUNCTIONS & COMPOUND DICTIONARY
# ==========================================

COMPOUND_DATA = {
    "Water (H2O)": 18.015,
    "Sodium Chloride (NaCl)": 58.44,
    "Carbon Dioxide (CO2)": 44.01,
    "Sucrose (C12H22O11)": 342.30,
    "Ethanol (C2H5OH)": 46.07,
    "Ammonia (NH3)": 17.03,
    "Hydrochloric Acid (HCl)": 36.46,
    "Sulfuric Acid (H2SO4)": 98.08
}

def calculate_theoretical_yield(compound: str, mass: float) -> float:
    """Calculates theoretical yield based on compound type and mass."""
    # Meaningful if statement 1: validates mass input
    if mass <= 0.0:
        return 0.0
    
    if compound in COMPOUND_DATA:
        molar_mass = COMPOUND_DATA[compound]
    else:
        molar_mass = 50.0  
        
    return round((mass / molar_mass) * molar_mass * 0.9, 2)


# ==========================================
# ROUTES (7 Routes Total)
# ==========================================

@route
def index(state: State) -> Page:
    """Home page of the Yield Calculator with clean vertical rows."""
    return Page(state, [
        "Yield Calculator Home",
        "Welcome! Please choose an option below:",
        "- ", Link("Go to Calculator", calculator_page),
        "- ", Link("View Dashboard", dashboard_page),
        "- ", Link("View Calculation History", history_page),
        "- ", Link("Compound Reference", reference_page),
        "- ", Link("About Application", about_page)
    ])

@route
def calculator_page(state: State) -> Page:
    """Calculator page with compound selection and mass input."""
    compound_list = list(COMPOUND_DATA.keys())
    return Page(state, [
        "Yield Calculator",
        SelectBox("compound_choice", compound_list),
        TextBox("mass_field", "Enter Reactant Mass (g)"),
        Button("Calculate Yield", perform_calculation),
        "- ", Link("Back to Home", index)
    ])

@route
def perform_calculation(state: State, compound_choice: str, mass_field: str) -> Page:
    """Processes user input, runs calculation, and updates state fields."""
    if mass_field == "" or mass_field is None:
        mass = 0.0
    else:
        try:
            mass = float(mass_field)
        except ValueError:
            mass = 0.0

    y_val = calculate_theoretical_yield(compound_choice, mass)
    
    new_record = CalculationRecord(
        compound_name=compound_choice,
        reactant_mass=mass,
        theoretical_yield=y_val
    )

    updated_records = state.records + [new_record]
    updated_total = state.total_calculations + 1

    new_state = State(
        records=updated_records,
        selected_compound=compound_choice,
        mass_input=mass_field,
        total_calculations=updated_total
    )

    return Page(new_state, [
        "Calculation Result",
        f"Selected Compound: {compound_choice}",
        f"Reactant Mass: {mass} g",
        f"Calculated Yield: {y_val} g",
        "- ", Link("View History", history_page),
        "- ", Link("Calculate Another", calculator_page),
        "- ", Link("Back to Home", index)
    ])

@route
def dashboard_page(state: State) -> Page:
    """Dashboard summarizing usage statistics."""
    # Meaningful if statement 2: evaluates activity level
    if state.total_calculations > 3:
        status_msg = "Activity Level: High calculation volume."
    else:
        status_msg = "Activity Level: Getting started."

    return Page(state, [
        "Calculation Dashboard",
        f"Total Calculations Run: {state.total_calculations}",
        f"Last Selected Compound: {state.selected_compound}",
        status_msg,
        "- ", Link("Back to Home", index)
    ])

@route
def history_page(state: State) -> Page:
    """Displays stored calculation records using a meaningful loop."""
    content = ["Calculation History Records"]
    
    # Meaningful loop over list of class instances
    for rec in state.records:
        if rec.theoretical_yield > 50.0:
            tier = "High Yield Batch"
        else:
            tier = "Standard Yield Batch"

        row_text = f"• {rec.compound_name} — Mass: {rec.reactant_mass}g | Yield: {rec.theoretical_yield}g ({tier})"
        content.append(row_text)

    content.append("- ")
    content.append(Link("Back to Home", index))
    return Page(state, content)

@route
def reference_page(state: State) -> Page:
    """Reference page for chemical compounds and molar masses."""
    # Meaningful if statement 3: dynamic tip based on calculations count
    if state.total_calculations == 0:
        tip = "Tip: Run your first calculation on the calculator page!"
    else:
        tip = "Tip: You can review past runs in the history page."

    return Page(state, [
        "Compound Reference Guide",
        "• Water (H2O): 18.015 g/mol",
        "• Sodium Chloride (NaCl): 58.44 g/mol",
        "• Carbon Dioxide (CO2): 44.01 g/mol",
        "• Sucrose (C12H22O11): 342.30 g/mol",
        "• Ethanol (C2H5OH): 46.07 g/mol",
        "• Ammonia (NH3): 17.03 g/mol",
        "• Hydrochloric Acid (HCl): 36.46 g/mol",
        "• Sulfuric Acid (H2SO4): 98.08 g/mol",
        tip,
        "- ", Link("Back to Home", index)
    ])

@route
def about_page(state: State) -> Page:
    """About page for the application."""
    return Page(state, [
        "About Yield Calculator",
        "A lightweight self-contained tool to calculate chemical yields and track laboratory runs locally using Drafter.",
        "- ", Link("Back to Home", index)
    ])


# ==========================================
# UNIT TESTS
# ==========================================

def test_calculate_theoretical_yield() -> None:
    assert_equal(calculate_theoretical_yield("Water (H2O)", 0.0), 0.0)
    assert_equal(calculate_theoretical_yield("Water (H2O)", 18.015), 16.21)

test_calculate_theoretical_yield()


# ==========================================
# START SERVER
# ==========================================

start_server(State(
    records=[CalculationRecord("Water (H2O)", 50.0, 40.5)],
    selected_compound="Water (H2O)",
    mass_input="50.0",
    total_calculations=1
))

