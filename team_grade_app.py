import streamlit as st
import pandas as pd
import pandas as pd
import numpy as np
import os
from io import StringIO


st.title("Team Grade Tool")
st.header("Upload Rankings Here :point_down:")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Can be used wherever a "file-like" object is accepted:
    data = pd.read_csv(uploaded_file)
    
    # Make a df for each pos to make the app look nicer
    qb_data = data[data['Pos'] == "QB"]
    rb_data = data[data['Pos'] == "RB"]
    wr_data = data[data['Pos'] == "WR"]
    te_data = data[data['Pos'] == "TE"]
    qb_list = qb_data['Player Name'].tolist()
    rb_list = rb_data['Player Name'].tolist()
    wr_list = wr_data['Player Name'].tolist()
    te_list = te_data['Player Name'].tolist()

    ### Have the dropdown always start off with Random Player ###
    # starting_player = player_list.index("Random Player")
    
    ### Enter Your Roster Settings ###
    qbs = st.number_input("How many QB's did you draft?", min_value = 0, max_value = 6)
    
    ### QB ###
    qb_keys = []
    qb_ppgs = []
    for i in range(0, qbs):
        key = st.selectbox('QB #'+str(i+1), qb_list, key = str(i))
        qb_keys.append(key)
    for i in qb_keys:
        qb_ppg = round((qb_data[qb_data['Player Name'] == i]['Proj'].values[0])/17,2)
        qb_ppgs.append(qb_ppg)
    all_qbs = pd.DataFrame(
    {"Player Name": qb_keys,
     "Projected PPG": qb_ppgs,
     "Position": "QB",
    }) 
    
    rbs = st.number_input("How many RB's did you draft?", min_value = 0, max_value = 12)
    
    ### RB ###
    rb_keys = []
    rb_ppgs = []
    for i in range(0, rbs):
        key = st.selectbox('RB #'+str(i+1), rb_list, key = str(i+10))
        rb_keys.append(key)
    for i in rb_keys:
        rb_ppg = round((rb_data[rb_data['Player Name'] == i]['Proj'].values[0])/17,2)
        rb_ppgs.append(rb_ppg)
        
    all_rbs = pd.DataFrame(
    {"Player Name": rb_keys,
     "Projected PPG": rb_ppgs,
     "Position": "RB",
    }) 
    
    wrs = st.number_input("How many WR's did you draft?", min_value = 0, max_value = 12)
    
    ### WR ###
    wr_keys = []
    wr_ppgs = []
    for i in range(0, wrs):
        key = st.selectbox('WR #'+str(i+1), wr_list, key = str(i+20))
        wr_keys.append(key)
    for i in wr_keys:
        wr_ppg = round((wr_data[wr_data['Player Name'] == i]['Proj'].values[0])/17,2)
        wr_ppgs.append(wr_ppg)
        
    all_wrs = pd.DataFrame(
    {"Player Name": wr_keys,
     "Projected PPG": wr_ppgs,
     "Position": "WR",
    })   
    
    tes = st.number_input("How many TE's did you draft?", min_value = 0, max_value = 6)

    ### TE ###
    te_keys = []
    te_ppgs = []
    for i in range(0, tes):
        key = st.selectbox('TE #'+str(i+1), te_list, key = str(i+30))
        te_keys.append(key)
    for i in te_keys:
        te_ppg = round((te_data[te_data['Player Name'] == i]['Proj'].values[0])/17,2)
        te_ppgs.append(te_ppg)
        
    all_tes = pd.DataFrame(
    {"Player Name": te_keys,
     "Projected PPG": te_ppgs,
     "Position": "TE",
    })   
    
    ### Combine DFS ###
    st.subheader("Your Team:")
    st.write("If someone is missing make sure to add them in above")
    dfs = [all_qbs, all_rbs, all_wrs, all_tes]
    all_df = pd.concat(dfs).reset_index(drop=True)
    all_df = all_df[["Position", "Player Name", "Projected PPG"]]
    st.dataframe(all_df)
    
    ### Determine starting lineup and bench ###
    st.header("Input the number of starters for each position")
    st.subheader("This is the amount in your starting lineup each week")
    s_qbs = st.number_input("Starting QB's:", min_value = 0, max_value = 6)
    s_rbs = st.number_input("Starting RB's:", min_value = 0, max_value = 12)
    s_wrs = st.number_input("Starting WR's:", min_value = 0, max_value = 12)
    s_tes = st.number_input("Starting TE's:", min_value = 0, max_value = 6)
    s_flex = st.number_input("Starting FLEX Spots:", min_value = 0, max_value = ((rbs+wrs+tes)-(s_rbs+s_wrs+s_tes)))
    super_flex = st.number_input("Starting SuperFlex Spots:", min_value = 0, max_value = ((qbs+rbs+wrs+tes)-(s_qbs+s_rbs+s_wrs+s_tes)))
    
    # Creating Pos Starters
    starting_qbs = all_qbs.sort_values(by = "Projected PPG", ascending = False)[0:s_qbs]
    starting_rbs = all_rbs.sort_values(by = "Projected PPG", ascending = False)[0:s_rbs]
    starting_wrs = all_wrs.sort_values(by = "Projected PPG", ascending = False)[0:s_wrs]
    starting_tes = all_tes.sort_values(by = "Projected PPG", ascending = False)[0:s_tes]
    
    # Create FLEX Starters
    flex_viable_rbs = all_rbs.sort_values(by = "Projected PPG", ascending = False)[s_rbs:rbs]
    flex_viable_wrs = all_wrs.sort_values(by = "Projected PPG", ascending = False)[s_wrs:wrs]
    flex_viable_tes = all_tes.sort_values(by = "Projected PPG", ascending = False)[s_tes:tes]
    starting_flex = pd.concat([flex_viable_rbs, flex_viable_wrs, flex_viable_tes]).sort_values(by = "Projected PPG", ascending = False)[0:s_flex]
    starting_flex["Position"] = "FLEX"

    # Create SuperFlex
    superflex_viable_qbs = all_qbs.sort_values(by = "Projected PPG", ascending = False)[s_qbs:qbs]
    starting_superflex = pd.concat([superflex_viable_qbs, starting_flex[s_flex:]])[0:super_flex]
    starting_superflex["Position"] = "SuperFlex"
    final_starters = pd.concat([starting_qbs, starting_rbs, starting_wrs, starting_tes, starting_flex, starting_superflex]).reset_index(drop=True)
    final_starters = final_starters[["Position", "Player Name", "Projected PPG"]]    
    
    # Create Bench
    all_df = all_df[["Position", "Player Name", "Projected PPG"]]  
    bench_df = pd.concat([final_starters, all_df])
    bench_df = bench_df.drop_duplicates(subset = ["Player Name", "Projected PPG"], keep=False)
    
    ### Calculate Total Roster Adjusted PPG ###
    if (s_qbs+s_rbs+s_wrs+s_tes+s_flex+super_flex) == 0:
        qb_weight = 0
        rb_weight = 0
        wr_weight = 0
        te_weight = 0        
    else:
        qb_weight = (s_qbs+super_flex)/(s_qbs+s_rbs+s_wrs+s_tes+s_flex+super_flex)
        rb_weight = (s_rbs+s_flex+super_flex)/(s_qbs+s_rbs+s_wrs+s_tes+s_flex+super_flex)
        wr_weight = (s_wrs+s_flex+super_flex)/(s_qbs+s_rbs+s_wrs+s_tes+s_flex+super_flex)
        te_weight = (s_tes+s_flex+super_flex)/(s_qbs+s_rbs+s_wrs+s_tes+s_flex+super_flex)

    # Create df with those weights
    all_weights = pd.DataFrame(
    {"Position": ["QB", "RB", "WR", "TE"],
     "Weight": [qb_weight, rb_weight, wr_weight, te_weight]})  
    
    # Merge weights into bench_df
    bench_weights_df = bench_df.merge(all_weights, on = "Position")
    bench_weights_df["Weighted PPG"] = bench_weights_df["Projected PPG"]*bench_weights_df["Weight"]
    # st.dataframe(bench_weights_df)
    
    # Divide each of those weights by the number on the bench
    qbs_on_bench = bench_weights_df[bench_weights_df["Position"] == "QB"].shape[0]
    rbs_on_bench = bench_weights_df[bench_weights_df["Position"] == "RB"].shape[0]
    wrs_on_bench = bench_weights_df[bench_weights_df["Position"] == "WR"].shape[0]
    tes_on_bench = bench_weights_df[bench_weights_df["Position"] == "TE"].shape[0]
    
    # Adjust weights to reflect that number
    if qbs_on_bench != 0:
        adj_qb_weight = qb_weight/qbs_on_bench
    else:
        adj_qb_weight = 0
    
    if rbs_on_bench != 0:
        adj_rb_weight = rb_weight/rbs_on_bench
    else:
        adj_rb_weight = 0        
    
    if wrs_on_bench != 0:
        adj_wr_weight = wr_weight/wrs_on_bench
    else:
        adj_wr_weight = 0
    
    if tes_on_bench != 0:
        adj_te_weight = te_weight/tes_on_bench
    else:
        adj_te_weight = 0
        
    # Create df with those adj weights
    adj_weights = pd.DataFrame(
    {"Position": ["QB", "RB", "WR", "TE"],
     "Weight": [adj_qb_weight, adj_rb_weight, adj_wr_weight, adj_te_weight]}) 
    
    # Merge weights into bench_df
    adj_bench_weights_df = bench_df.merge(adj_weights, on = "Position")
    adj_bench_weights_df["Weighted PPG"] = adj_bench_weights_df["Projected PPG"]*adj_bench_weights_df["Weight"]
    # st.dataframe(adj_bench_weights_df)
        
    ### Final Outputs ###
    st.subheader("Starting Lineup:")
    st.caption("Note that there are no defense or kicker options.")
    st.caption("You should be drafting those positions last and neither factor into team strength.")
    st.dataframe(final_starters)
    st.subheader("Bench:")
    st.dataframe(bench_df)
    st.write("### Starting Lineup Projected PPG: ", round(final_starters["Projected PPG"].sum(),2))
    st.write("### Total Roster Adjusted PPG: ", (round(adj_bench_weights_df["Weighted PPG"].sum(),2))+(round(final_starters["Projected PPG"].sum(),2)))
    
