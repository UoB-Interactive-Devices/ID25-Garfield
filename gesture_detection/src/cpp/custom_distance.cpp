#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>

namespace py = pybind11;


const float BETWEEN_SIZE = 4;
const float BETWEEN_WEIGHT = 0.3;
const float EACH_SIZE = 5;
const float EACH_WEIGHT = 0.3;
const float HORIZON_SIZE = 1;
const float HORIZON_WEIGHT = 0.1;
const float CAMERA_SIZE = 1;
const float CAMERA_WEIGHT = 0.1;

const float MAX_HAND_DISTANCE = 4;
const float HAND_DIST_WEIGHT = 0.1;

/*
Calculates the distance between 2 gesture frames (which each represent 2 mediapipes hands), stored a np arrays of floats
with the structure (defined in consts):
[4 * left between, 5 * left each, 1 * left horizon, 1 * left camera, 4 * right between, 5 * right each, 1 * right horizon, 1 * right camera, 1 * hand distance]
where all of right and/or left could be NaNs
each value apart from distance represents an angle between 0 and pi (in radians) s.t. the distance between two angles is abs(angle1 - angle2)

if one handed minimum of left and right hand
if two handed the average of left and right hand 

s.t. the distance between two frames is between 0 and pi

For more details on what this array represents read GestureFrame.py
*/
double custom_distance_two_handed(py::array_t<float> frame1, py::array_t<float> frame2) {

    py::buffer_info buf1 = frame1.request();
    py::buffer_info buf2 = frame2.request();
    
    if (buf1.size != 23 || buf2.size != 23) {
        throw std::runtime_error("Frame length incorrect!");
    }
    
    float *ptr1 = static_cast<float *>(buf1.ptr);
    float *ptr2 = static_cast<float *>(buf2.ptr);
    
    double total = 0.0;

    //LEFT HAND
    if (!std::isnan(ptr1[0]) && !std::isnan(ptr2[0])){
        double distSum = std::fabs(ptr1[0] - ptr2[0]) + std::fabs(ptr1[1] - ptr2[1]) + 
                         std::fabs(ptr1[2] - ptr2[2]) + std::fabs(ptr1[3] - ptr2[3]);
        total += (distSum / BETWEEN_SIZE) * (BETWEEN_WEIGHT/2);

        double eachSum = std::fabs(ptr1[4] - ptr2[4]) + std::fabs(ptr1[5] - ptr2[5]) + 
                         std::fabs(ptr1[6] - ptr2[6]) + std::fabs(ptr1[7] - ptr2[7]) + 
                         std::fabs(ptr1[8] - ptr2[8]);
        total += (eachSum / EACH_SIZE) * (EACH_WEIGHT/2);

        double horizonSum = std::fabs(ptr1[9] - ptr2[9]);
        total += (horizonSum / HORIZON_SIZE) * (HORIZON_WEIGHT/2);

        double cameraSum = std::fabs(ptr1[10] - ptr2[10]);
        total += (cameraSum / CAMERA_SIZE) * (CAMERA_WEIGHT/2);
    }else{ 
        total += M_PI * (BETWEEN_WEIGHT/2);
        total += M_PI * (EACH_WEIGHT/2);
        total += M_PI * (HORIZON_WEIGHT/2);
        total += M_PI * (CAMERA_WEIGHT/2);
    }

    if (!std::isnan(ptr1[11]) && !std::isnan(ptr2[11])){
        double distSum = std::fabs(ptr1[11] - ptr2[11]) + std::fabs(ptr1[12] - ptr2[12]) + 
                         std::fabs(ptr1[13] - ptr2[13]) + std::fabs(ptr1[14] - ptr2[14]);
        total += (distSum / BETWEEN_SIZE) * (BETWEEN_WEIGHT/2);
        
        double eachSum = std::fabs(ptr1[15] - ptr2[15]) + std::fabs(ptr1[16] - ptr2[16]) + 
                         std::fabs(ptr1[17] - ptr2[17]) + std::fabs(ptr1[18] - ptr2[18]) + 
                         std::fabs(ptr1[19] - ptr2[19]);
        total += (eachSum / EACH_SIZE) * (EACH_WEIGHT/2);
        
        double horizonSum = std::fabs(ptr1[20] - ptr2[20]);
        total += (horizonSum / HORIZON_SIZE) * (HORIZON_WEIGHT/2);
        
        double cameraSum = std::fabs(ptr1[21] - ptr2[21]);
        total += (cameraSum / CAMERA_SIZE) * (CAMERA_WEIGHT/2);
    }else{
        total += M_PI * (BETWEEN_WEIGHT/2);
        total += M_PI * (EACH_WEIGHT/2);
        total += M_PI * (HORIZON_WEIGHT/2);
        total += M_PI * (CAMERA_WEIGHT/2);
    }

    if (!std::isnan(ptr1[22]) && !std::isnan(ptr2[22])){
        double handDist = std::fabs(ptr1[22] - ptr2[22]);
        total += (handDist / MAX_HAND_DISTANCE) * (M_PI*HAND_DIST_WEIGHT);
    }else{
        total += M_PI*HAND_DIST_WEIGHT;
    }

    return total;
}


