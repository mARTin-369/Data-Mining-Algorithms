import random
import math

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def computeClusters(data, k):
    centroids = []
    clusters = []
    types = list(data.keys())
    # print(types)
    for i in range(k):
        cent = random.choice(types)
        centroids.append((data[cent][0], data[cent][1]))
        types.remove(cent)
    # print(centroids)

    while True:
        clusters = [ [] for x in range(k) ]
        for ty, point in data.items():
            i = 0
            dist = distance(centroids[0], point)
            for index, cent in enumerate(centroids):
                d = distance(cent, point)
                if  d < dist:
                    i, dist = index, d
            clusters[i].append(ty)
        
        new_centroids = []
        for cluster in clusters:
            x, y = 0, 0
            for point in cluster:
                x = x + data[point][0]
                y = y + data[point][1]
            new_centroids.append((x/len(cluster),y/len(cluster)))
        
        if centroids != new_centroids:
            centroids = new_centroids
        else:
            break
    return clusters

def getFileData(file_name):
    file_data = {}
    header = []
    with open(file_name) as file:
        lines = file.readlines()

        # Read column names
        header.extend(list(lines[0].split()))
        lines.pop(0)

        # Read row data
        for line in lines:
            point, x, y = list(line.split())
            file_data[point] = (int(x), int(y))
 
    return file_data, header

def main():
    data_file = input("Enter dataset file name: ")
    k = int(input("Enter number of clusters: "))
    data, attributes = getFileData(data_file)
    # print(data)
    clusters = computeClusters(data, k)

    print("\nK-mean Clusters: ")
    for index, cluster in enumerate(clusters):
        print(f"Cluster {index + 1}: {set(cluster)}")

if __name__ == "__main__":
    main()
