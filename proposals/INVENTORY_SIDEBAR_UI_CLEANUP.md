# Inventory App Sidebar UI Cleanup

## Problem Statement

The current inventory app sidebar has several visual and usability issues that make it look "janky":

1. **Long path display** - The processed directory path is shown in full, taking up excessive vertical space
2. **Cramped layout** - Three columns squeezed into narrow sidebar space  
3. **Mixed content hierarchy** - Settings, filters, and jobs mixed without clear separation
4. **Verbose job listings** - Long job descriptions and paths cluttering the interface
5. **Poor visual hierarchy** - No clear grouping or spacing between different sections

## Current Sidebar Structure Issues

```python
# Current problematic layout:
st.sidebar.header("Inventory Settings")
st.sidebar.write("**Processed dir**")
st.sidebar.code(str(PROCESSED_DIR), language="bash")  # LONG PATH!

# Cramped columns in narrow space
colA, colB, colC = st.sidebar.columns(3)  # TOO CRAMPED

# Jobs section at bottom gets cut off
for j in jobs:
    with st.sidebar.expander(lbl, expanded=False):  # VERBOSE
```

## Proposed UI Improvements

### 1. Compact Path Display
```python
# Instead of full path, show just the key parts
st.sidebar.header("📦 Inventory Settings")
processed_name = PROCESSED_DIR.name
parent_name = PROCESSED_DIR.parent.name
st.sidebar.caption(f"📁 {parent_name}/{processed_name}")

# Add tooltip or expandable for full path if needed
with st.sidebar.expander("📍 Full path", expanded=False):
    st.code(str(PROCESSED_DIR), language="bash")
```

### 2. Better Filter Layout
```python
# Replace cramped 3-column layout with vertical stack
st.sidebar.subheader("🔍 Filters")

# Seasons - full width for better readability
selected_seasons = st.sidebar.multiselect(
    "Seasons", 
    seasons, 
    default=seasons,
    help="Select NFL seasons to display"
)

# View options - stacked vertically
only_gaps = st.sidebar.checkbox("🚫 Show only gaps", value=False)
expand_all = st.sidebar.checkbox("📖 Expand all weeks", value=False)
```

### 3. Cleaner Gap Criteria
```python
# Move detailed criteria to main area or simplify
st.sidebar.subheader("📋 Gap Criteria")

# Quick preset buttons instead of individual checkboxes
gap_preset = st.sidebar.selectbox(
    "Data requirements",
    ["Basic (odds + scores)", "Full (all markets)", "Complete (with features)", "Custom"],
    help="Choose what data must be present"
)

# Only show detailed options for "Custom"
if gap_preset == "Custom":
    with st.sidebar.expander("Advanced criteria"):
        req_spreads = st.checkbox("Require spreads")
        req_totals = st.checkbox("Require totals") 
        req_feat_ats = st.checkbox("Require ATS features")
        req_feat_ou = st.checkbox("Require O/U features")
```

### 4. Streamlined Jobs Panel
```python
# Move jobs to top of main area or create separate tab
# If keeping in sidebar, make it much more compact:
if jobs:
    st.sidebar.subheader("⚡ Recent Jobs")
    for j in jobs[:3]:  # Show only 3 most recent
        status_icon = {"queued": "⏳", "running": "🔄", "completed": "✅", "failed": "❌"}.get(j['state'], "❓")
        job_summary = f"{status_icon} #{j['id'][:6]}"
        
        with st.sidebar.expander(job_summary, expanded=False):
            st.caption(j.get("description", "")[:50] + "..." if len(j.get("description", "")) > 50 else j.get("description", ""))
            if j.get("last_error"):
                st.error("Failed")
    
    # Link to full job management
    if len(jobs) > 3:
        st.sidebar.caption(f"... and {len(jobs) - 3} more jobs")
```

### 5. Visual Hierarchy Improvements
```python
# Add clear section separators and consistent spacing
st.sidebar.markdown("---")  # Between major sections

# Use consistent header styles
st.sidebar.subheader("🔍 Filters")  # Icons for visual clarity
st.sidebar.subheader("📋 Requirements") 
st.sidebar.subheader("⚡ Background Jobs")

# Add help text for complex features
st.sidebar.caption("💡 Tip: Use 'Show only gaps' to focus on missing data")
```

### 6. Alternative: Sidebar Tabs
```python
# Option: Split sidebar into tabs for different functions
sidebar_tab = st.sidebar.radio(
    "View",
    ["🔍 Filters", "⚙️ Settings", "⚡ Jobs"],
    horizontal=True
)

if sidebar_tab == "🔍 Filters":
    # Filter controls here
elif sidebar_tab == "⚙️ Settings":
    # Settings and configuration
elif sidebar_tab == "⚡ Jobs":
    # Job management
```

## Complete Proposed Sidebar Layout

```python
# Clean, organized sidebar structure
st.sidebar.header("📦 Data Inventory")

# Compact location info
st.sidebar.caption(f"📁 {PROCESSED_DIR.parent.name}/{PROCESSED_DIR.name}")

st.sidebar.markdown("---")

# Streamlined filters
st.sidebar.subheader("🔍 Filters")
selected_seasons = st.sidebar.multiselect("Seasons", seasons, default=seasons)
only_gaps = st.sidebar.checkbox("🚫 Show only gaps", value=False)

if only_gaps:
    gap_preset = st.sidebar.selectbox(
        "Required data",
        ["Basic", "Full markets", "With features"],
        help="What data must be present"
    )

st.sidebar.markdown("---")

# Compact job status (top 3 only)
if jobs:
    st.sidebar.subheader("⚡ Active Jobs")
    for j in jobs[:3]:
        status = {"queued": "⏳", "running": "🔄", "completed": "✅", "failed": "❌"}.get(j['state'], "❓")
        st.sidebar.caption(f"{status} #{j['id'][:6]} - {j['state']}")
    
    if len(jobs) > 3:
        st.sidebar.caption(f"+ {len(jobs) - 3} more jobs")

st.sidebar.markdown("---")
st.sidebar.caption("💡 Expand weeks to enqueue collection jobs")
```

## Benefits of These Changes

1. **Cleaner visual hierarchy** - Clear sections with consistent spacing
2. **Better space utilization** - No cramped columns, vertical stacking
3. **Reduced visual clutter** - Compact job display, simplified path
4. **Improved usability** - Preset options for common use cases
5. **Consistent iconography** - Visual cues for different section types
6. **Better mobile compatibility** - Vertical layout works better on narrow screens

## Implementation Priority

1. **High Priority**: Fix cramped 3-column layout, compact path display
2. **Medium Priority**: Streamline job listings, add visual separators  
3. **Low Priority**: Add preset gap criteria, implement sidebar tabs

These changes would transform the sidebar from a cluttered, hard-to-use panel into a clean, organized navigation area that enhances rather than detracts from the user experience.
