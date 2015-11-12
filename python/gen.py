# -*- coding: utf-8 -*-
import codecs

from slides import *

pr = Presentation('Concurrency First in Rust', 'Jim Blandy')
add = pr.add

add(Cover('Concurrency First in Rust',
          'Jim Blandy <jimb@mozilla.com> @jimblandy',
          'images/cover.png'))

add(BigPoint("""

    Rust makes concurrent designs easier to explore, implement, and maintain, by
    guaranteeing the absence of data races and memory corruption.

    """))

add(Slide('Why Rust?',
          Points('*safety*: no dangling pointers, no buffer overruns',
                 '*performance*: the programmer has control',
                 '*concurrency*: exploit multi-threaded machines')))

add(Slide('How does Rust accomplish those goals?',
          Points('statically typed language',
                 'ahead-of-time compiler (no JIT)',
                 'memory is freed at well-defined points (no GC)',
                 u'*traits* capture common characteristics of types',
                 'generic functions used everywhere, compiled by specialization',
                 'generic type parameters checked by traits')
          .reveal()))

add(Slide('Rust aims to compete with C++',
          Quote(u"""

          In general, C++ implementations obey the zero-overhead principle: What
          you don’t use, you don’t pay for. And further: What you do use, you
          couldn’t hand code any better.

          """, u'—Bjarne Stroustrup'),
          Para("Rust adopts this principle as well.").reveal()))

add(CodeCallout('A simple Rust function', """

    fn gcd(mut n: `u64`1, mut m: `u64`1) -> `u64`1 {
        assert!(n != `0`3 && m != `0`3);
        while m != `0`3 {
            if m < n {
                `let t = m;`2 m = n; n = t;
            }
            m = m % n;
        }
     `   n   `4
    }
"""))

add(CodeCallout('Rust `enum` types, aka algebraic types',
                """

                   enum Option`<T>`1 {
                       `None`2,
                       `Some(T)`3,
                   }

                """))

add(CodeCallout('A safe division function',
                """

    fn safe_div(n: i32, d: i32) -> `Option<i32>`1 {
        if d == 0 {
            return `None`2;
        }
        return `Some(n / d)`3;
    }

                """))

add(CodeCallout('A safe division function', """

        fn safe_div(n: i32, d: i32) -> Option<i32> {
            if d == 0 {
                return `None`2;
            }
            return `Some(n / d)`4;
        }

        `match`1 safe_div(24, 3) {
            `None`2 => `println!("No quotient.")`3,
            `Some(v)`4 => `println!("quotient is {}", v)`5
        }

                """))

add(CodeCallout('Results from fallible operations', """

    #[must_use]
    enum Result`<T, E>`1 {
        `Ok(T)`2,
        `Err(E)`3,
    }
                    """))

add(CodeCallout('Shareable references and mutable references', """
    let i = 42;
    let shareable = `&i`1;

    let mut j = 1729;
    let mutable = `&mut j`2;
"""))

add(CodeCallout('A single-threaded grep', """

    fn grep(path: &str, pattern: &str) -> `std::io::Result<$()$2>`1 {
        let file = `try!`3(File::open(path));
        let buffered = `BufReader::new(file);`4
        `for line in buffered.lines()`5 {
            let line = `try!`6(line);
            if `line.contains(pattern)`7 {
                println!("{}", line);
            }
        }
        `return Ok(());`8
    }

    """))

add(CodeCallout('A single-threaded grep', """

    fn grep(path: &str, pattern: &str) -> std::io::Result<()> {
        let file = try!(File::open(path));
        let buffered = BufReader::new(file);
        for line in buffered.lines() {
            let line = try!(line);
            if line.contains(pattern) {
                println!("{}", line);
            }
        }
        `Ok(())`0
    }

    """))

add(CodeCallout('A single-threaded grep', """

    `for file in args`1 {
        match `grep(&file, &pattern)`2 {
            `Err(e)`3 => {
                writeln!(std::io::stderr(),
                         "Error searching {}: {}", file, e)
                    .unwrap();
            },
            `Ok(_) => ()`4
        }
    }

    """))

add(Slide("Let's do it concurrently!"))

add(Slide('Thread Pools',
          Picture('images/thread-pool.svg')))

add(Slide('Channels',
          Picture('images/channels.svg')))
add(Slide('Forbidding data races',
          Para('Data races can only occur when data is both shared and mutable. So you can have either:'),
          Para('Sharing without mutability').center(),
          Para('*or*').center(),
          Para('Mutability without sharing').center()))

