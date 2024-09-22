import os
import pandas as pd

# Source of csv files, new files have “filtered” added to name
directory = '/run/user/1000/gvfs/smb-share:server=192.168.101.61,share=uni-ai/PCAP/Capture-all-DD-split-DS/'

# This bit shows which file is being worked on, useful for large scale processing
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

for file in csv_files:
    # Load CSV file into a DataFrame
    df = pd.read_csv(os.path.join(directory, file))
    
    # Convert ip.dst column into string, if it contains any non-string values
    df['ip.dst'] = df['ip.dst'].astype(str)
    
    # Filter out rows where ip.src is "192.168.50.254" and ip.dst does not start with "192.168"
    df = df[(df['ip.src'] != '192.168.50.254') | (~df['ip.dst'].str.startswith('192.168'))]
    
    # Save duplicate stripped file in CSV format
    filtered_filename = os.path.splitext(file)[0] + '_filtered.csv'
    df.to_csv(os.path.join(directory, filtered_filename), index=False)