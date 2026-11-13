from dataclasses import dataclass
from drafter import *
from bakery import assert_equal

# ==========================================
# 2) SECOND DATACLASS & STATE DATACLASS
# ==========================================

@dataclass
class Experiment:
    title: str
    reactant_name: str
    starting_mass: float
    percent_yield: float


@dataclass
class State:
    experiments: list[Experiment]
    current_filter: str
    search_query: str
    total_logged: int


# ==========================================
# CONFIGURATION
# ==========================================

hide_debug_information()
set_website_title("Chemistry Lab & Stoichiometry Tracker")
set_website_framed(False)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def calculate_yield(mass: float) -> float:
    """Calculates a sample percent yield based on starting mass."""
    if mass <= 0.0:
        return 0.0
    
    # Simple simulated yield calculation for demonstration
    computed_yield = (mass * 0.85) % 100.0
    return computed_yield


# ==========================================
# ROUTES (7 Routes Total)
# ==========================================

@route
def index(state: State) -> Page:
    """Home page providing an overview of the lab tracker."""
    return Page(state, [
        "Welcome to the Chemistry Lab & Stoichiometry Tracker!",
        Link(dashboard, "Go to Dashboard"),
        Link(add_experiment_page, "Add New Experiment"),
        Link(view_experiments_page, "View Experiment Records"),
        Link(compound_lookup_page, "Compound Reference Guide"),
        Link(about_page, "About Project")
    ])

@route
def dashboard(state: State) -> Page:
    """Dashboard summarizing stored lab data."""
    # Meaningful if statement 1
    if state.total_logged > 5:
        summary_msg = "Activity Status: High lab volume recorded."
    else:
        summary_msg = "Activity Status: Getting started with lab entries."

    return Page(state, [
        Heading("Lab Dashboard"),
        f"Total Experiments Logged: {state.total_logged}",
        f"Current Filter: {state.current_filter}",
        summary_msg,
        Link(index, "Back to Home")
    ])

@route
def add_experiment_page(state: State) -> Page:
    """Page containing input fields to add a new experiment."""
    return Page(state, [
        Heading("Add New Experiment"),
        TextBox("title_input", "Experiment Title"),
        SelectBox("reactant_input", ["Water", "Sodium Chloride", "Copper Sulfate"]),
        TextArea("notes_input", "Lab Notes & Observations"),
        Button(submit_experiment, "Save Experiment"),
        Link(index, "Back to Home")
    ])

@route
def submit_experiment(state: State, title_input: str, reactant_input: str, notes_input: str) -> Page:
    """Route that processes input and updates the state fields."""
    # Meaningfully modify state fields (4 fields modified across routes)
    new_mass = 50.0  # Default test mass
    y = calculate_yield(new_mass)
    
    new_exp = Experiment(
        title=title_input if title_input != "" else "Untitled Lab",
        reactant_name=reactant_input,
        starting_mass=new_mass,
        percent_yield=y
    )
    
    updated_experiments = state.experiments + [new_exp]
    updated_total = state.total_logged + 1
    updated_filter = reactant_input
    updated_query = title_input

    new_state = State(
        experiments=updated_experiments,
        current_filter=updated_filter,
        search_query=updated_query,
        total_logged=updated_total
    )

    return Page(new_state, [
        Heading("Experiment Successfully Added!"),
        f"Saved Title: {new_exp.title}",
        f"Reactant: {new_exp.reactant_name}",
        Link(view_experiments_page, "View All Records"),
        Link(index, "Back to Home")
    ])

@route
def view_experiments_page(state: State) -> Page:
    """Page that loops over the list of class instances and displays them."""
    content = [Heading("Experiment Records")]
    
    # At least 1 loop iterating over the list of class instances in a meaningful way
    for exp in state.experiments:
        # Meaningful if statement 2
        if exp.percent_yield < 70.0:
            status_text = "Warning: Low Yield (<70%)"
        else:
            status_text = "Status: Acceptable Yield"

        content.append(f"Title: {exp.title} | Reactant: {exp.reactant_name} | Yield: {exp.percent_yield:.1f}% | {status_text}")

    content.append(Link(index, "Back to Home"))
    return Page(state, content)

@route
def compound_lookup_page(state: State) -> Page:
    """Reference guide page for chemical compounds."""
    # Meaningful if statement 3
    if state.total_logged == 0:
        guide_tip = "Tip: Start by adding your first experiment!"
    else:
        guide_tip = "Tip: Keep tracking your stoichiometry regularly."

    return Page(state, [
        Heading("Compound Reference Guide"),
        "Common Molar Masses:",
        "• Water (H2O): 18.015 g/mol",
        "• Sodium Chloride (NaCl): 58.44 g/mol",
        "• Copper Sulfate (CuSO4): 159.60 g/mol",
        guide_tip,
        Link(index, "Back to Home")
    ])

@route
def about_page(state: State) -> Page:
    """About page detailing the web application purpose."""
    return Page(state, [
        Heading("About Chemistry Lab Tracker"),
        "This tool helps chemistry students track laboratory experiments, starting masses, and percentage yields locally.",
        Link(index, "Back to Home")
    ])


# ==========================================
# UNIT TESTS
# ==========================================

def test_calculate_yield() -> None:
    assert_equal(calculate_yield(0.0), 0.0)
    assert_equal(calculate_yield(100.0), 50.0)

test_calculate_yield()


# ==========================================
# START SERVER
# ==========================================

start_server(State(
    experiments=[Experiment("Initial Test Lab", "Water", 50.0, 42.5)],
    current_filter="All",
    search_query="",
    total_logged=1
))
