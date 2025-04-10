def count_digits(n):
    # Base case: if the number is a single digit, return 1
    if n < 10:
        return 1
    # Recursive case: remove the last digit and count again
    return 1 + count_digits(n // 10)

# Example usage
num = int(input("Enter a number: "))
print("Number of digits:", count_digits(num))