### Sidebar ###
st.sidebar.image('ffa_red.png', use_column_width=True)
st.sidebar.markdown(" ## About This App:")
st.sidebar.markdown("This app is designed to help you when mock drafting. Input your teams into this app after you're finished a mock draft and see what strategies result in the best teams! It's of course great to try and get the best starting lineup...but bench matters too! Ideally you're trying to maximize 'Total Roster Adjusted PPG'. This is a metric that also assigns some value to your bench, since having a strong bench is very important.")

st.sidebar.markdown("## Steps:")
st.sidebar.markdown("1) Go to the rankings page you want to use. All pages are linked below.")
st.sidebar.markdown("2) Click the button that says 'CSV' directly above the search bar. That will download the rankings to the 'Downloads' folder on your computer.")
st.sidebar.markdown("3) Click 'Browse files' on this page.")
st.sidebar.markdown("4) Find the rankings you just downloaded and open them.")
st.sidebar.markdown("5) Input how many players you drafted at each position, along with the players you drafted. You need to do this before moving on or else it will throw an error for dividing by 0. Also don't worry about going in order. The system will sort best to worst on the backend.")
st.sidebar.markdown("6) Input the number of players you have to start at each position every week.")
st.sidebar.markdown("7) See how good your team is! Your optimal lineup PPG is shown under 'Starting Lineup Projected PPG'.")
st.sidebar.markdown("8) As mentioned above, the strength of your bench is also important. You can try to maximize either metric, but I'd try and get as high a value for 'Total Roster Adjusted PPG' as possible.")

