import streamlit as st
from ai_component_additions import cortex_demand_forecast
import pandas as pd
from datetime import datetime
from snowflake.snowpark.context import get_active_session
import plotly.express as px


# ---------- AI Demand Forecast (Simple & Explainable) ----------
def forecast_demand(avg_daily_demand, days=7):
    """
    Simple AI-style demand forecast.
    Uses recent average demand to project future need.
    """
    return round(avg_daily_demand * days, 1)

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="CareStock Watch",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.block-container {padding-top: 1.5rem;}
.metric-card {
    background-color: #f8fafc;
    padding: 1rem;
    border-radius: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# SNOWFLAKE SESSION
# =================================================
@st.cache_resource
def get_session():
    return get_active_session()

session = get_session()

# =================================================
# LOAD DATA (Snowflake Dynamic Table = AI Brain)
# =================================================
@st.cache_data(ttl=300)
def load_stock_health():
    return session.sql("""
        SELECT
            LOCATION,
            ITEM,
            CLOSING_STOCK,
            AVG_DAILY_DEMAND,
            DAYS_TO_STOCKOUT,
            STOCK_STATUS,
            LEAD_TIME_DAYS
        FROM STOCK_HEALTH_DT
    """).to_pandas()

df = load_stock_health()

# =================================================
# SESSION STATE (Settings persistence)
# =================================================
if "email_alert" not in st.session_state:
    st.session_state.email_alert = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "sms_alert" not in st.session_state:
    st.session_state.sms_alert = False
if "phone" not in st.session_state:
    st.session_state.phone = ""

# =================================================
# SIDEBAR
# =================================================
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Analytics", "Actions", "Impact", "Settings"]
)

st.sidebar.divider()
st.sidebar.subheader("🔎 Filters")

locations = sorted(df["LOCATION"].unique())
items = sorted(df["ITEM"].unique())

sel_locations = st.sidebar.multiselect("Locations", locations, locations)
sel_items = st.sidebar.multiselect("Items", items, items)

df = df[
    df["LOCATION"].isin(sel_locations) &
    df["ITEM"].isin(sel_items)
].copy()

# =================================================
# DERIVED (UI-ONLY FEATURES)
# =================================================
# =================================================
# CORTEX AI FORECAST
# =================================================
df["AI_FORECAST"] = df.apply(
    lambda row: cortex_demand_forecast(
        row["AVG_DAILY_DEMAND"],
        row["LEAD_TIME_DAYS"],
        horizon_days=7
    ),
    axis=1
)

df["FORECAST_7D"] = df["AI_FORECAST"].apply(lambda x: x["forecast_units"])
df["FORECAST_LOW"] = df["AI_FORECAST"].apply(lambda x: x["lower_bound"])
df["FORECAST_HIGH"] = df["AI_FORECAST"].apply(lambda x: x["upper_bound"])
df["AI_EXPLANATION"] = df["AI_FORECAST"].apply(lambda x: x["explanation"])

df["DAYS_OF_COVER"] = df["CLOSING_STOCK"] / df["LEAD_TIME_DAYS"].replace(0, 1)

# Status badges
status_badge = {
    "Critical": "🔴 Critical",
    "Warning": "🟡 Warning",
    "Healthy": "🟢 Healthy"
}
df["STATUS_BADGE"] = df["STOCK_STATUS"].map(status_badge)

# Item priority (life-saving awareness)
LIFE_SAVING_ITEMS = ["Insulin", "Oxygen", "Blood", "Ventilator"]
df["ITEM_PRIORITY"] = df["ITEM"].apply(
    lambda x: "🔴 Life-saving" if x in LIFE_SAVING_ITEMS else "🟢 Essential"
)

# Overstock / wastage risk
df["OVERSTOCK_RISK"] = df["DAYS_OF_COVER"] > 90
df["OVERSTOCK_BADGE"] = df["OVERSTOCK_RISK"].apply(
    lambda x: "🟣 Overstock risk" if x else ""
)

status_colors = {
    "Critical": "#ef4444",
    "Warning": "#f59e0b",
    "Healthy": "#22c55e"
}

# ================================================
    # DASHBOARD