add(Slide('Forbidding data races',
          Points("If you send a mutable value on a channel, you must give up your pointers to it.",
                 "You can send pointers to immutable values to other threads, and both share access."),
          Para("We'll see examples of both.").reveal()))

add(BigPicture('images/cargo-home-page.png'))
add(BigPicture('images/cargo-search-results.png'))
add(BigPicture('images/cargo-scoped_threadpool.png'))
add(BigPicture('images/cargo-scoped_threadpool-dependency.png'))

add(CodeCallout('The `Cargo.toml` file', """
               [package]
               name = "pgrep"
               version = "0.1.0"
               authors = ["Jim Blandy <jimb@red-bean.com>"]

               [dependencies]
               `scoped_threadpool = "0.1.6"`1
               """))

add(BigPicture('images/cargo-build-pgrep.png'))

add(CodeCallout('A multi-threaded grep', """

    fn grep(path: &str, pattern: &str,
            `results: &Sender<Message>`1) -> Result<()>
    {
        let file = try!(File::open(path));
        let buffered = BufReader::new(file);
        for line in buffered.lines() {
            let line = try!(line);
            if line.contains(pattern) {
                `results.send(Message::Hit(line)).unwrap();`2
            }
        }
        return Ok(());
    }

    """))

add(CodeCallout('The grep message type', """

    enum Message<`'a`3> {
        `Hit(String),`1
        `Done(&$'a$3 str, Result<()>),`2
    }

    """))

add(CodeCallout('A multi-threaded grep', """

    fn grep(path: &str, pattern: &str,
            results: &Sender<Message>) -> `Result<()>`1
    {
        let file = `try!`1(File::open(path));
        let buffered = BufReader::new(file);
        for line in buffered.lines() {
            let line = `try!`1(line);
            if line.contains(pattern) {
                results.send(`Message::Hit(line)`0).unwrap();
            }
        }
        return `Ok(())`1;
    }

    """))

add(CodeCallout('A multi-threaded grep', """

    let mut pool = `scoped_threadpool::Pool::new(8);`1
    `let files : Vec<String> = args.collect();`2
    let (results_tx, results_rx) = channel();

    """))

add(CodeCallout('A multi-threaded grep', """

    // single-threaded version
    `for file in args`0 {
        match grep(&file, &pattern) {
            Err(e) => {
                writeln!(std::io::stderr(),
                         "Error searching {}: {}", file, e)
                    .unwrap();
            },
            Ok(_) => ()
        }
    }

    """))

add(CodeCallout('A multi-threaded grep', """

    let mut pool = scoped_threadpool::Pool::new(8);
    `let files : Vec<String> = args.collect();`0

    `pool.scoped`3(`|scope| { ... }`4);

    """))

add(CodeCallout('a multi-threaded grep', """

    pool.scoped(|scope| {
        let `receiver`4;
        {
            let `($sender$3, recv)`2 = `std::sync::mpsc::channel()`1;
            `receiver`4 = recv;

            ... enqueue search tasks ...
        }

        for message in `receiver`4 {
            ... process results ...
        }
    })

    """))

add(CodeCallout('enqueuing search tasks', """
    `for file in &files`1 {
        let pattern_ref = &pattern;
        let sender_clone = `sender.clone()`2;
        `scope.execute`3(`move`4 `||`5 {
            let `result`7 = `grep(file, pattern_ref, &sender_clone)`6;
            sender_clone.send(`Message::Done(file, result)`8)
                .expect("receiver died");
        });
    }
    """))

add(CodeCallout('processing search results', """
    for message in `receiver`1 {
        `match message`2 {
            `Message::Hit(line)`3 => { println!("{}", line); }
            `Message::Done(file, result)`4 => {
                `if let Err(e) = result`5 {
                    writeln!(std::io::stderr(),
                             "Error searching {}: {}", file, e)
                        .unwrap();
                }
            }
        }
    }
    """))

add(Slide('It works!'))

add(Slide("Looks the same as C++.",
          Para("Yes; Rust isn't a new paradigm for concurrency.").reveal(),
          Para("... but this program ran correctly the first time it compiled.").reveal()))

add(Slide('What does this show?',
          Points("Worker pools can manage large tasks with a bounded number of threads.",
                 "Channels are a convenient way to carry messages between threads.",
                 "We can throw pointers around between threads without fear.",
                 u"Concurrent Rust programs are still non-deterministic, but the non-determinism occurs only at operations designed for it—not just anywhere.").reveal()))

