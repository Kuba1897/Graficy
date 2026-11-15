#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <random>
#include <algorithm>
#include <iomanip>
#include <map>

using namespace std;

struct Page
{
    string name;
    double rank;
};

bool comparePages(const Page &a, const Page &b)
{
    return a.rank > b.rank;
}

int main()
{
    ifstream infile("pagerank.dat");
    if (!infile.is_open())
    {
        cerr << "Nie udalo sie otworzyc pliku" << endl;
        return 1;
    }

    map<string, vector<string>> adjList;
    vector<string> nodes;
    string line;
    while (getline(infile, line))
    {
        if (line.empty())
            continue;
        stringstream ss(line);
        string nodeName;
        char colon;
        ss >> nodeName >> colon;
        nodes.push_back(nodeName);
        string neighbor;
        while (ss >> neighbor)
        {
            if (!neighbor.empty() && neighbor.back() == ',')
            {
                neighbor.pop_back();
            }
            if (!neighbor.empty())
            {
                adjList[nodeName].push_back(neighbor);
            }
        }
    }
    infile.close();

    int n = nodes.size();
    map<string, int> nodeToIndex;
    for (int i = 0; i < n; ++i)
    {
        nodeToIndex[nodes[i]] = i;
    }

    vector<vector<int>> A(n, vector<int>(n, 0));
    vector<int> outDegree(n, 0);
    for (int i = 0; i < n; ++i)
    {
        string u = nodes[i];
        for (const string &v : adjList[u])
        {
            if (nodeToIndex.find(v) != nodeToIndex.end())
            {
                int j = nodeToIndex[v];
                A[i][j] = 1;
                outDegree[i]++;
            }
        }
    }

    double d = 0.15;

    // Błądzenie przypadkowe z teleportacją
    int N_steps = 1000000;
    vector<int> visits(n, 0);
    mt19937 gen(42);
    uniform_real_distribution<double> dist_prob(0.0, 1.0);
    uniform_int_distribution<int> dist_node(0, n - 1);

    int curr = dist_node(gen);
    for (int step = 0; step < N_steps; ++step)
    {
        visits[curr]++;
        if (dist_prob(gen) < d || outDegree[curr] == 0)
        {
            curr = dist_node(gen);
        }
        else
        {
            vector<int> neighbors;
            for (int j = 0; j < n; ++j)
            {
                if (A[curr][j] == 1)
                    neighbors.push_back(j);
            }
            uniform_int_distribution<int> dist_neigh(0, neighbors.size() - 1);
            curr = neighbors[dist_neigh(gen)];
        }
    }

    vector<Page> rankA(n);
    for (int i = 0; i < n; ++i)
    {
        rankA[i] = {nodes[i], (double)visits[i] / N_steps};
    }
    sort(rankA.begin(), rankA.end(), comparePages);

    // Iteracja wektora obsadzeń
    vector<vector<double>> P(n, vector<double>(n, 0.0));
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            double term1 = (outDegree[i] > 0 && A[i][j] == 1) ? ((1.0 - d) * A[i][j] / outDegree[i]) : 0.0;
            double term2 = d / n;
            P[i][j] = term1 + term2;
        }
    }

    vector<double> p(n, 1.0 / n);
    int max_iter = 1000;
    double tol = 1e-9;
    for (int iter = 0; iter < max_iter; ++iter)
    {
        vector<double> p_next(n, 0.0);
        for (int j = 0; j < n; ++j)
        {
            for (int i = 0; i < n; ++i)
            {
                p_next[j] += p[i] * P[i][j];
            }
        }
        double diff = 0.0;
        for (int i = 0; i < n; ++i)
        {
            diff += abs(p_next[i] - p[i]);
        }
        p = p_next;
        if (diff < tol)
            break;
    }

    vector<Page> rankB(n);
    for (int i = 0; i < n; ++i)
    {
        rankB[i] = {nodes[i], p[i]};
    }
    sort(rankB.begin(), rankB.end(), comparePages);

    // Zapis do pliku
    ofstream outfile("pagerank_output.dat");
    outfile << "Bladzenie przypadkowe (N = " << N_steps << "):\n";
    for (const auto &item : rankA)
    {
        outfile << item.name << " ==> PageRank = " << fixed << setprecision(6) << item.rank << "\n";
    }
    outfile << "\nIteracja wektora obsadzen (metoda potegowa):\n";
    for (const auto &item : rankB)
    {
        outfile << item.name << " ==> PageRank = " << fixed << setprecision(6) << item.rank << "\n";
    }
    outfile.close();
    return 0;
}
