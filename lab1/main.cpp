#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <chrono>

struct Particle {
    double x, y, z;
    double vx, vy, vz;
};

const double G = 6.67430e-11;

void compute_force(const Particle& p1, const Particle& p2, double& fx, double& fy, double& fz) {
    double dx = p2.x - p1.x;
    double dy = p2.y - p1.y;
    double dz = p2.z - p1.z;
    double distance = std::sqrt(dx*dx + dy*dy + dz*dz);
    double force = G / (distance * distance);

    fx = force * dx / distance;
    fy = force * dy / distance;
    fz = force * dz / distance;
}

void update_particles(std::vector<Particle>& particles, double dt) {
    int n = particles.size();
    for (int i = 0; i < n; ++i) {
        double fx = 0, fy = 0, fz = 0;
        for (int j = 0; j < n; ++j) {
            if (i != j) {
                double fx_temp, fy_temp, fz_temp;
                compute_force(particles[i], particles[j], fx_temp, fy_temp, fz_temp);
                fx += fx_temp;
                fy += fy_temp;
                fz += fz_temp;
            }
        }

        particles[i].vx += fx * dt;
        particles[i].vy += fy * dt;
        particles[i].vz += fz * dt;

        particles[i].x += particles[i].vx * dt;
        particles[i].y += particles[i].vy * dt;
        particles[i].z += particles[i].vz * dt;
    }
}

int main() {
    int num_particles = 6000;
    double dt = 0.01;
    int num_steps = 10000;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<> dis(0.0, 1.0);

    std::vector<Particle> particles(num_particles);
    for (int i = 0; i < num_particles; ++i) {
        particles[i].x = dis(gen) * 1000;
        particles[i].y = dis(gen) * 1000;
        particles[i].z = dis(gen) * 1000;
        particles[i].vx = dis(gen) * 10;
        particles[i].vy = dis(gen) * 10;
        particles[i].vz = dis(gen) * 10;
    }

    auto start_time = std::chrono::high_resolution_clock::now();
    for (int step = 0; step < num_steps; ++step) {
        update_particles(particles, dt);
    }
    auto end_time = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> elapsed_time = end_time - start_time;
    std::cout << "Simulation completed in " << elapsed_time.count() << " seconds." << std::endl;

    return 0;
}
