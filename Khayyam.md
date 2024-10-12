# Khayyam - Programming Language
This language is ideal for developers that want a clean spoken code that can write most performance library and application with it.

## File extension
We choose .kh for files that have Khayyam language codes.

## Top Level Keyword

### type
Type or data type is a subdivision of a particular kind of things. All things MUST define in below shape to understand by Khayyam compiler.
```khayyam
type {name} [Type] [subtype defined value]

type (
    {name1} [Type1] [subtype defined value]
    {name2} [Type2] [subtype defined value]
)
```

### Types
- **Include**: Khayyam allow developers to include multi file by use `in`.
    - use `include` more than once in a file is not legal.
    - Khayyam use `type {name} in {addr}` keyword e.g. 
        - `type * in "/lib/error"` to include all exported types, vars, functions, ... without need indicate package name to call them e.g. `fn test() error {}` that `error` can be type, ... indicate in included file.
        - `type NewError in "/lib/error"` to include just `NewError` e.g. `var ErrBadThing = NewError("oops...")`

- **Import**: Khayyam allow developers to imports other file codes by use `im`.
    - Khayyam allow developers to import multi files by use `import ()`, so use `import` more than once in a file is not legal.
    - Khayyam use `type {name} im {addr}` keyword e.g. `type json im "memar/json"` to import other code file to local one. import desire file and use needed logic by this way e.g. `json.Marshal()`

- **Function**: Khayyam allow developers to indicate functions by use `fn`.   
Two type function supported:
    - type {name} fn (args) (returns) >> pure standalone function

- **Abstraction**: Khayyam allow developers to indicate abstraction by use `ab`.    
We don't introduce any other syntax for Polymorphism(generic) like Golang(`[{name} {TYPE}]`) for other types. Compiler decide smartly to do it by runtime(Golang interface) or compile time(Golang generic).

- **structure**: Khayyam allow developers to indicate encapsulation-pattern by use `st`.
    - structure indicate by `type {name} st {...}` that has some other types inside itself.
    - Inside a structure can omit `type` keyword in each line to indicate fields.

- **Constant**: Khayyam allow developers to indicate constant by use `cn`.   
const, unlike other languages, is not very hard immutable data. Dev can change in runtime but unlike var, it will change binary code and don't need to get it by memory call. Compiler and runtime just let to change the value with the same memory size.

- **Variable**: Khayyam allow developers to indicate constant by use `vr`.   
Like other programming languages, `vr` keyword uses to store data in any mutable device. But unlike other, variables declare inside a function store.

### sf -> self as point to other members in the capsule!
- fn (type receiver) name(args) (returns) >> method function

### rt -> return
- Just use to indicate return in body of a function.
- Not need to indicate on end of any functions.
- It is pure keyword and must end with [commands break](#Commands_Break) style so dev can't use like "return 0".

### Commands Break
each command must end with new line or ';'

## Operators
Since we have no primitive types in language syntax, We don't need to provide any operators!

## Rules
### Inline Function
- Inline function return const as declare const globally. Below codes are same when compile them.
```Khayyam
fn fixedLen() (fixedSize integer.U16) {
    fixedSize.FromASCII(326)
    return
}

const fixedLen integer.U16.FromASCII(326)
```

### getter and setter methods
For each structure field developer must define global get & set methods, otherwise compiler throw compile error if any read||write directly to fields be in codes.

## Runtime
We offer very simple but with some unique logic

### Change logic in runtime
You can write code to change binary code in runtime.

## Rules
- The function body can omit in write code and add by compiler plugins as know code generation.
- Public of the first-class keyword indicates by a capital letter of identifier word and vice versa. Khayyam doesn't offer any specific keyword for this purpose like Go language.

## Not implement features!?
In this part, we say why not choose something that be real in some other programming languages.

### Methods Overloading
It seems we need this feature if we want to have very simple generic and polymorphism.   
Due to Khayyam not support primitive types, All disadvantages disappear and JUST advantages will shine.

### Method overriding
Method overloading is a compile-time polymorphism. Method overriding is a run-time polymorphism. CAN provide runtime feature when not provide rich runtime??

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
var x = 41      >> type x vr whole.W8.FromString(41)
var y = 3.14    >> type y vr rational.R32.FromString(3.14)
```

### Loop
We think loop can implement easily by `goto` instead of `while`, `for`, `do`, ... if and just if `Iterator` interface not implement by desire type.

### Dependency Management
We don't offer any version control for your codes, So we must not offer any dependency management too.

## Keyword in a glance
| type          | Logical           | ***********       | ***********       | ***********       |
| :---:         | :---:             | :---:             | :---:             | :---:             |
| type          | if                |                   |                   |                   |
| fn            | else if           |                   |                   |                   |
| st            | else              |                   |                   |                   |
| cn            |                   |                   |                   |                   |
| vr            |                   |                   |                   |                   |
|               | goto              |                   |                   |                   |
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
