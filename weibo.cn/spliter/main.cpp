#include "spliter.h"

int main(int argc, char *argv[])
{
    if(argc != 2) {
        fprintf(stderr, "Usage: ./spliter <image_filename> <output_filenames>[4]\n");
        return 1;
    }
    Spliter spliter("./dataset/");
    spliter.split_letters(argv[1]);
    return 0;
}
