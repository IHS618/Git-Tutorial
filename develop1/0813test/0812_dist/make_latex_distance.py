import sys
import os


def ExportTopologyToLatex(NUM_GRID, AREA_SIZE, APS, MSS, FILE_NAME='topology'):

    topo_x = 500
    topo_y = 500
    area_x = NUM_GRID*AREA_SIZE
    area_y = NUM_GRID*AREA_SIZE
    scale_x = topo_x / area_x
    scale_y = topo_y / area_y

    outfile = open(str(FILE_NAME+'.tex'), 'w')
    ("\\documentclass{article}\n")
    outfile.write("\\usepackage{epsfig}\n")
    outfile.write("\\usepackage{color}\n")
    outfile.write("\\usepackage{epic}\n")
    outfile.write("\\usepackage{nopageno}\n")
    outfile.write("\\definecolor{black}{rgb}{0,0,0}\n")
    outfile.write("\\definecolor{red}{rgb}{1,0,0}\n")
    outfile.write("\\definecolor{gray}{rgb}{0.5,0.5,0.5}\n")
    outfile.write("\\definecolor{darkgray}{rgb}{0.25,0.25,0.25}\n")
    outfile.write("\\definecolor{green}{rgb}{0,1,0}\n")
    outfile.write("\\definecolor{blue}{rgb}{0,0,1}\n")
    outfile.write("\\begin{document}\n")
    outfile.write("\\setlength{\\unitlength}{0.2mm}\n")
    outfile.write("\\begin{picture}(500,500)\n")

    # draw area boundary ---------------------------------------------------------
    outfile.write("\\thinlines\n")
    outfile.write("\\put(0,0){\\line(1,0){500}}\n")
    outfile.write("\\put(500,0){\\line(0,1){500}}\n")
    outfile.write("\\put(500,500){\\line(-1,0){500}}\n")
    outfile.write("\\put(0,500){\\line(0,-1){500}}\n")

    # draw walls -----------------------------------------------------------------
    for i in range(1, NUM_GRID):
        pos_x = i*topo_x/NUM_GRID
        outfile.write("\\put(%03d,0){\\line(0,1){500}}\n" % pos_x)

    for i in range(1, NUM_GRID):
        pos_y = i*topo_y/NUM_GRID
        outfile.write("\\put(0,%03d){\\line(1,0){500}}\n" % pos_y)

    # draw APs -------------------------------------------------------------------
    for i in range(len(APS)):
        cx = APS[i, 0]*scale_x
        cy = APS[i, 1]*scale_y
        outfile.write(
            "\\thinlines\\color{gray}\\put(%3d,%3d){\\circle*{10}}\n" % (cx, cy))
        outfile.write(
            "\\thicklines\\color{gray}\\put(%3d,%3d){\\small %d}\n" % (cx+5, cy+5, i))

    # draw mobile stations -------------------------------------------------------
    for i in range(len(MSS)):
        cx = MSS[i, 0]*scale_x
        cy = MSS[i, 1]*scale_y
        outfile.write(
            "\\thicklines\\color{black}\\put(%3d,%3d){\\circle{7}}\n" % (cx, cy))
        outfile.write(
            "\\thicklines\\color{black}\\put(%3d,%3d){\\small %d}\n" % (cx+5, cy+5, i))

    # temporary ------------------------------------------------------------------
    #room_size = 500 / NUM_GRID
    # for j in range(NUM_GRID):
    #  for i in range(NUM_GRID):
    #    ch = (i%2)+(j%2)*2+1
    #    pos_x = j*room_size+room_size-20
    #    pos_y = i*room_size+10
    #    outfile.write("\\thicklines\\color{black}\\put(%.1f,%.1f){\\normalsize %d}\n"%(pos_x, pos_y, ch))

    outfile.write("\\end{picture}\n")
    outfile.write("\\end{document}\n")
    outfile.close()

    os.system("rm -f %s.dvi %s.ps %s.pdf" % (FILE_NAME, FILE_NAME, FILE_NAME))
    os.system("latex %s.tex > /dev/null 2>&1" % FILE_NAME)
    os.system("dvips %s.dvi > /dev/null 2>&1" % FILE_NAME)
    os.system("ps2pdf %s.ps" % FILE_NAME)
    os.system("rm -f %s.dvi %s.ps" % (FILE_NAME, FILE_NAME))

    print('Topology saved to %s.pdf.' % FILE_NAME)
