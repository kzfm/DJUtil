#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# kzfm <kerolinq@gmail.com>

from sqlalchemy import *
import networkx as nx
import matplotlib.pyplot as plt

f = open('test.sif','w')

#G=nx.Graph()

db = create_engine('sqlite:////Users/kzfm/bin/djutil.db')
metadata = MetaData(bind=db, reflect=True)
music_table = metadata.tables['music']
graph_table = metadata.tables['graph']

music = [m.title for m in music_table.select().execute()]

stmt = graph_table.select()
result = stmt.execute()
for row in result:
    f.write("%s\t%s\t%s" % (music[row.head-1].encode('utf_8'), 'link', music[row.tail-1].encode('utf_8')))
    f.write('\n')
f.close()

#    G.add_edge(music[row.head-1], music[row.tail-1])

#pos=nx.spring_layout(G)
#nx.draw(G,pos,node_color='#A0CBE2',width=1,node_size=80,alpha=0.4,edge_cmap=plt.cm.Blues,font_size=6)
#plt.savefig("path.png")

