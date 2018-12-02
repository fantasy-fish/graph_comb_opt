#ifndef I_ENV_H
#define I_ENV_H

#include <vector>
#include <set>

#include "graph.h"

class IState
{
public:
    IState(){};
    IState(const std::vector<int>& action_list,const std::vector<double>& demands)
    {
        this->action_list = action_list;
        this->demands = demands;
    }
    IState(const IState& istate)
    {
        this->action_list = istate.action_list;
        this->demands = istate.demands;
    }
    void set(const std::vector<int>& action_list,const std::vector<double>& demands)
    {
        this->action_list = action_list;
        this->demands = demands;
    }
    std::vector<int> action_list;
    std::vector<double> demands;
};

class IEnv
{
public:

    IEnv(double _norm) : norm(_norm), graph(nullptr) {}

    virtual void s0(std::shared_ptr<Graph> _g) = 0;

    virtual double step(int a) = 0;

    virtual int randomAction() = 0;

    virtual bool isTerminal() = 0;
    
    double norm;
    std::shared_ptr<Graph> graph;
    
    std::vector<IState> state_seq;
    std::vector<double> demands;
    std::vector<int> act_seq, action_list;
    std::vector<double> reward_seq, sum_rewards;
};

#endif