st.sidebar.markdown("## Total Roster Adjusted PPG Explained")
st.sidebar.markdown("The base of this calculation is your starting lineup's projected PPG. From there, points are added depending on how good your bench is. The system will weight how important each position is for your league based on the percent of starting lineup spots that position can fill. It also understands law of diminishing returns, and thus punishes benches that load up too much at one position. Again, this is a better metric to compare your mock drafts against than simple starting lineup PPG.")
st.sidebar.markdown("Just make sure to only compare apples to apples! A PPR SuperFlex team is obviously going to have a higher value than a standard scoring league.")

st.sidebar.markdown("## Quick Links to Rankings:")
st.sidebar.info("Download PPR Rankings [Here](https://www.thefantasyfootballadvice.com/draft-package/2023-ppr-rankings/).")
st.sidebar.info("Download HPPR Rankings [Here](https://www.thefantasyfootballadvice.com/draft-package/2023-half-ppr-rankings/)")
st.sidebar.info("Download Standard Rankings [Here](https://www.thefantasyfootballadvice.com/draft-package/2023-standard-rankings/)")
st.sidebar.info("Download TE Premium Rankings [Here](https://www.thefantasyfootballadvice.com/draft-package/2023-te-premium-rankings/)")
st.sidebar.info("Download PPR SuperFlex Rankings [Here](https://www.thefantasyfootballadvice.com/draft-package/2023-ppr-superflex-rankings/)")
st.sidebar.info("Download FFPC Rankings [Here](https://www.thefantasyfootballadvice.com/draft-package/2023-ffpc-rankings/)")
st.sidebar.info("Download PPR 6 Pt Pass TD Rankings [Here](https://www.thefantasyfootballadvice.com/draft-package/2023-ppr-6-pt-pass-rankings/)")
