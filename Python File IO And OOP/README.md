# Python File IO And OOP

## Overview

Covers intermediate Python skills: file I/O operations, object-oriented design, and functional programming with higher-order functions.

## Files

| File | Description |
|------|-------------|
| `File IO And OOP.ipynb` | File I/O, OOP classes, functions, and lambda expressions |

## How to Run

```bash
jupyter notebook "File IO And OOP.ipynb"
```

## Topics Covered

### File I/O
- Reading and displaying file contents (`displayFile`)
- Counting words and lines in a file (`countWords`, `countLines`)
- Appending text to a file (`appendToFile`)
- Exception handling (`try/except/finally`) for `FileNotFoundError`
- File removal with `os.remove()`

### Object-Oriented Programming
Three-class banking system:
- **`Bank`** — container for multiple accounts
- **`Account`** — deposit, withdraw, balance tracking
- **`Transaction`** — executes deposit/withdrawal against the bank
- `__str__` dunder methods for readable output

### Functions and Arguments
- Typed function parameters (`a: int, b: int`)
- Keyword arguments with `**kwargs` (`printDetails`)
- Variadic arguments with `*args` (`findAvg`)
- Dictionary key lookup and default insertion (`checkKeyWords`)

### Functional Programming
- `map()` with lambda — square each element of a list
- `filter()` with lambda — filter strings starting with a vowel
- Custom string reversal without slicing