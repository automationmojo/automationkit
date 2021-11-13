# Coding Standards

    *in-progress*

## `return` Statements
All functions or methods that are not generators should have a `return` statement.  The return statements are important for three reasons:

* It prevents the formation of appended functionality during a bad code merge
* It provides line number data for the debugger
* It provides a way to check results, in context, before a return
* It make code easier to read

Below is a detailed description of each of these issues.
### Formation of Appended Functionality
One of the common tasks that is performed frequently by software developer is the refactoring or merging of code.  During the process of refactoring or merging code, function declarations might be missed or incorrectly deleted.  When this happens, new functionality can end up being inadvertantly appended to the previous function in the code.  Take the following two functions as a simplified example.

```python
def say_hello():
    print("Hello")

def say_world():
    print("World")
```

If returns are not present at the end of the functions above, during a refactor or code merge it is possible for lines of code to be removed, like if the `say_world` function declaration was deleted like so:

```python
def say_hello():
    print("Hello")

    print("World")
```

Now, without warning from python, the functionality of the `say_world` function has been appended to the `say_hello` function and thus changes the functionality of the `say_hello` function without warning.

Now lets look at what would happen if the same thing took place when return statements are utilized as in the code below.

```python
def say_hello():
    print("Hello")
    return

def say_world():
    print("World")
    return
```

In the code above, we clearly mark the end of our functions so python has a better chance of doing the correct thing when code is modified incorrectly.  If the function declaration for `say_world` is removed like so.

```python
def say_hello():
    print("Hello")
    return

    print("World")
    return
```

In the case above, python will not execute the stagling code and will not append its functionality to the `say_hello` method.  Also, the python linter can show the remaining code body for `say_world` as dead code or unreachable code and complain when it tries to lint the code in the file.

### Line Number for Debugging
A very important aspect of test code is debuggability.  In order to be able to inspect the results of a function before it returns, you need a line of code to hang a breakpoint on. By
stopping the debugger on the return statement, you can see the values of the inputs to the
function and values of any intermediate byproducts or local variables in the context of the
function.

```python
import dis

def function_with_return(a: int, b: int):
    if a + b == 99:
        print ("Hello '99'")
    return

def function_without_return(a: int, b: int):
    if a + b == 99:
        print ("Hello '99'")

print("==== FUNCTION WITH RETURN ====")
fwr_assem = dis.dis(function_with_return)
print(fwr_assem)
print("")


print("==== FUNCTION WITHOUT RETURN ====")
fwor_assem = dis.dis(function_without_return)
print(fwor_assem)
print("")
```

```bash
==== FUNCTION WITH RETURN ====
  4           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD
              6 LOAD_CONST               1 (99)
              8 COMPARE_OP               2 (==)
             10 POP_JUMP_IF_FALSE       20

  5          12 LOAD_GLOBAL              0 (print)
             14 LOAD_CONST               2 ("Hello '99'")
             16 CALL_FUNCTION            1
             18 POP_TOP

  6     >>   20 LOAD_CONST               0 (None)  # Has a Distict Line Number (6)
             22 RETURN_VALUE
None
```

Distinct lines of code, which have an associated line number, are very important for enabling a
great debugging experience.  Without a distinct line of code or line number, there is no place
to hang a breakpoint on a piece of code that is associated with the bytecode of a program.

```bash
==== FUNCTION WITHOUT RETURN ====
  9           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD
              6 LOAD_CONST               1 (99)
              8 COMPARE_OP               2 (==)
             10 POP_JUMP_IF_FALSE       20

 10          12 LOAD_GLOBAL              0 (print)
             14 LOAD_CONST               2 ("Hello '99'")
             16 CALL_FUNCTION            1
             18 POP_TOP
        >>   20 LOAD_CONST               0 (None)  # Has NO Line Number
             22 RETURN_VALUE
None
```


### In Context Return Verification
One of the most important aspects of writing debuggable code, is to write code in such a way that you can see the values of the local variables that contributed to the creation of the value being returned.  The following is an example function that demonstrates the concept of writing functions so the context of the return value can be examined.

```python
def example_function(a: int, b: int) -> int:

    multiplier = random.randint(0, 10)

    rtnval: int = (a + b) * multiplier
    
    return rtnval
```

From looking at the simple example above, you can see that in order to debug the function and
make sure it is returning the correct answer, it is useful to be able to see the `multiplier`
parameter that is generated locally and is being used to effect the output.  Providing a simple
independant return allows us to see the context that is generating the output value.  Another
example below shows how a function like this might be written that will not provide the same
ability to debug the function.

```python
def example_function(a: int, b: int) -> int:
    return (a + b) * random.randint(0, 10)
```

This function is sometimes valued by some developers for its brevity, but for testing purposes this coding style results in reduced quality code. The reason the code is reduced quality is because you cannot see the context of the return value being generated.  If you put a breakpoint
on the `return` statement, you don't see the resulting value until you step out into the calling function context. When you step out of the function to its calling function to see the return value, the local variables of the `example_function` and the context that generated the return 
value is no longer available. Upon the return of the function, the stack was popped and the 
context went away.

Because of the importance of examining the context that generates a returned value, it is always prefered to create a local variable in order to effect a simple return like so:

```python
def example_function(a: int, b: int, c: int):
    rtnval = (a + b) * c
    return rtnval
```

Vise a complexed return statement such as

```python
def example_function(a: int, b: int, c: int):
    return (a + b) * c
```

### Code Legibility


