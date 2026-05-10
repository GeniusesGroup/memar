# Khayyam - Programming Language
This language is ideal for developers that want a clean spoken code that can write most performance library and application with it.

## File extension
We choose .kh for files that have Khayyam language codes.

## Top Level Keyword

### **type**
Type or data type is a subdivision of a particular kind of things. All things MUST define in below shape to understand by Khayyam compiler.
```khayyam
tp {name} [Type] [subtype defined value]

tp (
    {name1} [Type1] [subtype defined value]
    {name2} [Type2] [subtype defined value]
)
```

#### **Types**
- **Include**: Khayyam allow developers to include other packages(multi files) as top level encapsulation-pattern by use `in`.
  - Khayyam use `tp {name} in {addr}` keyword e.g. 
    - `tp * in "/lib/error"` to include all exported types, vars, functions, ... without need indicate package name to call them e.g. `fn test() error {}` that `error` can be type, ... indicate in included file.
    - `tp NewError in "/lib/error"` to include just `NewError` e.g. `var ErrBadThing = NewError("oops...")`

- **Import**: Khayyam allow developers to imports other packages(multi files) as top level encapsulation-pattern by use `im`.
  - Consumers will set name for a `package` that import, so Producers don't need to indicate or naming in producing side.
  - Khayyam use `tp {name} im {addr}` keyword e.g. `tp json im "memar/json"` to import other code file to local one. import desire file and use needed logic by this way e.g. `json.Marshal()`

- **Capsule**: Khayyam allow developers to indicate first level encapsulation-pattern by use `cp`.
  - Capsule structure indicate by `tp {name} cp {...}` that has some other data types inside itself.
  - Inside a structure can omit `tp` keyword in each line to indicate fields.
  - Khayyam way only allow access to inner data types via methods(functions). there is no data fields to expose.

- **Method**: Khayyam allow developers to indicate methods for capsules by use `mt`.
  - `tp {name} mt ({capsule}) ({args}...) ({returns}...) {}`
  - Devs MUST separate `capsule`, `args` and `returns` by use `()` to indicate all of them even it is empty. We know that all of them is same in underlying layers and this rule is just to improve code readability.
  - Devs CAN write pure standalone function in this way, there is no limitation.
  - Dev can use any naming for capsule naming, BUT suggest use `self` as base point to other members in the capsule.
    - `tp Set mt (self Key) (key string_p.String) (err error_p.Error) {}`

- **Abstraction**: Khayyam allow developers to indicate abstraction by use `ab`.
  - `tp {name} ab {}`
  - Abstractions MUST use other abstractions as arguments or returns not other `capsule`s
  - We don't introduce any other syntax for Polymorphism(generic) like Golang(`[{name} {TYPE}]`) for other types. Compiler decide smartly to do it by runtime(Golang interface) or compile time(Golang generic).

### **Variable**:
- Khayyam allow developers to indicate variables by use `vr`.   
- Like other programming languages, `vr` keyword uses to store data in any mutable device. 
- Variables CAN declare in any encapsulation level as packages and methods and of course functions bodies.
- Compiler MUST inline variables as much as possible like immutable variables(constant in other language like Go).

