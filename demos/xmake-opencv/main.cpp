#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>

int main(int argc, char** argv) {

    std::string img_path = "./../../../../d2learn.png";

    if (argc == 2) {
        img_path = std::string(argv[1]);
    }

    cv::Mat image = cv::imread(img_path.c_str(), cv::IMREAD_COLOR);
    
    if (image.empty()) {
        std::cout << "Could not open or find the image\n";
        return -1;
    }

    cv::namedWindow("Display Image", cv::WINDOW_AUTOSIZE);
    cv::imshow("Display Image", image);
    
    cv::waitKey(0);

    return 0;
}