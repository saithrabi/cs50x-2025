#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // tell the user to how to use this code
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    for (int k = 0; k < strlen(argv[1]); k++)
    {
        if (isalpha(argv[1][k]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int k = atoi(argv[1]) % 26;
    string plaintext = get_string("Plaintext: ");

    printf("Ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (!isalpha(plaintext[i]))
        {
            printf("%c", plaintext[i]);
            continue;
        }

        int ascii_offset = isupper(plaintext[i]) ? 65 : 97;
        int pi = plaintext[i] - ascii_offset;
        int ci = (pi + k) % 26;

        printf("%c", ci + ascii_offset);
    }
    printf("\n");
    return 0;
}
