#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int rgbGray = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = rgbGray;
            image[i][j].rgbtGreen = rgbGray;
            image[i][j].rgbtBlue = rgbGray;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE buffer;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            buffer = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = buffer;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sum_red = 0, sum_blue = 0, sum_green = 0, total_pixels = 0;
            for (int ui = i - 1; ui < i + 2; ui++)
            {
                for (int uj = j - 1; uj < j + 2; uj++)
                {
                    if (ui >= 0 && uj >= 0 && ui < height && uj < width)
                    {
                        sum_red += image[ui][uj].rgbtRed;
                        sum_green += image[ui][uj].rgbtGreen;
                        sum_blue += image[ui][uj].rgbtBlue;
                        total_pixels++;
                    }
                }
            }
            copy[i][j].rgbtRed = round(sum_red / total_pixels);
            copy[i][j].rgbtGreen = round(sum_green / total_pixels);
            copy[i][j].rgbtBlue = round(sum_blue / total_pixels);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    int gx_array[] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int gy_array[] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gx_red = 0, gx_blue = 0, gx_green = 0, counter = 0, gy_red = 0, gy_blue = 0, gy_green = 0;
            for (int ui = i - 1; ui < i + 2; ui++)
            {
                for (int uj = j - 1; uj < j + 2; uj++)
                {
                    if (!(ui < 0 || uj < 0 || ui >= height || uj >= width))
                    {
                        gx_red += gx_array[counter] * image[ui][uj].rgbtRed;
                        gx_green += gx_array[counter] * image[ui][uj].rgbtGreen;
                        gx_blue += gx_array[counter] * image[ui][uj].rgbtBlue;
                        gy_red += gy_array[counter] * image[ui][uj].rgbtRed;
                        gy_green += gy_array[counter] * image[ui][uj].rgbtGreen;
                        gy_blue += gy_array[counter] * image[ui][uj].rgbtBlue;
                    }
                    counter++;
                }
            }
            int finalRed = round(sqrt(pow(gx_red, 2) + pow(gy_red, 2)));
            int finalGreen = round(sqrt(pow(gx_green, 2) + pow(gy_green, 2)));
            int finalBlue = round(sqrt(pow(gx_blue, 2) + pow(gy_blue, 2)));

            copy[i][j].rgbtRed = (finalRed > 255) ? 255 : finalRed;
            copy[i][j].rgbtGreen = (finalGreen > 255) ? 255 : finalGreen;
            copy[i][j].rgbtBlue = (finalBlue > 255) ? 255 : finalBlue;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}
