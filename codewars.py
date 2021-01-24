# def high(x):
#     alphabet = list('abcdefghijklmnopqrstuvwxyz')
#     res = 0
#     # [print(alphabet[0]) for i in range(len(alphabet))]
#     for word in x.split():
#         buff = 0
#         for letter in range(len(word)):
#             if word[letter] in alphabet:
#                 buff += alphabet.index(word[letter]) + 1
#             if res < buff:
#                 res = buff
#                 res_w = word
#     return res_w
#
#
#
# def main():
#     print(high("what time are we climbing up the volcano"))
#
#
# if __name__ == '__main__':
#     main()