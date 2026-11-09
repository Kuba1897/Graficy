#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <random>
#include <algorithm>
#include <iomanip>

using namespace std;

struct Point
{
    double x, y;
};

double distance(const Point &p1, const Point &p2)
{
    return sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y));
}

double calculateTotalDistance(const vector<int> &tour, const vector<Point> &points)
{
    double dist = 0.0;
    int n = tour.size();
    for (int i = 0; i < n; ++i)
    {
        dist += distance(points[tour[i]], points[tour[(i + 1) % n]]);
    }
    return dist;
}

int main()
{

    ifstream infile("salesman.dat");

    if (!infile.is_open())
    {
        cerr << "Nie udalo sie otworzyc pliku" << endl;
        return 1;
    }

    vector<Point> points;
    double x, y;
    while (infile >> x >> y)
    {
        points.push_back({x, y});
    }
    infile.close();

    int n = points.size();
    if (n == 0)
    {
        cerr << "⠀⠀⠀⠀⠈⠟⠻⢛⣿⣿⣿⣷⣶⣦⣄⠀⠸⣿⣿⣿⠗⠀⠀⠀" << endl;
        cerr << "⠀⠀⠀⠀⠀⣼⠀⠄⣿⡿⠋⣉⠈⠙⢿⣿⣦⣿⠏⡠⠂⠀⠀⠀No data?" << endl;
        cerr << "⠀⠀⠀⠀⢰⡌⠀⢠⠏⠇⢸⡇⠐⠀⡄⣿⣿⣃⠈⠀⠀⠀⠀⠀" << endl;
        cerr << "⠀⠀⠀⠀⠈⣻⣿⢫⢻⡆⡀⠁⠀⢈⣾⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀" << endl;

        return 1;
    }

    vector<int> tour(n);
    for (int i = 0; i < n; ++i)
    {
        tour[i] = i;
    }

    double current_dist = calculateTotalDistance(tour, points);
    cout << "Przed wykonaniem algorytmu: " << current_dist << endl;

    vector<int> best_tour = tour;
    double best_dist = current_dist;

    mt19937 gen(42);
    uniform_real_distribution<double> dist_prob(0.0, 1.0);
    uniform_int_distribution<int> dist_idx(0, n - 1);

    int MAX_IT = 2500; // Liczba iteracji dla temperatury

    for (int i = 100; i >= 1; --i)
    {
        double T = 0.001 * i * i;

        for (int it = 0; it < MAX_IT; ++it)
        {
            int idx1 = dist_idx(gen);
            int idx2 = dist_idx(gen);
            if (idx1 == idx2)
                continue;
            if (idx1 > idx2)
                swap(idx1, idx2);

            // krawędzie nie mogą być sąsiednie
            if (idx2 - idx1 == 1 || (idx1 == 0 && idx2 == n - 1))
                continue;

            vector<int> new_tour = tour;
            reverse(new_tour.begin() + idx1 + 1, new_tour.begin() + idx2 + 1);

            double new_dist = calculateTotalDistance(new_tour, points);
            double delta = new_dist - current_dist;

            if (delta < 0 || dist_prob(gen) < exp(-delta / T))
            {
                tour = new_tour;
                current_dist = new_dist;
                if (current_dist < best_dist)
                {
                    best_dist = current_dist;
                    best_tour = tour;
                }
            }
        }
    }

    cout << "Po wykonaniu algorytmu: " << best_dist << endl;

    // Zapis do pliku
    ofstream outfile("salesman_output.dat");
    outfile << best_dist << "\n";
    for (int idx : best_tour)
    {
        outfile << idx << " " << points[idx].x << " " << points[idx].y << "\n";
    }
    outfile << best_tour[0] << " " << points[best_tour[0]].x << " " << points[best_tour[0]].y << "\n";
    outfile.close();
    return 0;
}
