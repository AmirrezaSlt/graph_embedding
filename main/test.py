from dask.distributed import Client
client = Client()
client

def input_converter(record): 
    return {
        "user": record["follower_user_id"],
        "followee": record["user_id"],
        "time": record["ctime"]
    }

import dask.bag as db
import json

df = db.read_text('data/user_follower.json').map(json.loads).flatten().map(input_converter).to_dataframe()
df.to_parquet("data/user_follower_df")

from collections import Counter
import dask.array as da
from sqlitedict import SqliteDict
    
values = [df.user.values, df.followee.values]
values = da.concatenate(values, axis=0)
counts = Counter(values.compute())
i = 0
with SqliteDict("data/counts.db", "n", autocommit=False) \
as counts_db, SqliteDict("data/dictionary.db", "n", autocommit=False) as dictionary:
    for index, value in counts.most_common(): 
        dictionary[index] = i
        counts_db[i] = value
        i += 1
    counts_db.commit()
    dictionary.commit()
del counts

import networkx as nx

G = nx.DiGraph()
with SqliteDict("data/dictionary.db", autocommit=False) as dictionary: 
    for row in df.iterrows():
        G.add_edge(dictionary[row['user'], row['followee']])

node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text
fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>CN follower graph',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Author: Amirreza Salamat",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )