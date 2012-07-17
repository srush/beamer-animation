import numpy as np
import random 

def kmeans(points, k, iters=10):
  results = []
  centers = random.sample(points, k)
  for iter in range(iters):

    # E-step
    assigned = [[] for _ in range(k)]
    for p in points:
      center_index = np.argmin(np.array([np.linalg.norm(p - c) for c in centers]))
      assigned[center_index].append(p)
    results.append((assigned, centers))
    # M-Step
    centers = [sum(a) / len(a) for a in assigned]

  return results
    
def main():
  points = [np.random(2) for n in range(50)]
  results = kmeans(points, 5)

if __name__ == "__main__": main()
