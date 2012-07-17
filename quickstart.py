import os, sys
import shutil

def mkdir(dir):
    if sys.path.isdir(dir):
        return
    os.makedirs(dir)

def copy(from_file, to_file):
  shutil.copy(from_file, to_file)

def write(file_path, text):
  file = open(file_path, 'w')
  file.write(text)
  file.close()

slides_template = r"""
\documentclass{beamer}
\mode<presentation>
\setbeamertemplate{navigation symbols}{}

\usepackage{tikz}
% \usetikzlibrary{}

% Needed for diagrams.
\def\im#1#2{
  \node(#1) [scale=#2]{\pgfbox[center,top]{\pgfuseimage{#1}}
};}
\input{diagrams/pictures_header}

\title{}
\date{}
\author{}

\begin{document}

\begin{frame}
  \titlepage
\end{frame}

% \begin{frame}{Sample Animation} 
%   \begin{tikzpicture}
%      \foreach \x in {1,...,8} {
%        \uncover<\x>{\im{animation\x}{1.0}}
%      }        
%   \end{tikzpicture}
% \end{frame}

\end{document}
"""

diagram_template = r"""
\documentclass{article}
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

generator_template = r"""
import latex_lib
"""

sconstruct_template = r"""
import os
env = Environment(ENV=os.environ)
diagram_tex_files = list(env.Glob("diagram/*.tex"))
plot_tex_files = list(env.Glob("plots/*.tex"))
animation_tex_files = list(env.Glob("animation/*.tex"))
custom_tex_files = list(env.Glob("custom/*.tex"))

all_tex_files = diagram_tex_files + \
    plot_tex_files + animation_tex_files + custom_tex_files
all_tex_files = map(str, all_tex_files)

for tex_file in all_tex_files:
  name = tex_file.split(".")[0]
  png_file = name + ".png"
  env.Command(pdf_file, [tex_file], "rubber  -d -f " + str(tex_file))


# Write all the tex files as pgfdeclareimage's
file_list = "pictures_header.tex"
out = open(file_list, "w")
for tex_file in all_tex_files:
  full_name = str(tex_file).split(".")[0]
  name = full_name.split()
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

if __name__ == "__main__":
  main()