double custom_distance_one_handed(py::array_t<float> frame1, py::array_t<float> frame2) {

    py::buffer_info buf1 = frame1.request();
    py::buffer_info buf2 = frame2.request();
    
    if (buf1.size != 23 || buf2.size != 23) {
        throw std::runtime_error("Frame length incorrect!");
    }
    
    float *ptr1 = static_cast<float *>(buf1.ptr);
    float *ptr2 = static_cast<float *>(buf2.ptr);
    
    double left_total = 0.0;
    double right_total = 0.0;

    //LEFT HAND
    if (!std::isnan(ptr1[0]) && !std::isnan(ptr2[0])){
        double distSum = std::fabs(ptr1[0] - ptr2[0]) + std::fabs(ptr1[1] - ptr2[1]) + 
                         std::fabs(ptr1[2] - ptr2[2]) + std::fabs(ptr1[3] - ptr2[3]);
        left_total += (distSum / BETWEEN_SIZE) * (BETWEEN_WEIGHT);

        double eachSum = std::fabs(ptr1[4] - ptr2[4]) + std::fabs(ptr1[5] - ptr2[5]) + 
                         std::fabs(ptr1[6] - ptr2[6]) + std::fabs(ptr1[7] - ptr2[7]) + 
                         std::fabs(ptr1[8] - ptr2[8]);
        left_total += (eachSum / EACH_SIZE) * (EACH_WEIGHT);

        double horizonSum = std::fabs(ptr1[9] - ptr2[9]);
        left_total += (horizonSum / HORIZON_SIZE) * (HORIZON_WEIGHT);

        double cameraSum = std::fabs(ptr1[10] - ptr2[10]);
        left_total += (cameraSum / CAMERA_SIZE) * (CAMERA_WEIGHT);
    }else{ 
        left_total += M_PI * (BETWEEN_WEIGHT);
        left_total += M_PI * (EACH_WEIGHT);
        left_total += M_PI * (HORIZON_WEIGHT);
        left_total += M_PI * (CAMERA_WEIGHT);
    }

    if (!std::isnan(ptr1[11]) && !std::isnan(ptr2[11])){
        double distSum = std::fabs(ptr1[11] - ptr2[11]) + std::fabs(ptr1[12] - ptr2[12]) + 
                         std::fabs(ptr1[13] - ptr2[13]) + std::fabs(ptr1[14] - ptr2[14]);
        right_total += (distSum / BETWEEN_SIZE) * (BETWEEN_WEIGHT);
        
        double eachSum = std::fabs(ptr1[15] - ptr2[15]) + std::fabs(ptr1[16] - ptr2[16]) + 
                         std::fabs(ptr1[17] - ptr2[17]) + std::fabs(ptr1[18] - ptr2[18]) + 
                         std::fabs(ptr1[19] - ptr2[19]);
        right_total += (eachSum / EACH_SIZE) * (EACH_WEIGHT);
        
        double horizonSum = std::fabs(ptr1[20] - ptr2[20]);
        right_total += (horizonSum / HORIZON_SIZE) * (HORIZON_WEIGHT);
        
        double cameraSum = std::fabs(ptr1[21] - ptr2[21]);
        right_total += (cameraSum / CAMERA_SIZE) * (CAMERA_WEIGHT);
    }else{
        right_total += M_PI * (BETWEEN_WEIGHT);
        right_total += M_PI * (EACH_WEIGHT);
        right_total += M_PI * (HORIZON_WEIGHT);
        right_total += M_PI * (CAMERA_WEIGHT);
    }

    return std::min(left_total, right_total);
}



PYBIND11_MODULE(custom_distance, m) {
    m.doc() = "A module providing custom distance for gesture detection";
    
    m.def("two_handed", &custom_distance_two_handed, 
          "Function that finds a custom distance between two gesture frame for 2 handed, returning a value between 0 (similar) and pi (unsimilar).",
          py::arg("frame1"), py::arg("frame2"));

    m.def("one_handed", &custom_distance_one_handed, 
        "Function that finds a custom distance between two gesture frame for 1 handed, returning a value between 0 (similar) and pi (unsimilar).",
        py::arg("frame1"), py::arg("frame2"));
}