for i in xrange(0, 9):
    add(Slide('A bit of pure math',
              Picture('images/squaring-{}.svg'.format(i))))

add(Slide('a variation',
          Code("""
              fn m(c: f64) {
                  let z = 0;
                  loop {
                      z = z*z + c;
                  }
              }
              """),
          Para(u"Unless -2 ≤ c ≤ 0.25, z escapes.").reveal()))

add(Slide('a Complex variation',
          Code("""
              fn m(c: Complex<f64>) {
                  let z = Complex { re: 0., im: 0. };
                  loop {
                      z = z*z + c;
                  }
              }
              """),
          Para(u"... it's complicated.").reveal()))

# Generated with:
# ./target/release/mandelbrot ~/rust/amsterdam/images/mandelbrot.png 1024x768 -2.75,1.20 1.25,-1.80
add(BigPicture('images/mandelbrot.png'))

add(CodeCallout('the Mandelbrot escape calculation', """
    fn escapes(c: Complex<f64>, `limit: u32`2) -> `Option<u32>`1 {
        let mut z = Complex { re: 0.0, im: 0.0 };
        `for i in 0..limit`2 {
            z = z*z + c;
            `if z.norm_sqr() > 4.0`3 {
                return Some(i);
            }
        }

        `return None;`4
    }
    """))

add(CodeCallout('mapping pixels to points', """
    fn pixel_to_point(`bounds: (usize, usize)`1,
                      `pixel:  (usize, usize)`2,
                      `ul: (f64, f64)`3,
                      `lr: (f64, f64)`4)
        -> `(f64, f64)`5
    {
        let (width, height) = (`lr.0`6 - `ul.0`6,
                               `ul.1`6 - `lr.1`6);
        (`ul.0`6 + `pixel.0`6 `as f64`7 * width  / `bounds.0`6 `as f64`7,
         `ul.1`6 - `pixel.1`6 `as f64`7 * height / `bounds.1`6 `as f64`7)
    }
    """))

add(CodeCallout('rendering the set', """
    fn render(pixels: `&mut [u8]`1, bounds: (usize, usize),
              ul: (f64, f64), lr: (f64, f64)) {
       `for r in 0 .. bounds.1`2 {
          `for c in 0 .. bounds.0`3 {
             let pt = `pixel_to_point(bounds, (c, r), ul, lr)`4;
             let pt = `Complex { re: pt.0, im: pt.1 }`5;
             `pixels[r * bounds.0 + c]`9 =
                match `escapes(pt, 255)`6 {
                   `None => 0`7,
                   `Some(count) => 255 - count as u8`8
                };
          }
       }
    }
    """))

add(CodeCallout('writing the image file', """
    fn write_bitmap(filename: &str,
                    pixels: &[u8],
                    bounds: (usize, usize))
        -> Result<()>
    {
        let output = try!(`File::create(filename)`1);
        let encoder = `PNGEncoder::new(output)`2;
        try!(`encoder.encode`3(pixels,
                            bounds.0 as u32, bounds.1 as u32,
                            `ColorType::Gray(8)`4));
        Ok(())
    }
    """))

add(Slide('banding the Mandelbrot',
          Picture('images/sliced-mandelbrot.svg')))

add(CodeCallout('banded driver', """
    let bands `: Vec<_>`3
        = `pixels.chunks_mut`1(`band_rows * bounds.0`2).collect();
    `crossbeam::scope`4(|scope| {
        for `(i, band)`6 in `bands.into_iter()`5.`enumerate()`6 {
            let top = band_rows * i;
            let height = band.len() / bounds.0;
            let band_bounds = (bounds.0, height);
            let (band_ul, band_lr) = ...;
            `scope.spawn`7(move || {
                `render(band, band_bounds, band_ul, band_lr)`8;
            });
        }
    });
    """))

add(GnuPlot('banded Mandelbrot speedup', 'images/mandelbrot-8-no-ideal.png'))
add(GnuPlot('banded Mandelbrot speedup', 'images/mandelbrot-8.png'))
add(GnuPlot('banded Mandelbrot speedup', 'images/mandelbrot-16.png'))
add(GnuPlot('banded Mandelbrot speedup', 'images/mandelbrot-100.png'))

add(Slide('Not all bands are the same',
          Picture('images/sliced-mandelbrot.svg')))

