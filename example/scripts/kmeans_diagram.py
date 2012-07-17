from string import Template
import kmeans


dot_template = """
  \\node at (${x}, %{y}) [color=${color}, fill=%{fill}, ${extra}]; 
  """

def draw_dot(**kwargs):
  return Template(dot_template).substitute(kwargs)

def draw_points(points, centers):
  output = ""
  output += " ".join(draw_dot({"x" : p[0], 
                               "y" : p[1], 
                               "color": "red!70", 
                               "fill" : "red!40",
                               "extra" : "circle"})
                     for p in points)
  output += " ".join(draw_dot({"x" : c[0], 
                               "y" : c[1],
                               "color": "blue!70", 
                               "fill" : "blue!40",
                               "extra" : "circle"}) 
                     for c in centers)
  return output
    

def main():
  points = [np.random(2) for n in range(50)]
  results = kmeans(points, 5)
  animations = [draw_points([r[0] for r in result], 
                            [r[1] for r in result]) 
                for result in results]
  write_animation("kmeans", animations)

if __name__ == "__main__": main()
