"""Streamlit UI — thin wrapper around retrieve + generate."""

from __future__ import annotations

import streamlit as st

from .pipeline import ask

st.title("RAG Pipeline")

query = st.text_input("Ask a question about your documents")

if query:
    with st.spinner("Retrieving and generating..."):
        # TODO: uncomment once pipeline.ask() is implemented
        # response = ask(query)
        # st.write(response.answer)
        # st.caption("Sources: " + ", ".join(response.sources))
        st.info("Pipeline not yet implemented — stub only.")
