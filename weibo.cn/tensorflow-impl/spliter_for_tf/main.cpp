#include "spliter.h"
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>


int main(int argc, char *argv[])
{
    if (argc != 2) {
        std::cout << "please specify image file";
        return 0;
    }
    Spliter spliter("./");
    spliter.split_and_save(argv[1]);
    return 0;
}