# =================================================
if page == "Dashboard":

    # -------------------------------------------------
    # PREMIUM HEADER
    # -------------------------------------------------
    st.markdown(
        """
        <h1 style="margin-bottom:0.25rem;">🏥 CareStock Watch</h1>
        <p style="color:#475569; font-size:1rem; max-width:900px;">
        Predicts shortages <b>before shelves go empty</b> and flags overstock 
        to reduce medicine wastage. Intelligence runs inside 
        <b>Snowflake</b> using demand patterns and supplier lead times.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -------------------------------------------------
    # PREMIUM KPI CARDS
    # -------------------------------------------------
    critical = (df["STOCK_STATUS"] == "Critical").sum()
    warning = (df["STOCK_STATUS"] == "Warning").sum()
    healthy = (df["STOCK_STATUS"] == "Healthy").sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="
                background:#FEF2F2;
                border:1px solid #FECACA;
                border-radius:16px;
                padding:20px;
                text-align:center;">
                <div style="font-size:14px; color:#991B1B;">🔴 CRITICAL</div>
                <div style="font-size:36px; font-weight:700; color:#7F1D1D;">
                    {critical}
                </div>
                <div style="font-size:13px; color:#7F1D1D;">
                    Immediate action required
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="
                background:#FFFBEB;
                border:1px solid #FDE68A;
                border-radius:16px;
                padding:20px;
                text-align:center;">
                <div style="font-size:14px; color:#92400E;">🟡 WARNING</div>
                <div style="font-size:36px; font-weight:700; color:#78350F;">
                    {warning}
                </div>
                <div style="font-size:13px; color:#78350F;">
                    Monitor closely
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="
                background:#ECFDF5;
                border:1px solid #A7F3D0;
                border-radius:16px;
                padding:20px;
                text-align:center;">
                <div style="font-size:14px; color:#065F46;">🟢 HEALTHY</div>
                <div style="font-size:36px; font-weight:700; color:#064E3B;">
                    {healthy}
                </div>
                <div style="font-size:13px; color:#064E3B;">
                    Adequate stock coverage
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()


    # Early warnings
    st.subheader("🚨 Early-warning: stock-out risks")
    risk_df = df[df["STOCK_STATUS"].isin(["Critical", "Warning"])]

    st.dataframe(
        risk_df[
            ["LOCATION", "ITEM", "ITEM_PRIORITY", "STATUS_BADGE",
             "CLOSING_STOCK", "DAYS_TO_STOCKOUT"]
        ],
        use_container_width=True
    )
    st.divider()

    # ================================
    # 🤖 Cortex AI – Demand Forecast
    # ================================
    st.subheader("🤖 Cortex AI – Demand Forecast (Next 7 Days)")

    ai_view = df[df["STOCK_STATUS"].isin(["Critical", "Warning"])]

    st.dataframe(
        ai_view[
            [
                "LOCATION",
                "ITEM",
                "AVG_DAILY_DEMAND",
                "FORECAST_7D",
                "FORECAST_LOW",
                "FORECAST_HIGH"
            ]
        ],
        use_container_width=True
    )

    with st.expander("🧠 How Cortex AI made this prediction"):
        st.markdown(
            """
            - Uses recent average daily demand  
            - Projects demand over next 7 days  
            - Considers supplier lead time  
            - Adds a confidence band to reflect uncertainty  

            This AI component is modular and can be replaced
            with Snowflake Cortex models in production.
            """
        )

    st.download_button(
        "⬇️ Download priority list (CSV)",
        risk_df.to_csv(index=False),
        "priority_reorder_list.csv",
        "text/csv"
    )

    st.divider()

    # Overstock
    st.subheader("🟣 Potential wastage (overstock risks)")
    overstock_df = df[df["OVERSTOCK_RISK"]]

    if overstock_df.empty:
        st.info("No overstock risks detected.")
    else:
        st.dataframe(
            overstock_df[
                ["LOCATION", "ITEM", "OVERSTOCK_BADGE",
                 "CLOSING_STOCK", "DAYS_OF_COVER"]
            ],
            use_container_width=True
        )

    st.divider()

    # Explainability
    st.info(
        "🔍 **How decisions are made**  \n"
        "- Avg daily demand is learned from historical usage  \n"
        "- Days-to-stockout = Stock ÷ Demand  \n"
        "- Compared against supplier lead time  \n"
        "- Life-saving items are prioritized  \n"
        "- Overstock is flagged to reduce expiry & waste"
    )
    

# =================================================
# ANALYTICS
# =================================================
elif page == "Analytics":
    st.title("📊 Inventory Analytics")
    st.caption(
        "A visual overview designed for fast decision-making — "
        "clean, focused, and operational."
    )

    st.divider()

    # -------------------------------------------------
    # 1️⃣ STOCK HEALTH DISTRIBUTION (Modern Bar UI)
    # -------------------------------------------------
    st.subheader("Overall stock health")

    status_counts = df.groupby("STOCK_STATUS").size().reset_index(name="COUNT")

    fig_status = px.bar(
        status_counts,
        x="STOCK_STATUS",
        y="COUNT",
        color="STOCK_STATUS",
        color_discrete_map={
            "Critical": "#EF4444",
            "Warning": "#F59E0B",
            "Healthy": "#10B981"
        },
        text="COUNT"
    )

    fig_status.update_layout(
        template="simple_white",
        height=360,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="",
        yaxis_title="Items",
        showlegend=False,
        title=dict(
            text="Items by stock health",
            x=0,
            font=dict(size=18)
        )
    )

    fig_status.update_traces(
        textposition="outside",
        marker=dict(
            line=dict(width=0),
            opacity=0.9
        )
    )

    st.plotly_chart(fig_status, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # 2️⃣ LOCATION RISK COMPARISON (Clean Ranking View)
    # -------------------------------------------------
    st.subheader("Risk concentration by location")

    location_risk = (
        df[df["STOCK_STATUS"].isin(["Critical", "Warning"])]
        .groupby("LOCATION")
        .size()
        .reset_index(name="AT_RISK_ITEMS")
        .sort_values("AT_RISK_ITEMS", ascending=False)
    )

    if location_risk.empty:
        st.info("No locations currently have at-risk items.")
    else:
        fig_location = px.bar(
            location_risk,
            x="LOCATION",
            y="AT_RISK_ITEMS",
            text="AT_RISK_ITEMS",
            color_discrete_sequence=["#6366F1"]
        )

        fig_location.update_layout(
            template="simple_white",
            height=360,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Location",
            yaxis_title="At-risk items",
            title=dict(
                text="Locations with highest risk load",
                x=0,
                font=dict(size=18)
            )
        )

        fig_location.update_traces(
            textposition="outside",
            marker=dict(
                opacity=0.85,
                line=dict(width=0)
            )
        )

        st.plotly_chart(fig_location, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # 3️⃣ HEATMAP (Enterprise-style, Softer Colors)
    # -------------------------------------------------
    st.subheader("Stock coverage heatmap")

    heat = df.pivot(
        index="LOCATION",
        columns="ITEM",
        values="DAYS_OF_COVER"
    ).fillna(0)

    fig_heat = px.imshow(
        heat,
        color_continuous_scale=[
            "#FEE2E2",  # soft red
            "#FEF3C7",  # soft yellow
            "#DCFCE7"   # soft green
        ],
        aspect="auto"
    )

    fig_heat.update_layout(
        template="simple_white",
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(
            text="Days of stock cover (lower = higher risk)",
            x=0,
            font=dict(size=18)
        ),
        coloraxis_colorbar=dict(
            title="Days",
            thickness=12,
            len=0.6
        )
    )

    st.plotly_chart(fig_heat, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # 4️⃣ LIFE-SAVING PRIORITY VIEW (Table, Not Chart)
    # -------------------------------------------------
    st.subheader("Life-saving items at risk")

    life_risk = df[
        (df["ITEM_PRIORITY"] == "🔴 Life-saving") &
        (df["STOCK_STATUS"].isin(["Critical", "Warning"]))
    ]

    if life_risk.empty:
        st.success("All life-saving items are currently well covered.")
    else:
        st.dataframe(
            life_risk[
                ["LOCATION", "ITEM", "STATUS_BADGE",
                 "CLOSING_STOCK", "DAYS_TO_STOCKOUT"]
            ],
            use_container_width=True
        )

        st.warning(
            "Life-saving items shown above should always be prioritized "
            "ahead of non-critical supplies."
        )

    st.divider()

    # -------------------------------------------------
    # 5️⃣ QUICK INSIGHTS (Executive-friendly)
    # -------------------------------------------------
    st.markdown(
        """
        **Quick insights**
        - Focus first on locations with the highest concentration of at-risk items  
        - Life-saving supplies require immediate prioritization  
        - Heatmap reveals hidden gaps that tables alone cannot show  
        - Early visibility enables proactive, not reactive, action
        """
    )
# action

# =================================================
# ACTIONS
# =================================================
elif page == "Actions":

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------
    st.markdown(
        """
        <h1 style="margin-bottom:0.3rem;">📝 Action Log</h1>
        <p style="color:#475569; font-size:1rem; max-width:900px;">
        Record and track actions taken on at-risk items.
        This ensures accountability, coordination, and avoids duplicate efforts.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -------------------------------------------------
    # AT-RISK ITEMS
    # -------------------------------------------------
    at_risk = df[df["STOCK_STATUS"].isin(["Critical", "Warning"])]

    if at_risk.empty:
        st.success("No critical or warning items at the moment 🎉")
    else:
        st.subheader("🚨 Select an at-risk item")

        selected_index = st.selectbox(
            "Item requiring action",
            at_risk.index,
            format_func=lambda i: (
                f"{at_risk.loc[i,'LOCATION']} → "
                f"{at_risk.loc[i,'ITEM']} "
                f"({at_risk.loc[i,'STATUS_BADGE']})"
            )
        )

        selected_item = at_risk.loc[selected_index]

        st.divider()

        # -------------------------------------------------
        # ITEM CONTEXT CARD
        # -------------------------------------------------
        st.markdown(
            f"""
            <div style="
                background:#F8FAFC;
                border:1px solid #E2E8F0;
                border-radius:16px;
                padding:18px;">
                <b>📍 Location:</b> {selected_item['LOCATION']}<br>
                <b>📦 Item:</b> {selected_item['ITEM']}<br>
                <b>🚦 Status:</b> {selected_item['STATUS_BADGE']}<br>
                <b>⏳ Days to stock-out:</b> {round(selected_item['DAYS_TO_STOCKOUT'], 1)}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # -------------------------------------------------
        # ACTION FORM
        # -------------------------------------------------
        st.subheader("✍️ Log action taken")

        with st.form("action_form"):
            action_taken = st.selectbox(
                "Action type",
                [
                    "Purchase order raised",
                    "Transferred from another location",
                    "Delivered to location",
                    "NGO / partner support requested",
                    "Other"
                ]
            )

            notes = st.text_area(
                "Additional notes (optional)",
                placeholder="Add any useful context for other teams or future reference..."
            )

            user = st.text_input(
                "Your name / team",
                placeholder="e.g. District Hospital Supply Team"
            )

            submit = st.form_submit_button("💾 Save action")

        if submit:
            if not user.strip():
                st.error("Please enter your name or team before saving.")
            else:
                session.sql(
                    """
                    INSERT INTO ACTION_LOG
                    (ACTION_TIMESTAMP, LOCATION, ITEM, ACTION_TYPE, NOTES, USER_NAME)
                    VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s)
                    """,
                    params=[
                        selected_item["LOCATION"],
                        selected_item["ITEM"],
                        action_taken,
                        notes,
                        user
                    ]
                ).collect()

                st.success("Action logged successfully ✅")

    st.divider()

    # -------------------------------------------------
    # RECENT ACTIONS
    # -------------------------------------------------
    st.subheader("📜 Recent actions")

    try:
        actions_df = session.sql(
            """
            SELECT
                ACTION_TIMESTAMP,
                LOCATION,
                ITEM,
                ACTION_TYPE,
                NOTES,
                USER_NAME
            FROM ACTION_LOG
            ORDER BY ACTION_TIMESTAMP DESC
            LIMIT 20
            """
        ).to_pandas()

        if actions_df.empty:
            st.info("No actions recorded yet.")
        else:
            st.dataframe(actions_df, use_container_width=True)

    except Exception:
        st.info(
            "Action log table not found. "
            "Create ACTION_LOG table to enable this feature."
        )

    st.info(
        "ℹ️ **Why this matters**  \n"
        "Action logging keeps humans in control, improves coordination, "
        "and creates an audit trail for critical supply decisions."
    )

# =================================================
# SETTINGS
# =================================================
# =================================================
# SETTINGS
# =================================================
elif page == "Settings":

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------
    st.markdown(
        """
        <h1 style="margin-bottom:0.3rem;">⚙️ Alert & Notification Settings</h1>
        <p style="color:#475569; font-size:1rem; max-width:900px;">
        Configure how and when teams should be notified about inventory risks.
        These preferences are designed for flexibility and safe human oversight.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -------------------------------------------------
    # NOTIFICATION CHANNELS
    # -------------------------------------------------
    st.subheader("📢 Notification channels")

    channel_col1, channel_col2 = st.columns(2)

    with channel_col1:
        st.markdown(
            """
            <div style="background:#F8FAFC; border:1px solid #E2E8F0;
                        border-radius:14px; padding:16px;">
            <b>Email alerts</b><br>
            <span style="font-size:13px; color:#475569;">
            Suitable for procurement and planning teams
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.email_alert = st.checkbox(
            "Enable email alerts",
            value=st.session_state.email_alert
        )

        st.session_state.email = st.text_input(
            "Notification email address",
            value=st.session_state.email,
            placeholder="supply-team@hospital.org"
        )

    with channel_col2:
        st.markdown(
            """
            <div style="background:#F8FAFC; border:1px solid #E2E8F0;
                        border-radius:14px; padding:16px;">
            <b>SMS / WhatsApp alerts</b><br>
            <span style="font-size:13px; color:#475569;">
            For urgent, time-sensitive notifications
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.sms_alert = st.checkbox(
            "Enable SMS / WhatsApp alerts",
            value=st.session_state.sms_alert
        )

        st.session_state.phone = st.text_input(
            "Mobile number",
            value=st.session_state.phone,
            placeholder="+91XXXXXXXXXX"
        )

    st.divider()

    # -------------------------------------------------
    # ALERT SEVERITY
    # -------------------------------------------------
    st.subheader("🚦 Alert severity preferences")

    st.markdown(
        """
        Select which inventory conditions should trigger alerts.
        Keeping alerts focused avoids notification fatigue.
        """
    )

    alert_levels = st.multiselect(
        "Send alerts for",
        options=["Critical", "Warning", "Overstock"],
        default=st.session_state.get("alert_levels", ["Critical", "Warning"])
    )

    st.session_state.alert_levels = alert_levels

    st.caption(
        "🔴 **Critical** → immediate risk of stock-out  \n"
        "🟡 **Warning** → stock trending low  \n"
        "🟣 **Overstock** → potential expiry or wastage"
    )

    st.divider()

    # -------------------------------------------------
    # RECIPIENTS
    # -------------------------------------------------
    st.subheader("👥 Alert recipients")

    st.markdown(
        "Choose which teams should receive notifications."
    )

    recipients = st.multiselect(
        "Recipient groups",
        options=[
            "Hospital procurement team",
            "Warehouse manager",
            "District health office",
            "NGO / partner organization"
        ],
        default=st.session_state.get(
            "recipients", ["Hospital procurement team"]
        )
    )

    st.session_state.recipients = recipients

    st.divider()

    # -------------------------------------------------
    # SAVE CONFIRMATION
    # -------------------------------------------------
    if st.button("💾 Save alert preferences"):
        st.success("Alert preferences saved successfully ✅")

    st.info(
        "ℹ️ **Production note**  \n"
        "In a real deployment, these settings would be persisted in a database "
        "and consumed by Snowflake Tasks or external notification services "
        "to deliver alerts automatically."
    )


    # =================================================
# IMPACT
# =================================================
# =================================================
# IMPACT
# =================================================
elif page == "Impact":
    st.markdown(
        """
        <h1 style="margin-bottom:0.3rem;">🌍 Real-world Impact</h1>
        <p style="color:#475569; font-size:1rem; max-width:900px;">
        CareStock Watch is built to create measurable outcomes — protecting patients,
        reducing emergency procurement costs, and minimizing medicine wastage across
        hospitals, public distribution systems, and NGOs.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ---------------- Assumptions ----------------
    PATIENTS_PER_ITEM_PER_DAY = 3
    COST_PER_STOCKOUT = 2500       # INR (estimated emergency procurement)
    WASTE_REDUCTION_RATE = 0.15    # 15% reduction via early visibility
    DAYS_PREVENTED = 5             # days of stock-out avoided on average

    critical = df[df["STOCK_STATUS"] == "Critical"]
    warning = df[df["STOCK_STATUS"] == "Warning"]
    overstock = df[df["OVERSTOCK_RISK"]]

    # ---------------- Calculations ----------------
    patients_protected = (
        len(critical) + len(warning)
    ) * PATIENTS_PER_ITEM_PER_DAY * DAYS_PREVENTED

    cost_saved = len(critical) * COST_PER_STOCKOUT
    waste_reduction_pct = int(WASTE_REDUCTION_RATE * 100)
    locations_covered = df["LOCATION"].nunique()
    items_monitored = df["ITEM"].nunique()

    # ---------------- KPI CARDS ----------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div style="background:#ECFDF5; border:1px solid #A7F3D0;
                        border-radius:16px; padding:18px; text-align:center;">
                <div style="color:#065F46; font-size:14px;">🧑‍⚕️ Patients protected</div>
                <div style="font-size:32px; font-weight:700; color:#064E3B;">
                    {patients_protected}+
                </div>
                <div style="font-size:12px; color:#064E3B;">
                    uninterrupted care
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background:#EFF6FF; border:1px solid #BFDBFE;
                        border-radius:16px; padding:18px; text-align:center;">
                <div style="color:#1E3A8A; font-size:14px;">💰 Cost savings</div>
                <div style="font-size:32px; font-weight:700; color:#1E40AF;">
                    ₹{cost_saved:,}
                </div>
                <div style="font-size:12px; color:#1E40AF;">
                    avoided emergency buys
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="background:#FFFBEB; border:1px solid #FDE68A;
                        border-radius:16px; padding:18px; text-align:center;">
                <div style="color:#92400E; font-size:14px;">♻️ Waste reduced</div>
                <div style="font-size:32px; font-weight:700; color:#78350F;">
                    {waste_reduction_pct}%
                </div>
                <div style="font-size:12px; color:#78350F;">
                    expiry risk avoided
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="background:#F8FAFC; border:1px solid #E2E8F0;
                        border-radius:16px; padding:18px; text-align:center;">
                <div style="color:#334155; font-size:14px;">📦 System scale</div>
                <div style="font-size:32px; font-weight:700; color:#0F172A;">
                    {locations_covered} / {items_monitored}
                </div>
                <div style="font-size:12px; color:#334155;">
                    locations × items
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # ---------------- Impact Breakdown ----------------
    st.subheader("📊 How CareStock Watch creates impact")

    st.markdown(
        """
        - **Early-warning alerts** prevent last-minute shortages  
        - **AI-assisted demand forecasting** enables proactive procurement  
        - **Overstock detection** reduces expiry-driven wastage  
        - **Human-in-the-loop actions** improve accountability  
        - **Shared visibility** aligns hospitals, warehouses, and NGOs
        """
    )

    st.divider()

    # ---------------- Validation Table ----------------
    st.subheader("📌 What problems are being addressed")

    impact_table = pd.DataFrame({
        "Problem": [
            "Stock-outs of critical medicines",
            "Emergency procurement costs",
            "Medicine expiry and wastage",
            "Lack of coordination across teams",
            "Late reaction to demand spikes"
        ],
        "Before CareStock Watch": [
            "Detected after shelves are empty",
            "High, unplanned expenses",
            "Hidden until expiry",
            "Manual follow-ups",
            "Reactive firefighting"
        ],
        "With CareStock Watch": [
            "Detected days in advance",
            "Reduced via early planning",
            "Flagged proactively",
            "Logged & visible actions",
            "Proactive decision-making"
        ]
    })

    st.dataframe(impact_table, use_container_width=True)

    st.divider()

    st.info(
        "Impact metrics are indicative and based on conservative assumptions. "
        "They can be refined using real hospital, PDS, or NGO data during production deployment."
    )
