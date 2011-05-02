#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# kzfm <kerolinq@gmail.com>

from sqlalchemy import *
import networkx as nx
import matplotlib.pyplot as plt

G=nx.Graph()

db = create_engine('sqlite:////Users/kzfm/python/DJUtil/djutil.db')
metadata = MetaData(bind=db, reflect=True)
music_table = metadata.tables['music']
graph_table = metadata.tables['graph']

music = [m.title for m in music_table.select().execute()]

stmt = graph_table.select()
result = stmt.execute()
for row in result:
    G.add_edge(music[row.head-1], music[row.tail-1])

pos=nx.spring_layout(G)
#nx.draw(G,pos,node_color='#A0CBE2',width=1,node_size=20,edge_cmap=plt.cm.Blues,with_labels=False)
nx.draw(G,pos,node_color='#A0CBE2',width=1,node_size=200,alpha=0.4,edge_cmap=plt.cm.Blues,font_size=8)
plt.savefig("path.png")
