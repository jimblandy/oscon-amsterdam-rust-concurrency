set term png font 'DejaVu-Sans,24' \
             size 1200,900
set pointsize 4

set xlabel 'threads'
set ylabel 'pixels / ms'

mand_rate = 2800
mand_limit = 30000

set output 'images/mandelbrot-8-no-ideal.png'
set xtics 1,1
plot [0:8] [0:mand_limit] \
     'mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed'

set output 'images/mandelbrot-8.png'
plot [0:8] [0:mand_limit] \
     'mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed', \
     mand_rate * x with lines linewidth 3 title 'ideal'

set output 'images/mandelbrot-16.png'
plot [0:16] [0:mand_limit] \
     'mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed', \
     x <= 8 ? mand_rate * x : mand_rate * 8 with lines linewidth 3 title 'eight-core ideal', \
     x <= 4 ? mand_rate * x : mand_rate * 4 with lines linewidth 3 title 'four-core ideal'

set output 'images/mandelbrot-100.png'
set xtics autofreq
plot [0:100] [0:mand_limit] \
     'mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed', \
     x <= 8 ? mand_rate * x : mand_rate * 8 with lines linewidth 3 title 'eight-core ideal', \
     x <= 4 ? mand_rate * x : mand_rate * 4 with lines linewidth 3 title 'four-core ideal'

set output 'images/mandelbrot-1000.png'
plot [0:1000] [0:mand_limit] \
     'mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed', \
     x <= 8 ? mand_rate * x : mand_rate * 8 with lines linewidth 3 title 'eight-core ideal', \
     x <= 4 ? mand_rate * x : mand_rate * 4 with lines linewidth 3 title 'four-core ideal'


### Time taken to plot an empty region of the Mandelbrot set, to show that
### sub-linear speedup is due to some bands having a lot of slow points.

empty_rate = 216000
empty_limit = 1050000

set output 'images/empty-mandelbrot-8.png'
set xtics 1,1
plot [0:8] [0:empty_limit] \
     'empty-mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed', \
     x <= 4 ? 216000 * x : 216000 * 4 with lines linewidth 3 title 'four-core ideal'

set output 'images/empty-mandelbrot-16.png'
plot [0:16] [0:empty_limit] \
     'empty-mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed', \
     x <= 4 ? 216000 * x : 216000 * 4 with lines linewidth 3 title 'four-core ideal'


### Dynamic band allocation
dynamic_rate = 2823
dynamic_hyper_rate = 1523
dynamic_limit = 31000

set output 'images/mandelbrot-dynamic-8.png'
plot [0:8] [0:dynamic_limit] \
     'mandelbrot-dynamic.data' \
         with points linewidth 3 \
         title 'median render speed', \
     dynamic_rate * x with lines linewidth 3 title 'ideal'

set output 'images/mandelbrot-dynamic-16.png'
plot [0:16] [0:dynamic_limit] \
     'mandelbrot-dynamic.data' \
         with points linewidth 3 \
         title 'median render speed, dynamic', \
     'mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed, static', \
     x <= 4 ? dynamic_rate * x : dynamic_rate * 4 with lines linewidth 3 title 'four-core ideal', \
     x <= 8 ? dynamic_rate * x : dynamic_rate * 8 with lines linewidth 3 title 'eight-core ideal'


set output 'images/mandelbrot-dynamic-100.png'
set xtics autofreq
plot [0:100] [0:dynamic_limit] \
     'mandelbrot-dynamic.data' \
         with points linewidth 3 \
         title 'median render speed, dynamic', \
     'mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed, static', \
     x <= 4 ? dynamic_rate * x : dynamic_rate * 4 with lines linewidth 3 title 'four-core ideal', \
     x <= 8 ? dynamic_rate * x : dynamic_rate * 8 with lines linewidth 3 title 'eight-core ideal'


### Lock-free band allocation

atomic_limit = 33000

set output 'images/mandelbrot-lockfree-16.png'
plot [0:16] [0:atomic_limit] \
     'mandelbrot-dynamic.data' \
         with points linewidth 3 \
         title 'median render speed, dynamic', \
     'mandelbrot.data' \
         with points linewidth 3 \
         title 'median render speed, static', \
     'mandelbrot-atomic.data' \
         with points linewidth 3 \
         title 'median render speed, lock-free', \
     x <= 4 ? dynamic_rate * x : dynamic_rate * 4 with lines linewidth 3 title 'four-core ideal', \
     x <= 8 ? dynamic_rate * x : dynamic_rate * 8 with lines linewidth 3 title 'eight-core ideal'
