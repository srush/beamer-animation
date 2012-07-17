from string import Template

base_template = "".join(open("scripts/static/diagram.tex.template").readlines())

def draw_diagram(content):
  return Template(base_template).substitute({"content" : content})

def write_animation(base_name, animations):
  for i, animation in enumerate(animations):
    file = open("animations/" + base_name + str(i + 1) + ".tex", 'w')
    print >>file, draw_diagram(animation)

def write_diagram(name, code):
  file = open("diagrams/" + name + ".tex", 'w')
  print >>file, draw_diagram(code)

def write_plot(name, code):
  pass
