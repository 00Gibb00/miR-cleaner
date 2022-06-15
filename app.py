import streamlit as st
import pandas as pd
import csv

# Configure webpage
st.set_page_config(page_icon='logo4.ico')

st.title("miR-cleaner")
st.markdown("Transform output from high-throughput qPCR machines by removing trailing characters.")

st.sidebar.markdown("### miR-cleaner")
st.sidebar.markdown("Welcome to miR-cleaner! Remove those annoying trailing characters from high-throughput qPCR outputs with a simple click!")
st.sidebar.markdown("Example:")
st.sidebar.markdown("hsa-miR-1-3p-477820_mir --🧼-->")
st.sidebar.markdown("hsa-miR-1-3p")

st.image('soap-emoji.png', width=100)

# Accept user data
uploaded_file =  st.file_uploader('', type='.csv', key='1')

# Allow users to check their data by viewing in browser
if uploaded_file is not None:
    file_container = st.expander("Check your uploaded .csv")
    df_unclean = pd.read_csv(uploaded_file)
    uploaded_file.seek(0)
    file_container.write(df_unclean)

else:
    st.info(
        f"""
            Upload a .csv file above, or download an example file below
        """
    )

# Provide example dataset for download
with open('example.csv', 'r') as file:
    st.download_button('Download example file', file, file_name='example.csv')

### Clean data
if uploaded_file is not None:
    fixed_miRs = []

    # Read file and fix miR names
    miR_list = df_unclean.iloc[:,0].tolist()

    for miR in miR_list:

        # Split miR name into component parts
        miR_splits = miR.split("-")

        # Drop unwanted part
        for split in miR_splits:
            if split[-4:] == "_mir":
                miR_splits.remove(split)

        # Re-join remaining parts
        fixed_miRs.append("-".join(miR_splits))

    df_clean = pd.DataFrame(fixed_miRs)
    output = df_clean.to_csv(index=False).encode('utf-8')
  
    st.download_button('Download cleaned miRs', output, "cleaned_miRs.csv", key='download-cleaned-miRs')
