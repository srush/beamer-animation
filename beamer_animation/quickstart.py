import os, sys

def mkdir(dir):
    if os.path.isdir(dir):
        return
    os.makedirs(dir)

def write(file_path, text):
  file = open(file_path, 'w')
  file.write(text)
  file.close()

slides_template = \
r"""\documentclass{beamer}
\mode<presentation>
\setbeamertemplate{navigation symbols}{}

\usepackage{tikz}

% Needed for diagrams.
\def\im#1#2{
  \node(#1) [scale=#2]{\pgfbox[center,top]{\pgfuseimage{#1}}
};}
\input{pictures_header}

\title{Beamer Project}
\author{}

\begin{document}

\begin{frame}
  \titlepage
\end{frame}

\begin{frame}{Sample Animation} 
  \begin{tikzpicture}
     \foreach \x in {1,...,3} {
       \uncover<\x>{\im{dots\x}{1.0}}
     }        
  \end{tikzpicture}
\end{frame}

\end{document}
"""

diagram_template = \
r"""\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{arrows}
\usepackage[graphics,tightpage,active]{preview}
\PreviewEnvironment{tikzpicture}
\begin{document}
\begin{tikzpicture}

${content}

\end{tikzpicture}
\end{document}
"""

generator_template = \
r"""from beamer_animation import latex_lib 
#import pyplot



latex_lib.write_diagram("dot", r"\node [circle] {};")
latex_lib.write_animation("dots", 
                          [r"\node [circle, fill=%s] {};"%color 
                           for color in ["red", "blue", "green"]])
# write_plot()
"""

sconstruct_template = \
r"""import os
env = Environment(ENV=os.environ)
diagram_tex_files = list(env.Glob("diagrams/*.tex"))
plot_tex_files = list(env.Glob("plots/*.tex"))
animation_tex_files = list(env.Glob("animations/*.tex"))
custom_tex_files = list(env.Glob("custom/*.tex"))

generated_tex_files = diagram_tex_files + animation_tex_files + plot_tex_files
all_tex_files = generated_tex_files + custom_tex_files
all_tex_files = map(str, all_tex_files)

env.Command([generated_tex_files], ["scripts/generate_diagrams.py"], 
             "python scripts/generate_diagrams.py")

all_pictures = []
for tex_file in all_tex_files:
  name = tex_file.split(".")[0]
  pdf_file = name + ".pdf"
  all_pictures += env.Command([pdf_file], [tex_file], "rubber  -d -f --inplace " + str(tex_file))
env.Command("slides.pdf", ["slides.tex"] + all_pictures, "rubber  -d -f slides.tex")

# Write all the tex files as pgfdeclareimage's
file_list = "pictures_header.tex"
out = open(file_list, "w")
for tex_file in all_tex_files:
  full_name = str(tex_file).split(".")[0]
  name = full_name.split("/")[-1]
  print >>out, r"\pgfdeclareimage{%s}{%s}"%(name, full_name)
out.close()
"""

def main():
  mkdir("scripts")
  mkdir("scripts/static")
  mkdir("animations")
  mkdir("diagrams")
  mkdir("plots")
  mkdir("custom")
  write("slides.tex", slides_template)
  write("scripts/generate_diagrams.py", generator_template)
  write("scripts/static/diagram.tex.template", diagram_template)
  write("SConstruct", sconstruct_template)
  os.system("python scripts/generate_diagrams.py")

if __name__ == "__main__":
  main()
