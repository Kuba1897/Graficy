import matplotlib.pyplot as plt

def visualize_tsp(output_file):
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    best_dist = float(lines[0].strip())
    x_coords = []
    y_coords = []
    
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) >= 3:
            x_coords.append(float(parts[1]))
            y_coords.append(float(parts[2]))
            
    plt.figure(figsize=(9, 7))
    plt.plot(x_coords, y_coords, 'r-o', markersize=4, linewidth=1.2, label='Trasa')
    plt.title(f"Symulowane wyżarzanie – algorytm komiwojażera\nOptymalna długość trasy: {best_dist:.3f}", fontsize=12)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("salesman_result.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    visualize_tsp("salesman_output.dat")
