#include "tsp2d_env.h"
#include "graph.h"
#include <cassert>
#include <random>
#include <iostream>

int sign = 1;

Tsp2dEnv::Tsp2dEnv(double _norm) : IEnv(_norm)
{

}

void Tsp2dEnv::s0(std::shared_ptr<Graph> _g)
{
    graph = _g;
    partial_set.clear();
    action_list.clear();
    action_list.push_back(0);
    partial_set.insert(0);
    assert(graph->demands[0]==1);

    state_seq.clear();
    IState state;
    state.action_list = action_list;
    state.demands = graph->demands;
    state_seq.push_back(state);
    act_seq.clear();
    reward_seq.clear();
    sum_rewards.clear();
}

double Tsp2dEnv::step(int a)
{
    if (a>0)
    {
        assert(graph);
        assert(partial_set.count(a) == 0);
        assert(a > 0 && a < graph->num_nodes);
        graph->demands[0] -= graph->demands[a];
        assert(graph->demands[0]>=0);
        graph->demands[a] = 0;
    }
    else
    {
        assert(a==0);
        graph->demands[0] = 1;
    }
    //state_seq.push_back(action_list);
    IState state;
    state.demands = graph->demands;
    state.action_list = action_list;
    state_seq.push_back(state);
    act_seq.push_back(a);

    double r_t = add_node(a);
    
    reward_seq.push_back(r_t);
    sum_rewards.push_back(r_t);  

    return r_t;
}

int Tsp2dEnv::randomAction()
{
    assert(graph);
    avail_list.clear();
    if(graph->demands[0]!=1)
        avail_list.push_back(0);
    if(graph->demands[0]>0 && graph->demands[0]<1)
    {
        for(int i = 1; i < graph->num_nodes; ++i)
        {
            if(graph->demands[i]!=0 && graph->demands[0]>graph->demands[i])
                avail_list.push_back(i);
            if(graph->demands[i]==0)
                assert(partial_set.count(i)!=0);
        }
    }

    assert(avail_list.size());
    int idx = rand() % avail_list.size();
    return avail_list[idx];
}

bool Tsp2dEnv::isTerminal()
{
    assert(graph);
    return ((int)partial_set.size() == graph->num_nodes);
}

double Tsp2dEnv::add_node(int new_node)
{
    double cur_dist = 10000000.0;
    int pos = -1;
    for (size_t i = 0; i < action_list.size(); ++i)
    {
        int adj;
        if (i + 1 == action_list.size())
            adj = action_list[0];
        else
            adj = action_list[i + 1];
        double cost = graph->dist[new_node][action_list[i]]
                     + graph->dist[new_node][adj]
                     - graph->dist[action_list[i]][adj];
        if (cost < cur_dist)
        {
            cur_dist = cost;
            pos = i;
        }
    }
    assert(pos >= 0);
    assert(cur_dist >= -1e-8);
    action_list.insert(action_list.begin() + pos + 1, new_node);
    partial_set.insert(new_node);

    return sign * cur_dist / norm;
}