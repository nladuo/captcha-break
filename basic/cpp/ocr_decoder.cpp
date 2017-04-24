#include "ocr_decoder.h"

void OCRDecoder::decodeGrayMat (cv::Mat mat, char *result)
{
    tesseract::TessBaseAPI tess;
    tess.Init(NULL, "eng", tesseract::OEM_DEFAULT);
    tess.SetPageSegMode(tesseract::PSM_SINGLE_BLOCK);
    tess.SetImage((uchar*)mat.data, mat.cols, mat.rows, 1, mat.cols);

    strcpy(result, tess.GetUTF8Text());
}
