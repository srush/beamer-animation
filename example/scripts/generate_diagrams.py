import numpy as np
from beamer_animation import latex_lib 
from string import Template
import kmeans

dot_template = """
  \\draw[color=${color}, fill=${fill}, ${extra}]  (${x}, ${y}) circle (0.25); 
  """

box_template = """
  \\draw[color=${color}, fill=${fill}, ${extra}]  (${x}, ${y}) rectangle +(0.4, 0.4); 
  """

def draw_dot(*args):
  return Template(dot_template).substitute(args[0])

def draw_box(*args):
  return Template(box_template).substitute(args[0])

def draw_points(point_sets, centers):
  output = ""
  colors = ["green", "blue", "orange", "brown"]
  for center, points, color in zip(centers, point_sets, colors):

    output += " ".join(draw_dot({"x" : p[0], 
                                 "y" : p[1], 
                                 "color": color + "!70", 
                                 "fill" : color + "!5",
                                 "extra" : "very thick"})
                       for p in points)
    output += draw_box({"x" : center[0], 
                        "y" : center[1],
                        "color": color + "!70", 
                        "fill" : color + "!50",
                        "extra" : "very thick"}) 
                     
  return output
    

def main():
  means = ([5,5], [0,5], [5,0], [0,0])
  points = [np.random.multivariate_normal(np.array(mean),  3.0 * np.eye(2)) 
            for n in range(50)
            for mean in means]   
  results = kmeans.kmeans(points, 4)
  animations = [draw_points(result[0], 
                            result[1]) +
                "\n".join([draw_box({"x" : p[0], 
                                     "y" : p[1], 
                                     "color": "black!80", 
                                     "fill" : "black!70",
                                     "extra" : "thick"})
                          for p in means])
                for result in results]
  latex_lib.write_animation("kmeans", animations)

if __name__ == "__main__": main()

