set term png font 'DejaVu-Sans,24' \
             size 1200,900
set pointsize 4

set xlabel 'threads'
set ylabel 'time (ms)'

set output 'mandelbrot-8.png'
set xtics 1,1
plot [0:8] [0:900] \
     'mandelbrot-thread-count.data' \
         using 1:($2 / 1000000):($3 / 1000000) with yerrorbars linewidth 3 \
         title 'Render time for thread count', \
     825 / x with lines linewidth 3 title 'linear speedup'


set output 'mandelbrot-16.png'
plot [0:16] [0:900] \
     'mandelbrot-thread-count.data' \
         using 1:($2 / 1000000):($3 / 1000000) with yerrorbars linewidth 3 \
         title 'Render time for thread count', \
     825 / x with lines linewidth 3 title 'linear speedup'


set output 'mandelbrot-100.png'
set xtics autofreq
plot [0:100] [0:900] \
     'mandelbrot-thread-count.data' \
         using 1:($2 / 1000000):($3 / 1000000) with yerrorbars linewidth 3 \
         title 'Render time for thread count', \
     825 / x with lines linewidth 3 title 'linear speedup'


set output 'mandelbrot-1000.png'
plot [0:1000] [0:900] \
     'mandelbrot-thread-count.data' \
         using 1:($2 / 1000000):($3 / 1000000) with yerrorbars linewidth 3 \
         title 'Render time for thread count', \
     825 / x with lines linewidth 3 title 'linear speedup'


### Time taken to plot an empty region of the Mandelbrot set, to show that
### sub-linear speedup is due to some bands having a lot of slow points.

set output 'empty-mandelbrot-8.png'
plot [0:8] \
     'empty-mandel.data' \
         using 1:($2 / 1000000):($3 / 1000000) \
         with yerrorbars linewidth 3 \
         title 'Render time for thread count', \
     11.25 / x \
         with lines linewidth 3 \
         title 'linear speedup'

set output 'empty-mandelbrot-16.png'
plot [0:16] \
     'empty-mandel.data' \
         using 1:($2 / 1000000):($3 / 1000000) \
         with yerrorbars linewidth 3 \
         title 'Render time for thread count', \
     11.25 / x \
         with lines linewidth 3 \
         title 'linear speedup'
