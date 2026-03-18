# 6.1 
text = "Hello, World!"
print("Первый символ:", text[0])
print("Последний символ:", text[-1])
print("Подстрока:", text[7:12])

# 6.2 
user_string = input("Введите строку: ")
if len(user_string) % 2 == 0:
    print(user_string.upper())
else:
    print(user_string.lower())

# 6.3 
user_string = input("Введите строку: ")
small = "aeiou"
big = "AEIOU"
count_small = 0
count_big = 0
for char in user_string:
    if char in small:
        count_small += 1
    elif char in big:
        count_big += 1
print("Количество строчных гласных:", count_small)
print("Количество заглавных гласных:", count_big)

# 6.4 
user_string = input("Введите строку: ")
result = ""
for i in range(len(user_string)):
    if i == 0 or user_string[i] != user_string[i - 1]:
        result += user_string[i]
print("Результат после удаления повторов:", result)

# 6.5 
word1 = input("Введите первое слово: ").lower()
word2 = input("Введите второе слово: ").lower()
if sorted(word1) == sorted(word2):
    print(True)
else:
    print(False)