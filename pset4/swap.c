#include <cs50.h>
#include <stdio.h>

void swap(int *a, int *b);

int main(void)
{
    int x = get_int("x: ");
    int y = get_int("y: ");

    swap(&x, &y);

    printf("x: %i\n", x);
    printf("y: %i\n", y);
}

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}
