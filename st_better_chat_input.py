import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from typing import Literal, Sequence
from time import sleep

def st_better_chat_input(orientation: Literal["left", "right"] = "left", borders: bool | Sequence[bool] = False, additional_container: bool = False) -> Sequence[DeltaGenerator]:

    # Validate `orientation`
    if orientation not in {"left", "right"}:
        raise ValueError("Argument 'orientation' must be either 'left' or 'right'.")

    # Validate `borders`
    if not (isinstance(borders, bool) or (isinstance(borders, (list, tuple)) and len(borders) == 4 and all(isinstance(x, bool) for x in borders))):
        raise ValueError("Argument 'borders' must be a boolean (True/False) or a list/tuple of four boolean values.")

    # Validate `additional_container`
    if not isinstance(additional_container, bool):
        raise ValueError("Argument 'additional_container' must be a boolean (True/False).")

    # If `borders` is a boolean, convert it to a list of four identical boolean values for later use
    if isinstance(borders, bool):
        borders = [borders] * 4

    # Build the CSS styles string dynamically based on `orientation`
    CSS_STYLES = f"""
    .st-key-BOTTOM-CONTAINER, .st-key-BUTTONS-CONTAINER {{
        display: flex;
        flex-direction: row !important;
        flex-wrap: nowrap;
        gap: 0.5rem;
        align-items: center;
    }}
    .st-key-BUTTONS-CONTAINER[data-testid="stVerticalBlock"] div {{
        width: max-content !important;
    }}
    .st-key-BOTTOM-CONTAINER > div:{"first" if orientation == "left" else "last"}-child {{
        min-width: max-content;
        max-width: max-content;
    }} 
    .st-key-BOTTOM-CONTAINER > div:{"last" if orientation == "left" else "first"}-child {{
        flex-grow: 1;
    }}
    """

    # Use st._bottom to place all containers at the bottom of the Streamlit app, similar to how normal st.chat_input behaves
    with st._bottom:
        # Apply CSS styles, which allow elements to be displayed in a row
        st.write(f"<style>{CSS_STYLES}</style>", unsafe_allow_html=True)

        # Create additional container if needed
        if additional_container:
            additional_container = st.container(key="ADDITIONAL-CONTAINER", border=borders[3])

        # Create bottom container and its children
        with st.container(key="BOTTOM-CONTAINER", border=borders[0]):
            # Create input and button containers depending on the `orientation`
            if orientation == "left":
                buttons_container = st.container(key="BUTTONS-CONTAINER", border=borders[1])
                input_container =  st.container(key="INPUT-CONTAINER", border=borders[2])
            else:
                input_container =  st.container(key="INPUT-CONTAINER", border=borders[2])
                buttons_container = st.container(key="BUTTONS-CONTAINER", border=borders[1])

    # Return containers including additional if it was created
    if additional_container:
        return buttons_container, input_container, additional_container
    else:
        return buttons_container, input_container

def main():

    # Set Streamlit app layout
    st.set_page_config(layout="wide")

    # Initialize session state variable to track the first run
    if "first_run" not in st.session_state:
        st.session_state["first_run"] = True

    # Create containers for buttons and input field using `st_better_chat_input`
    buttons_container, input_container = st_better_chat_input()

    # Adding a short delay to allow Streamlit to properly render flexbox elements.
    # This prevents incorrect width calculations on first app run caused by the dynamic Streamlit rendering but does not always work.
    if st.session_state["first_run"]:
        sleep(0.5)
        st.session_state["first_run"] = False

    # Example elements placed inside respective containers
    button1 = buttons_container.button(":material/attach_file:", key="button1")
    button2 = buttons_container.button(":material/language:", key="button2")
    chat_input = input_container.chat_input(key="chat_input")

if __name__ == '__main__':
    main()