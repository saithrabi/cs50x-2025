#include <stdio.h>
#include <cs50.h>

// declaring functions
int get_size(void);
void print_pyramid(int size);

// main function
int main()
{
    int n = get_size();
    print_pyramid(n);
}

// function for asking user for size
int get_size(void)
{
    int n;
    do{
        n = get_int("size: ");
    }while(n<1 || n>8);
    return n;
}

// function for printing pyramid
void print_pyramid(int size)
{

    for(int row = 0; row < size; row++)
    {
        for(int space = 0; space < size-row-1; space++)
        {
            printf(" ");
        }

        for(int column = 0; column <= row; column++)
        {
            printf("#");
        }
        printf("  ");
        for(int column = 0; column <= row; column++){
            printf("#");
        }
        printf("\n");
    }
}
