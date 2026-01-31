
import re
from pathlib import Path

import streamlit as st

from devhero.logging_config import configure_logging
from devhero.core.planning import manager_suggests_plan, manager_refine_plan
from devhero.core.runner import run_dynamic_flow
from devhero.services.output_writer import save_agent_outputs_and_zip
from devhero.services.github import push_outputs_to_github
from devhero.utils.parsing import code_blocks_from_text
from devhero.utils.secure import sanitize_error

configure_logging()

st.set_page_config(
    page_title="🤖 DevHero – Multi-Agent Builder (Simple)",
    page_icon="🛠️",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center; color: #005fae;'>🤖 DevHero – Multi-Agent Workflow Automation (Simple)</h1>",
    unsafe_allow_html=True
)

# Initialize session state keys (UI state only)
if "plan" not in st.session_state:
    st.session_state.plan = None
if "plan_refined" not in st.session_state:
    st.session_state.plan_refined = False
if "phase_results" not in st.session_state:
    st.session_state.phase_results = {}
if "current_phase_index" not in st.session_state:
    st.session_state.current_phase_index = 0

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    img_path = Path("assets/devhero.png")
    if img_path.exists():
        st.image(str(img_path), caption="DevHero", width=300)

with col2:
    user_prompt = st.text_area(
        label="Describe your requirement",
        placeholder="e.g., Create a login page with React frontend and Spring Boot backend",
        height=180
    )

# Step 1: Analyze Request
if st.button("🔍 Analyze Request", use_container_width=True):
    if user_prompt.strip():
        with st.spinner("Manager analyzing your request..."):
            try:
                st.session_state.plan = manager_suggests_plan(user_prompt)
                st.session_state.plan_refined = False
                st.session_state.phase_results = {}
                st.session_state.current_phase_index = 0
                st.success("✅ Plan generated! Scroll down to view & run.")
            except Exception as e:
                st.error(f"Manager failed: {sanitize_error(str(e))}")
                st.session_state.plan = None
    else:
        st.warning("⚠️ Please enter a request first.")

# Step 2: Display Plan & Refinement
if st.session_state.get("plan"):
    st.subheader("✅ Manager Suggestion")
    for idx, item in enumerate(st.session_state.plan, start=1):
        agent_role = item.get("agent", "—")
        task_desc = item.get("task", "—")
        tools = item.get("tools", [])
        if isinstance(tools, str):
            tools = [tools]
        plan_text = item.get("plan", "—")

        with st.expander(f"📌 Phase {idx}: {agent_role} — {task_desc}", expanded=True):
            st.markdown(f"**🛠️ Tools:** {', '.join(tools) if tools else '—'}")
            st.markdown(f"**📋 Plan:** {plan_text}")

    st.markdown("### 🔁 Refine the Plan")
    feedback = st.text_input(
        "Suggest improvements (optional):",
        placeholder="e.g., Add QA role, or focus only on frontend"
    )
    if st.button("✨ Refine Plan", use_container_width=True):
        if not feedback.strip():
            st.warning("Please provide feedback text first.")
        else:
            with st.spinner("Manager refining plan..."):
                try:
                    refined_plan = manager_refine_plan(st.session_state.plan, feedback, user_prompt)
                    st.session_state.plan = refined_plan
                    st.session_state.plan_refined = True
                    st.toast("✅ Plan refined successfully!", icon="✨")
                except Exception as e:
                    st.error(f"Refinement failed: {sanitize_error(str(e))}")

    if st.session_state.get("plan_refined"):
        st.markdown("### 🧩 Refined Plan")
        for idx, item in enumerate(st.session_state.plan, start=1):
            agent_role = item.get("agent", "—")
            task_desc = item.get("task", "—")
            tools = item.get("tools", [])
            if isinstance(tools, str):
                tools = [tools]
            plan_text = item.get("plan", "—")

            with st.expander(f"📌 Phase {idx}: {agent_role} — {task_desc}", expanded=True):
                st.markdown(f"**🛠️ Tools:** {', '.join(tools) if tools else '—'}")
                st.markdown(f"**📋 Plan:** {plan_text}")

    st.write("---")

# Step 3: Run Agents Phase-by-Phase
if st.session_state.get("plan"):
    st.markdown("### 🚀 Run Agents Sequentially")

    phases = st.session_state.plan
    current_index = st.session_state.current_phase_index

    if current_index >= len(phases):
        st.success("🎉 All agents have completed successfully!")
    else:
        phase = phases[current_index]
        agent_role = phase.get("agent", "Unknown")
        task_desc = phase.get("task", "—")
        tools_list = phase.get("tools", [])
        tools = ", ".join(tools_list) if isinstance(tools_list, list) else str(tools_list)
        plan_text = phase.get("plan", "—")

        st.markdown(f"#### 📍 Phase {current_index + 1}: {agent_role}")
        st.markdown(f"**🛠️ Tools:** {tools}")
        st.markdown(f"**📋 Task:** {task_desc}")
        st.markdown(f"**🧩 Plan:** {plan_text}")

        if st.button(f"▶️ Run {agent_role}", key=f"run_{current_index}", use_container_width=True):
            with st.spinner(f"{agent_role} executing task..."):
                try:
                    result = run_dynamic_flow(plan=[phase])  # run only this phase
                    output = result[0]["output"] if result else "No output"
                    st.session_state.phase_results[current_index] = output
                    st.toast(f"{agent_role} completed successfully!", icon="🤖")
                except Exception as e:
                    st.error(f"{agent_role} failed: {sanitize_error(str(e))}")

    # If we have an output for current phase, show it and offer actions
    if current_index in st.session_state.phase_results:
        output = st.session_state.phase_results[current_index]
        st.markdown("### 🧾 Agent Output:")
        blocks = code_blocks_from_text(output)
        if blocks:
            text_without_code = re.sub(r"```.*?```", "", output, flags=re.DOTALL).strip()
            if text_without_code:
                st.markdown(text_without_code)
            for lang, code in blocks:
                st.code(code.strip(), language=(lang or "text"))
        else:
            st.markdown(output)

        # Action buttons
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📥 Download Code ZIP", use_container_width=True):
                outputs_to_zip = [
                    {"agent": st.session_state.plan[i]["agent"], "output": st.session_state.phase_results[i]}
                    for i in range(current_index + 1)
                    if i in st.session_state.phase_results
                ]
                zip_bytes = save_agent_outputs_and_zip(outputs_to_zip, zip_name="generated_code.zip")
                st.download_button(
                    label="Download ZIP",
                    data=zip_bytes,
                    file_name="generated_code.zip",
                    mime="application/zip",
                    use_container_width=True
                )

        with c2:
            if st.button("💾 Push to GitHub", use_container_width=True):
                outputs_to_push = [
                    {"agent": st.session_state.plan[i]["agent"], "output": st.session_state.phase_results[i]}
                    for i in range(current_index + 1)
                    if i in st.session_state.phase_results
                ]
                with st.spinner("📦 Pushing outputs to GitHub..."):
                    ok = push_outputs_to_github(outputs_to_push, phase_index=current_index)
                    if ok:
                        st.success("✅ Outputs pushed to GitHub successfully!")
                    else:
                        st.error("❌ Failed to push outputs to GitHub.")

        with c3:
            approved = st.checkbox("✅ Approve this phase to continue", key=f"approve_{current_index}")
            if approved:
                st.session_state.current_phase_index += 1
                st.rerun()
