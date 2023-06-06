# Khayyam - Programming Language
This language is ideal for developers that want a clean spoken code that can write most performance library and application with it.

## File extension
We choose .kh for files that have Khayyam language codes.

## Top Level Keyword

### include
Khayyam allow developers to include multi file by use `include ()`, so use `include` more than once in a file is not legal.
Khayyam use `include ({name} {addr})` keyword e.g. 
- `include ("/lib/error")` to include all exported types, vars, functions, ... without need indicate package name to call them e.g. `fn test() error {}` that `error` can be type, ... indicate in included file.
- `include ({NewError} "/lib/error)"` to include just `NewError` e.g. `var ErrBadThing = NewError("oops...") `

### import
Khayyam use `import ({name} {addr})` keyword e.g. `import (json "../json)"`  to import other code file to local one. import desire file and use needed logic by this way e.g. `json.Marshal()`
- Khayyam allow developers to import multi files by use `import ()`, so use `import` more than once in a file is not legal.

### type -> data type
Khayyam force you naming a type with one of below type as `type {Name} [Type]`. `Type` can be one of below items.
- ptr as [Pointer]() to point specific memory location as [Digital computing](). Size depend on CPU architecture(32||64||...bit). e.g. `type buf ptr`
- `Function` can indicate by 
- `Interface`: We can't decide yet that Khayyam must support interface type in old fashion way.
- Any other `structure`

Any library use above fundamental types and implement any types like:
- `bool` to work on any boolean logical. It will usually cost 8bit memory. It can hold value 1 or 0 as true or false. e.g. `type ok Bool` if it is included to this package or file.
- Numerical can indicate by e.g. `type testNum [x][NS]`. They can `Init` by any natural number (x>0) to indicate fixed array length in bit that number can hold. `x` itself just to indicate it can get any length. library decide to how handle this type of logic e.g. with any hardware accelerator or do many logic in large length.   
Libraries can decide to implement `Arithmetic` rule. This rule can be done on `bool`, `Numerical` and `array(list)` type. In Numerical if either operand is not the same number system, It always converts to a higher system range e.g. if one of the operands is [1]N and the other is [2]W, the result type is [2]W.
    - NS can any [Number systems](https://en.wikipedia.org/wiki/Number#Main_classification):
        - N as [Natural](https://en.wikipedia.org/wiki/Natural_number) is any number > 0
        - W as [Whole]() is any number >= 0
        - Z as [Integer](https://en.wikipedia.org/wiki/Integer) also know as signed number is any number <>= 0
        - Q as [Rational](https://en.wikipedia.org/wiki/Rational_number) also knows as decimal, float, ...
        - R as [Real](https://en.wikipedia.org/wiki/Real_number)  also know as Irrational, Fractional
        - C as [Complex](https://en.wikipedia.org/wiki/Complex_number)
- `Array` or `List` or `List of List` or ... can indicate by this syntax `[List]` and it is fixed size. e.g. `type testArray List`, `type emails emails` and can `Init` by any number `email.Init(256, 8)`

### st -> structure as encapsulation-pattern
- structure indicate by `struct{...}` that has some other types inside itself.

### self -> point to other members in the capsule!
- fn (type receiver) name(args) (returns) >> method function

### cn -> Constant
const, unlike other languages, is not very hard immutable data. Dev can change in runtime but unlike var, it will change binary code and don't need to get it by memory call. Compiler and runtime just let to change the value with the same memory size.

### vr -> Variable
Like other programming languages, var keyword uses to store data in any mutable device. But unlike other, vars declare inside a function  store 

### fn -> Function
Two type function supported:
- fn name(args) (returns) >> pure standalone function


### rt -> return
- Just use to indicate return in body of a function.
- Not need to indicate on end of any functions.
- It is pure keyword and must end with [commands break](#Commands_Break) style so dev can't use like "return 0".

### Commands Break
each command must end with new line or ';' 

## Operators
https://en.wikipedia.org/wiki/Operators_in_C_and_C%2B%2B
https://maxbase.org/my-programming-language/et-operat]Nor-precedence-en/

### Comparison or Relational
### Logical
### Bitwise
### Compound assignment
### Member and pointer
### Other
### Precedence

## Rules
### Inline Function
- Inline function return const as declare const globally. Below codes are same when compile them.
```Khayyam
fn fixedLen() (fixedSize Natural) {
    const fixedSize Natural.Init(326)
    return fixedSize
}

const fixedLen Natural.Init(326)
```

### getter and setter methods
For each structure field developer must define global get & set methods, otherwise compiler throw compile error if any read||write be in codes.

## Runtime
We offer very simple but with some unique logic

### Change logic in runtime
You can write code to change binary code in runtime.

## Rules
- The function body can omit in write code and add by compiler plugins as know code generation.
- Public of the first-class keyword indicates by a capital letter of identifier word and vice versa. Khayyam doesn't offer any specific keyword for this purpose like Go language.

## Not implement features!?
In this part, we say why not choose something that be real in some other programming languages.

### Packaging
We can't decide yet to offer any package some files code.

### GC (Garbage Collection)

### Tuples
Tuples are implemented by two dynamic and static type languages.
- In a dynamic language, tuples implement unsafe structures that allocate by the runtime and have a performance penalty for the app because we use runtime for developing or compiling phase.
- In a static language, tuples implement safe structures that just don't have internal names. But it is duplicate work, more learning curve and adds more confusing situation just lazy developer to not indicate names.

### Type Inference
Khayyam don't support type inference and also you can't assign to var before you decare it.
```
var x = 41      >> var x [1]W = 41
var y = 3.14    >> var y [32]Q = 3.14
```

### Loop
We think loop can implement easily by `goto` instead of while, for, do, ...

### Dependency Management
We don't offer any version control for your codes, So we must not offer any dependency management too.

## Keyword in a glance
| type          | Logical           | ***********       | ***********       | ***********       |
| :---:         | :---:             | :---:             | :---:             | :---:             |
| ptr           | if                |                   |                   |                   |
| bool          | else if           |                   |                   |                   |
| struct        | else              |                   |                   |                   |
| const         | true              |                   |                   |                   |
| var           | false             |                   |                   |                   |
| fn          | goto              |                   |                   |                   |
|               |                   |                   |                   |                   |
|               |                   |                   |                   |                   |

## Inspired of
### Languages
These languages inspirations don't mean just about get good idea but mean drop bad idea from these and not implement them.
- [C](https://en.wikipedia.org/wiki/C_(programming_language))
- [D](https://dlang.org)
- [Go](https://golang.org/)
- [Rust](https://www.rust-lang.org/)
- [Spiral](https://github.com/mrakgr/The-Spiral-Language)

### Articles
- https://pingcap.com/blog/early-impressions-of-go-from-a-rust-programmer/
- http://www.linux-kongress.org/2009/slides/compiler_survey_felix_von_leitner.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.143.4688

## Khayyam word meaning
[Omar Khayyam](https://en.wikipedia.org/wiki/Omar_Khayyam) was a Persian mathematician, astronomer, philosopher, and poet.