add(GnuPlot('banded Mandelbrot speedup', 'images/mandelbrot-100.png'))
add(GnuPlot('banded Mandelbrot speedup', 'images/mandelbrot-1000.png'))

add(Slide('dynamic band allocation',
          Picture('images/dynamic-sliced-mandelbrot.svg')))

add(CodeCallout('Dynamically allocated bands', """
    let bands =
        `Mutex::new`2(`pixels.chunks_mut`1(band_rows * bounds.0)
                   .enumerate());
    crossbeam::scope(|scope| {
        `for i in 0..8`3 {
            scope.spawn(|| { ... });
        }
    });
    """))

add(CodeCallout('Dynamically allocated bands', """
    scope.spawn(|| {
        loop {
            match {
                let mut `guard`2 = `bands.lock().unwrap()`1;
                `guard.next()`3
            }
            {
                `None => { return; }`4
                `Some((i, band)) => { render(band, ...); }`5
            }
        }
    });
    """))

add(GnuPlot('dynamic band allocation', 'images/mandelbrot-dynamic-8.png'))
add(GnuPlot('dynamic band allocation', 'images/mandelbrot-dynamic-16.png'))
add(GnuPlot('dynamic band allocation', 'images/mandelbrot-dynamic-100.png'))

add(BigPoint("Something is still slightly unsatisfying..."))

add(CodeCallout('A lock-free chunk iterator', """
    use std::sync::atomic::{`AtomicUsize`!, Ordering};
    use std::sync::atomic::Ordering::*;

    `struct AtomicChunksMut`1<`'a`5, T: `'a`5> {
        `slice: &$'a$5 [T],`2
        `step: usize,`3
        `next: AtomicUsize`4
    }
    """))

add(CodeCallout('A lock-free chunk iterator', """
    `impl`1<'a, T> `AtomicChunksMut`1<'a, T> {
        pub `fn new`2(...) { ... }
        unsafe `fn next`3(...) { ... }
    }
    """))

add(CodeCallout('A lock-free chunk iterator', """
    impl<'a, T> AtomicChunksMut<'a, T> {
        `pub fn new`2(slice: &'a mut [T], step: usize)
                  -> AtomicChunksMut<'a, T> {
            `AtomicChunksMut {             `3
            `   slice: slice,              `3
            `    step: step,               `3
            `    next: $AtomicUsize::new$4(0) `3
            `}                             `3
        }
        ...
    }
    """))

add(CodeCallout('A lock-free chunk iterator', """
    `unsafe`D fn next(&self) -> `Option<(usize, $&'a mut [T]$C)>`1 {
        `loop`B {
            let cur = `self.next.load(SeqCst)`3;
            if `cur == self.slice.len()`4 { return None; }
            let end = `min(cur + self.step, self.slice.len())`5;
            if `self.next`7.`compare_and_swap`6(`cur`7, `end`8, SeqCst)
               `== cur`9 {
               return `Some((cur / self.step,                   `A
                      `      $transmute$C(&self.slice[cur..end])));`A
            }
        }
    }
    """))

add(CodeCallout('A lock-free chunk iterator', """
    impl<'a, 'b, T> `Iterator`1 for `&'b AtomicChunksMut<'a, T>`3 {
        `type Item`1 = (usize, &'a mut [T]);
        `fn next`1(&mut self) -> `Option<Self::Item>`2 {
            unsafe { `(*self).next()`4 }
        }
    }
    """))

add(CodeCallout('Lock-free dynamic bands', """
    let bands = `AtomicChunksMut::new`1(&mut pixels, bounds.0);
    crossbeam::scope(|scope| {
        `for i in 0..8`2 {
            scope.spawn(|| {
                `for (i, band) in $&bands$2`3 {
                    ...
                    render(band, ...);
                }
            });
        }
    });
    """))

add(GnuPlot('dynamic band allocation', 'images/mandelbrot-lockfree-16.png'))

add(Slide('Summing up',
          Points('Message-passing works',
                 'Mutexes work.',
                 'Atomics work.',
                 'Never a data race, if you stick to safe code.',
                 "Rust's concurrency primitives are open-ended: when you know what you're doing, you can build new safe primitives from unsafe implementations.",
                 "Benchmark, and you learn cool stuff.").reveal()))

for i in xrange(5):
    add(BigPicture('images/subsets-{}.svg'.format(i)))



with codecs.open('slides.html', 'w', 'utf-8') as f:
    pr.render(f)

# Local Variables:
# compile-command: "cd ~/rust/amsterdam && python python/gen.py"
# End:
