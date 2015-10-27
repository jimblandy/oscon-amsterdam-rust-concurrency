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
          Points('safety: no dangling pointers, no buffer overruns',
                 'performance: the programmer has control',
                 'concurrency: exploit multi-threaded machines')))

add(Slide('How does Rust accomplish those goals?',
          Points('statically typed language',
                 'ahead-of-time compiler (no JIT)',
                 'memory freed at well-defined points (no GC)',
                 u'“traits” capture common characteristics of types',
                 'generic functions everywhere, compiled by specialization',
                 'generic type parameters checked by traits')
          .reveal()))

add(Slide('Rust aims to compete with C++',
          Quote(u"""

          In general, C++ implementations obey the zero-overhead principle: What
          you don’t use, you don’t pay for. And further: What you do use, you
          couldn’t hand code any better.

          """, 'Bjarne Stroustrup'),
          Para("This is Rust's principle as well.").reveal()))

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

add(CodeCallout('Rust `enum` types, aka algebraic datatypes',
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

add(CodeCallout('A single-threaded grep', """

    fn grep(path: &str, pattern: &str) -> `Result<$()$2>`1 {
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

    fn grep(path: &str, pattern: &str) -> Result<()> {
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

with codecs.open('slides.html', 'w', 'utf-8') as f:
    pr.render(f)
