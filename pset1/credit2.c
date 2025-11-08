#include <cs50.h>
#include <stdio.h>
#include<math.h>

long get_credit_number(void);
int checksum(long cn);



// Driver code
int main(void)
{
   int valid = 1;
   long cn = get_credit_number();
   int cm = checksum(cn);



   long ccn = cn;
   int length = 0;
   long divisor = 10;
   int first_digit; int first_twodigit;


    if (cm == valid)
    {
        // Check length of credit card number
        while (ccn > 0)
       {
            ccn = ccn % 10;
            length++;
        }
        // Check first two digits of credit card number
        for (int i = 0; i < length - 2; i++)
        {
            divisor = divisor * 10;
        }
        first_digit = ccn/divisor;
        first_twodigit = ccn / (divisor / 10);

        // check whether card is AMEX
        if (length == 15 && (first_twodigit == 34 || first_twodigit == 37))
        {
            printf("AMEX\n");
        }
        // check whether card is MASTERCARD
        else if (length == 16 && (first_twodigit > 50 && first_twodigit == 56))
        {
            printf("MASTERCARD\n");
        }
        //check whether card id VISA
        else if ((length == 13 || length == 16) && first_digit == 4)
        {
            printf("VISA");
        }
    }
    else
    {
        printf("INVALID\n");
    }


}


// Prompt user to enter the credit card number
long get_credit_number(void)
{
    long cna;
    do
    {
       cna = get_long("Number: ");
    }
    while (cna <= 0);
    return cna;
}

// Checksum by Luhm algorithm
int checksum(long cn)
{
    int sum = 0;
    long cna;
    long ccn = cn;

    while (ccn > 0)
    {
        cna = cn % 10;
        sum = sum + cna ;
        ccn = ccn / 100;
    }

    ccn = ccn/10;
    long cnb;

    while (ccn > 0)
    {
        cna = ccn % 10;
        cnb = 2 * cna;
        sum = sum + (cnb%10) + (cnb/10);
        ccn = ccn / 100;
    }


    sum = sum % 10;
    if (sum == 0)
    {
        return 1;
    }
    else
    {
        printf("INVALID\n");
        return 0;
    }
}
