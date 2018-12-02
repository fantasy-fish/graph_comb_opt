#ifndef NN_API_H
#define NN_API_H

#include "inet.h"

extern INet* net;

void Predict(std::vector< std::shared_ptr<Graph> >& g_list, std::vector< std::shared_ptr<IState> >& states, std::vector< std::vector<double>* >& pred);

void PredictWithSnapshot(std::vector< std::shared_ptr<Graph> >& g_list, std::vector< std::shared_ptr<IState> >& states, std::vector< std::vector<double>* >& pred);

double Fit(const double lr, std::vector< std::shared_ptr<Graph> >& g_list, std::vector< std::shared_ptr<IState> >& states, std::vector<int>& actions, std::vector<double>& target);

//void Predict(std::vector< std::shared_ptr<Graph> >& g_list, std::vector< std::vector<int>* >& covered, std::vector< std::vector<double>* >& pred);
//covered is states

//void PredictWithSnapshot(std::vector< std::shared_ptr<Graph> >& g_list, std::vector< std::vector<int>* >& covered, std::vector< std::vector<double>* >& pred);
#endif