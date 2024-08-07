import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="OH SPK 2024")
st.title("Menu")

menu_style = """
<style>
    .menu-grid {
        background: white;
    }
</style>
"""

st.markdown(menu_style, unsafe_allow_html=True)
df = pd.read_csv("./dataset/bazar-2024-items.csv").fillna(0)

sidebar = st.sidebar
sidebar.text("")

# Initialize session state to store the orders if not already done
if 'orders' not in st.session_state:
    st.session_state.orders = {}

grid_per_row = 3

# Create a placeholder for the grid
for n_row, row in df.reset_index().iterrows():
    i = n_row % grid_per_row
    if i == 0:
        grid_row = st.columns(grid_per_row)
    
    col = grid_row[i]
    with col:
        with st.container(border=True):
            menu_name = row['Menu'].title()
            menu_type = row['Jenis'].title() if row['Jenis'] else None
            menu_id = row['ID']
            stock = int(row["Stok"])

            # Unique identifier for each menu item using Menu ID
            order_key = f"{menu_name}_{menu_id}"

            if row['Jenis']:
                st.markdown(f"{menu_name}")
                st.caption(f"*{menu_type}*")
            else:
                st.markdown(f"{menu_name}")
                st.caption("...")

            if order_key in st.session_state.orders:
                # Calculate remaining stock based on previous orders
                stock -= st.session_state.orders[order_key]

            order_amount = st.number_input(
                "Order Amount",
                key=f"numinput-{n_row}",
                min_value=0,
                max_value=stock,
                step=1,
                label_visibility='hidden'
            )
            
            if st.button("Add to order", key=f"btn-{n_row}"):
                if order_key in st.session_state.orders:
                    st.session_state.orders[order_key] += order_amount
                else:
                    st.session_state.orders[order_key] = order_amount

            st.markdown(f'📦 Stock: {stock}')

# Sidebar Order List
with st.sidebar:
    st.markdown("## Order List")
    
    if st.session_state.orders:
        for key, quantity in st.session_state.orders.items():
            item_name = key.split('_')[0]
            st.write(f"{item_name}: {quantity}")
    else:
        st.write("No items ordered yet.")

    if st.button("Clear Orders"):
        st.session_state.orders.clear()
        st.rerun()