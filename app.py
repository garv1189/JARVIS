import streamlit as st
from jarvis import process_command, speak

st.title("JARVIS AI Assistant")
st.write("Enter a command (e.g., 'What's the weather?', 'Stock price AAPL', 'Generate password')")

command = st.text_input("Command")
if st.button("Process Command"):
    if command:
        result = process_command(command.lower())
        st.write(f"Response: {result}")
        # Simulate speech output (Streamlit doesn't support audio output directly)
        st.write("Simulated speech: " + speak(result))
    else:
        st.write("Please enter a command.")
