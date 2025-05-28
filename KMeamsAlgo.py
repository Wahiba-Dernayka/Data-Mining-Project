import csv
import random
import math

def read_csv(file_path):
    data = []
    colors = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                point = [float(row[0]), float(row[1])]
                data.append(point)
                if len(row) > 2:
                    colors.append(row[2])
            except ValueError:
                continue  # skip header or invalid rows
    return data, colors

def euclidean(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def kmeans(data, k, max_iters=100):
    # Randomly initialize centroids
    centroids = random.sample(data, k)
    labels = [0] * len(data)

    for _ in range(max_iters):
        clusters = {i: [] for i in range(k)} #creates a new empty dictionary(cluster) at the start of each iteration

        # Assign points to the nearest centroid
        for idx, point in enumerate(data):
            distances = [euclidean(point, centroid) for centroid in centroids]
            closest_index = distances.index(min(distances))
            clusters[closest_index].append(point)
            labels[idx] = closest_index
            

        # Save old centroids to check for convergence
        old_centroids = centroids.copy()

        # Recalculate new centroids
        for i in range(k):
            cluster = clusters[i]
            if cluster:
                x_mean = sum(p[0] for p in cluster) / len(cluster)
                y_mean = sum(p[1] for p in cluster) / len(cluster)
                centroids[i] = [x_mean, y_mean]

        # Check convergence
        if old_centroids == centroids:
            break

    return centroids, clusters, labels
