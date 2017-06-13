import networkx as nx
import matplotlib.pyplot as plt
import MySQLdb




connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',db='mala',charset='utf8')
cursor=connect.cursor()



# g=nx.krackhardt_kite_graph()
# g.add_edge('X','Y')
# nx.draw(g)
# print nx.info(g)
# plt.show()
# nx.test()

G=nx.Graph(name='graph')
G.clear()


sql1='SELECT * FROM mala.friendshipall WHERE owneruid=%d'%(752731)
sql2='SELECT * FROM mala.friendshipall'
cursor.execute(sql2)
data=cursor.fetchall()
for i in data:
    G.add_edge(i[0],i[2])
    G.node[i[0]]['size']=300
    # G.node[i[0]]['color']='blue'



# G=nx.Graph(name='graph')
G.add_node(1,time='5pm')
G.add_nodes_from('hello')
# k3=nx.Graph(((1,2),(2,4),(4,5)))
# G.add_edges_from(k3)
G.add_edge(2,3)
print G.node[1]
print G.nodes()
print G.edges()
nx.draw(G,node_size=50,node_color='r',with_labels=False)
plt.show()
G.clear()