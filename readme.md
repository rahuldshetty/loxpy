
# LoxPy <!-- {docsify-ignore-all} -->

> Dynamically-typed interpreter programming language written in Python. This project is based out of a  book called [Crafting Interpreters](https://craftinginterpreters.com) which is about building your own programming language. This is my second attempt to build a custom programming language. Highly recommend the book for beginners who want to get into Compiler designing.

## Features

- Easy to Code
- High Level interpreter language
- Object Oriented Programming
- Dynamically-Typed
- Dynamic memory allocation & Garbage collector using Python's GC system.
- Free & Open Source

# Sample

```
// Functions
fn hello(name){
    print "Hello " + name;
}

hello("World!"); // Prints Hello World!


// Operators
var a = 10;
var b = 20;

print a+b;
print a-b;
print a*b;
print b / a;

for(var i = 1; i <= 10; i = i + 1){
    print i;
    if (i == 5){
        break;
    }
}


// Class & Objects
class Doughnut {
  fn cook() {
    print "Fry until golden brown.";
  }
}

class BostonCream (Doughnut) {
  fn cook() {
    super.cook();
    print "Pipe full of custard and coat with chocolate.";
  }
}

BostonCream().cook();

```

## Contributing

If you would like to contribute to the project or report any bugs, feel free to raise this in the Github Issue [tracker](https://github.com/rahuldshetty/talion/issues).