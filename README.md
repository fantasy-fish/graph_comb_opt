# Deep Q-Learning with Structure2Vec for solving the Vehicle Routing Problem
Our method is based on the paper "Learning Combinatorial Optimization Algorithms over Graphs" (https://arxiv.org/abs/1704.01665) and the github repository (https://github.com/Hanjun-Dai/graph_comb_opt). The original paper uses Deep Q learning to solve the TSP, while we extend it for the Vehicle Routing Problem. It seems that we are the first one to use DQN to solve VRP. 

# Proposed Framework
This is a figure of our proposed framework. It shows an update step computed by the proposed framework as applied to an instance of the Vehicle Routing Problem. At the beginning of each step, the embedding of each node is just some random number. Then, it's updated after a few iterations of message passing through the Structure2Vec architecture. With the updated node embedding, the Q-value is calculated at each node. Finally, the node with the maximum Q-value is added to the current partial tour. At each step, some nodes may be masked based on the masking mechanism introduced in the project report.<br/>
<img src="https://github.com/fantasy-fish/graph_comb_opt/blob/fantasyfish/visualize/framework.png" width="512" height="512" />

# Sample Runs
Below are two sample runs of S2V-DQN(50) on the VRP20Cap30 Test Set and VRP50Cap40 Test Set. Edges to and from the depot (the black box) are not drawn for clarity.
Legend ordering indicates what order the solution was generated. Each bar is representative of capacity of the vehicle and the black segment represents the demand of the node.
As we follow the path a vehicle took, we notice that the black segment moves up showing us how the vehicle provides for the nodes. The white segment (if it exists) represents 
what portion of the resource was not used in the current route.<br/>
<img src="https://github.com/fantasy-fish/graph_comb_opt/blob/fantasyfish/visualize/cvrp20_94_d.png" width="512" height="512" />
<img src="https://github.com/fantasy-fish/graph_comb_opt/blob/fantasyfish/visualize/cvrp50_11_d.png" width="512" height="512" />

# Reference
    @article{dai2017learning,
      title={Learning Combinatorial Optimization Algorithms over Graphs},
      author={Dai, Hanjun and Khalil, Elias B and Zhang, Yuyu and Dilkina, Bistra and Song, Le},
      journal={arXiv preprint arXiv:1704.01665},
      year={2017}
    }
