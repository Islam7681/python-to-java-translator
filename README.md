# Python to Java Translator

A Python script that converts basic Python code into equivalent Java code using regular expressions and simple parsing.

## How to Use
1. Write your Python code in `input.txt`
2. Run the script:
   python translator.py
3. The translated Java code will be written to `output.txt`

## Example

input.txt:
def greet(name):
    if name == "Alice":
        print("Hello, Alice")
    else:
        print("Hello, stranger")

output.txt:
public class TranslatedCode {
public static void main(String[] args) {
}
public static void greet(int name) {
if (name == "Alice") {
System.out.println("Hello, Alice");
} else {
System.out.println("Hello, stranger");
}
}
}