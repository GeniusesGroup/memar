# Khayyam - Programming Language
This language is ideal for developers that want a clean spoken code that can write most performance library and application with it!

## File extension
We choose .kh for files that have Khayyam language codes!

## Top Level Keyword

### type -> data-types
Khayyam force you naming a type with one of below type as `type {Name} {Type}`
- [Digital computing]()
    - ptr as [Pointer]() to point specific memory location. Size depend on CPU architecture(32||64||...bit)! e.g. `type buf ptr`
    - bool to work on any boolean logical! Usually 1 octet(byte-8bit) size! It can hold value 1 or 0 as true or false. e.g. `type ok bool`
- Numerical indicate by `[x]NS` e.g. `type testNum [3]N`
    - x can be
        - fixed size of number in octet||byte! Can be any natural number (x>0)!
        - "x" itself just in function argument to indicate it can get any number size. Can't use in structure type
    - NS can any [Number systems](https://en.wikipedia.org/wiki/Number#Main_classification):
        - N as [Natural](https://en.wikipedia.org/wiki/Natural_number)
        - W as [Whole]()
        - Z as [Integer](https://en.wikipedia.org/wiki/Integer) also know as signed number, ...
        - Q as [Rational](https://en.wikipedia.org/wiki/Rational_number) also knows as float, ...
        - R as [Real](https://en.wikipedia.org/wiki/Real_number)  also know as Irrational, Fractional
        - C as [Complex](https://en.wikipedia.org/wiki/Complex_number)
- Array indicate by this syntax `[x][x]...T` and it is fixed size! e.g. `type testArray [256][1]N`
- structure indicate by `struct{...}` that has some other types inside themself!

### const -> Constant
const, unlike other languages, is not very hard immutable data! Dev can change in runtime but unlike var, it will change binary code and don't need to get it by memory call! Compiler and runtime just let to change the value with the same memory size!

### var -> Variable
Like other programming languages, var keyword uses to store data in any mutable device. But unlike other, vars declare inside a function  store 

### func -> Function
Two type function supported:
- func name(args) (returns) >> pure standalone function
- func (type receiver) name(args) (returns) >> method function

## Operators
https://en.wikipedia.org/wiki/Operators_in_C_and_C%2B%2B
https://maxbase.org/my-programming-language/et-operator-precedence-en/
### Arithmetic
Arithmetic can just be done on bool, Numerical and array type! In Numerical if either operand is not the same number system, It always converts to a higher system range e.g. if one of the operands is [1]N and the other is [2]W, the result type is [2]W!
### Comparison or Relational
### Logical
### Bitwise
### Compound assignment
### Member and pointer
### Other
### Precedence

## Runtime
We offer very simple but with some unique logic!

### Change logic in runtime!
You can write code to change binary code in runtime!

## Rules
- The function body can omit in write code and add by compiler plugins as know code generation!
- Public of the first-class keyword indicates by a capital letter of identifier word and vice versa! Khayyam doesn't offer any specific keyword for this purpose like Go language!

## Not implement features!!?
In this part, we say why not choose something that be real in some other programming languages!

### Packaging
We can't decide yet to offer any package some files code!

### GC (Garbage Collection)


### Interface
We can't decide yet that Khayyam must support interface type!!

### Tuples
Tuples are implemented by two dynamic and static type languages!
- In a dynamic language, tuples implement unsafe structures that allocate by the runtime and have a performance penalty for the app because we use runtime for developing or compiling phase!!
- In a static language, tuples implement safe structures that just don't have internal names! But it is duplicate work, more learning curve and adds more confusing situation just lazy developer to not indicate names!!

### Type Inference
Khayyam don't support type inference and also you can't assign to var before you decare it!
```
var x = 41      >> var x [1]W = 41
var y = 3.14    >> var y [32]Q = 3.14
```

### Loop
We think loop can implement easily by `goto` instead of while, for, do, ...!!

### Dependency Management
We don't offer any version control for your codes, So we must not offer any dependency management too! 

## Keyword in a glance
| type          | Logical           | ***********       | ***********       | ***********       |
| :---:         | :---:             | :---:             | :---:             | :---:             |
| ptr           | if                |                   |                   |                   |
| bool          | else if           |                   |                   |                   |
| struct        | else              |                   |                   |                   |
| const         | true              |                   |                   |                   |
| var           | false             |                   |                   |                   |
| func          | goto              |                   |                   |                   |
|               |                   |                   |                   |                   |
|               |                   |                   |                   |                   |

## Inspired of
### Languages
These languages inspirations don't mean just about get good idea but mean drop bad idea from these and not implement them!
- [C]()
- [D](https://dlang.org)
- [Go]()
- [Rust]()
- [Spiral](https://github.com/mrakgr/The-Spiral-Language)
### Articles
- https://pingcap.com/blog/early-impressions-of-go-from-a-rust-programmer/
- http://www.linux-kongress.org/2009/slides/compiler_survey_felix_von_leitner.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.143.4688

## Khayyam word meaning
[Omar Khayyam](https://en.wikipedia.org/wiki/Omar_Khayyam) was a Persian mathematician, astronomer, philosopher, and poet.
