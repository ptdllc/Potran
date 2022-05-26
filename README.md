# Potran
The Potran programming language

## Why Python/LARK?
It was the most sensible option for creating the first versions of our compiler as it allows for quicker and more sensible development. LARK was chosen because of it's sensible grammar syntax and easy to use shortcuts, plus it is more powerful and feature ready than PLY or other parser tools, and making a custom parser made no sense.

## Hello, World!
```p22
Program HelloWorld {
    Export Integer32::Function Main () {
        OutputLine "Hello, World!";
        Return 0;
    };
};
```