### Logical
- **GOTO**: GOTO use to fly to desire location in a process. Some known labels:
  - loop: find loop by `{}`
  - end: find by `{}`
  - next: it is like `continue` in `switch` in other languages.
  - return
      - Just use to indicate return in body of a function.
      - Not need to indicate on end of any functions.
      - It is pure keyword and must end with [commands break](#Commands_Break) style so dev can't use like "return 0".
      - 
- **Commands Break**: each command must end with new line or ';'

## Compiler
- Compiler provide `compiler` package that developers can use in coding and let compiler know that must decide.
```khayyam
tp Set mt (self Key) (key STR) () {
	if key.CharacterEncoding() != ascii.CharacterEncoding {
		compiler.Log.Fatal("Linter MUST notify developers not call this method with string other than ASCII")
	}
	self.CopyFrom(key)
}
```
- The function body can omit in write code and add by compiler plugins as know code generation.
- Public of the first-class keyword indicates by a capital letter of identifier word and vice versa. Khayyam doesn't offer any specific keyword for this purpose like Go language.

### Compile time functions
- Below function MUST compute in compile time not runtime. Any use of CNF_KeepAlive_Idle return variable is just a simple constant capsule.
```Khayyam
tp CNF_KeepAlive_Idle mt (self Config) () (dur duration.NanoSecond) {
    dur.FromASCII("7200")
    dur.Multiplication(duration.NanoSecondInSecond)
}

tp closeIdleSocket mt (tcpSock Sock) (st net_p.Socket) (err error_p.Error) {
    // some logic ...
    // vr passIdle boolean.Boolean
    tcpSock.checkIdlePass (Config.CNF_KeepAlive_Idle()) (passIdle)
    // some logic ...
}
```

### Inline Function
- Inline function return const as declare const globally. Below codes are same when compile them.

## Runtime
- We need to offer very simple but with some unique logic

### Change logic in runtime
You can write code to change(add or remove) modules binary code in runtime. It is like `WASM` idea. It can be very dangerous feature and MUST tag as `unsafe`. It is useful to add or remove modules in microservice way but as describe by [this paper from google expert software developers](https://dl.acm.org/doi/pdf/10.1145/3593856.3595909)

## Linters
- Linters MUST suggest naming e.g. in importing other packages, ...
- Linter MUST provide `Type` suggestion in developing of codes.
- Variables MUST treat immutable by default after initialization, unless Developer indicate it by some specific method. If need to change the capsule data, need to copy desire data to new variables.
- Linter MUST help to generate some useful methods like getter and setter methods. For each structure field developer must define global get & set methods, otherwise compiler throw compile error if any read||write directly to fields be in codes.

## Not implement features!?
In this part, we say why not choose something that be real in some other programming languages.

### Package (Packaging)
We can't decide yet to offer any package some files code.   
When in interfaces we need to clarify methods name e.g. `Parent() T` is meaningless name and need to clarify as `ParentCommand() Command` or `ParentElement() Element` why we need package level encapsulation?

### **Function**:
Function can't imagine as independent blocks of code. It is a capsule and need to provide more methods about its behavior. Many languages need to provide their other usages such as authorization to access the function as top level keyword such as `private`, `public`,... But Khayyam don't introduce many top level keyword for this type of requirements, Due to we believe this requirements CAN change in near future and this abstraction CAN easily implement by methods for any capsule. So a function is a capsule with many methods to introduce itself.   
Khayyam don't allow developers to indicate functions by use any keywords like `fn` or `func`, ... as `tp {name} fn (args) (returns)`. Khayyam still support pure standalone function and MUST not assume in wrong way. It can be assumed that functions are methods for the package level encapsulation and Khayyam not support this style.
We suggest use `Do` method name for a capsule to doing its logic like a simple function call 
```khayyam
// when is a helper function for setting the 'when' field of a Timer.
// It returns what the time will be, in nanoseconds, Duration d in the future.
tp Do mt (wh WhenHelper) (d duration.NanoSecond) (t monotonic.Time) {}

// use in this manner:::
vr t1 monotonic.Time
WhenHelper.Do (d) (t1)
```

### Constant
- [Constant](https://en.wikipedia.org/wiki/Constant_(computer_programming)) is a `variable` that return by a `capsule` `method` that can't change after first initialization. So it is an organization rule not compiler one. e.g. a `config` capsule for a module that expose module variables, this config capsule may provide some method to change some of its variables.
- We have 2 types of constant:
  - Static constants as compile time declaration and initialization that usually inline in compile time
  - Dynamically-valued constants as compile time declaration and runtime initialization that can't inline in compile time and need memory service call to get its value.
- Constants can assume as functions that run in compile time! so write functions that return desire variable that live in that function body!
- Dev can change variables in runtime. `compiler` CAN force `Runtime` to change binary codes and don't need to get it by memory call. Compiler and runtime just let to change the value with the same memory size. (Really decide to provide this??)

### Operators
Since we have no primitive types in language syntax, We don't need to provide any operators!

### Decorators
As describe [decorators in TS](https://www.typescriptlang.org/docs/handbook/decorators.html) or [python decorators](https://www.w3schools.com/python/python_decorators.asp) or [Java decorators](https://docs.oracle.com/javaee/7/api/javax/decorator/package-summary.html), It is just a `initialize` process that we don't want to have magic and not support this feature.

### Methods Overloading
It seems we need this feature if we want to have very simple [generic](https://en.wikipedia.org/wiki/Generic_programming) and polymorphism.   
Due to Khayyam not support primitive types, All disadvantages disappear and JUST advantages will shine.

### Method overriding
Method overloading is a compile-time polymorphism. Method overriding is a run-time polymorphism. CAN provide runtime feature when not provide rich runtime??

### Memory management - GC (Garbage Collection)
Libraries must provide memory management and data types (almost always ADT's decide) decide to choose and use desire memory management for its usage.

### Tuples
Tuples are implemented by two dynamic and static type languages.
- In a dynamic language, tuples implement unsafe structures that allocate by the runtime and have a performance penalty for the app because we use runtime for developing or compiling phase.
- In a static language, tuples implement safe structures that just don't have internal names. But it is duplicate work, more learning curve and adds more confusing situation just lazy developer to not indicate names.

### Type Inference
- Khayyam don't support automatic type inference in compiler level, It is linter job.
- Developers can't assign to var before decare it.
- e.g.
```go
// Other languages
var x = 41
var y = 3.14
```
```khayyam
// Khayyam way
vr x whole.W8; x.FromString ("41")

vr y rational.R32; y.FromString ("3.14")
```

### Iteration - Loop
We think loop can implement easily by `goto` instead of `while`, `for`, `do`, ... if and just if `Iterator` interface not implement by desire type. But strongly suggest iteration MUST implement by just `Container` ADT.

### Dependency Management
We don't offer any version control for your codes, So we must not offer any dependency management too.

## Keyword in a glance
| Top level | type  | Logical | *********** | *********** |
| :-------: | :---: | :-----: | :---------: | :---------: |
|    tp     |  in   |   if    |             |             |
|    vr     |  im   | else if |             |             |
|           |  cp   |  else   |             |             |
|           |  mt   |  goto   |             |             |
|           |  ab   |         |             |             |
|           |       |         |             |             |
|           |       |         |             |             |

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
