#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int getNumLetters(string text);
int getNumSentences(string text);
int getNumWords(string text);
int getGradeLevel(int getNumLetters, int getNumSentences, int getNumWords);
void printGrade(int getGradeLevel);

int main(void)
{
    string text = get_string("Text: ");
    int letters = getNumLetters(text);
    int sentences = getNumSentences(text);
    int words = getNumWords(text);

    int gradeLevel = getGradeLevel(letters, sentences, words);

    printGrade(gradeLevel);
}

int getNumLetters(string text)
{
    int numLetters = 0;
    int len = strlen(text);
    for (int i = 0; i < len; i++)
    {
        if (isalpha(text[i]))
        {
            numLetters += 1;
        }
    }
    return numLetters;
}

int getNumWords(string text)
{
    int numWords = 0;
    int len = strlen(text);
    for (int i = 0; i < len; i++)
    {
        if (text[i] == ' ')
        {
            numWords += 1;
        }
    }
    return numWords + 1;
}

int getNumSentences(string text)
{
    int NumSentences = 0;
    int len = strlen(text);
    for (int i = 0; i < len; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            NumSentences += 1;
        }
    }
    return NumSentences;
}

int getGradeLevel(int getNumLetters, int getNumSentences, int getNumWords)
{
    float S = (getNumSentences / (float) getNumWords) * 100;
    float L = (getNumLetters / (float) getNumWords) * 100;
    return round(0.0588 * L - 0.296 * S - 15.8);
}
void printGrade(int getGradeLevel)
{
    if (getGradeLevel < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (getGradeLevel > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", getGradeLevel);
    }
}
