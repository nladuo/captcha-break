cmake_minimum_required(VERSION 2.8)
project(recognizer)
include_directories(${PROJECT_SOURCE_DIR} )
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set( tiny_cnn_hrds tiny_cnn/activations/activation_function.h  tiny_cnn/io/cifar10_parser.h  tiny_cnn/layers/convolutional_layer.h  tiny_cnn/io/display.h  tiny_cnn/util/image.h  tiny_cnn/layers/layer.h  tiny_cnn/lossfunctions/loss_function.h  tiny_cnn/io/mnist_parser.h  tiny_cnn/optimizers/optimizer.h  tiny_cnn/util/product.h  tiny_cnn/util/util.h
tiny_cnn/layers/average_pooling_layer.h  tiny_cnn/config.h  tiny_cnn/util/deform.h tiny_cnn/layers/fully_connected_layer.h tiny_cnn/layers/input_layer.h  tiny_cnn/layers/layers.h  tiny_cnn/layers/max_pooling_layer.h  tiny_cnn/network.h  tiny_cnn/layers/partial_connected_layer.h  tiny_cnn/tiny_cnn.h  tiny_cnn/util/weight_init.h tiny_cnn/layers/arithmetic_layer.h tiny_cnn/layers/concat_layer.h tiny_cnn/layers/feedforward_layer.h tiny_cnn/layers/dropout_layer.h tiny_cnn/layers/lrn_layer.h tiny_cnn/layers/linear_layer.h tiny_cnn/node.h tiny_cnn/nodes.h tiny_cnn/util/target_cost.h tiny_cnn/util/aligned_allocator.h tiny_cnn/layers/deconvolutional_layer.h tiny_cnn/layers/max_unpooling_layer.h tiny_cnn/layers/average_unpooling_layer.h)
find_package(OpenCV REQUIRED)
find_package(Boost REQUIRED COMPONENTS filesystem system)
aux_source_directory(./ SOURCE_DIR)
add_executable(recognizer ${SOURCE_DIR} ${tiny_cnn_hrds})
target_link_libraries(recognizer ${OpenCV_LIBS})
target_link_libraries(recognizer ${Boost_LIBRARIES})