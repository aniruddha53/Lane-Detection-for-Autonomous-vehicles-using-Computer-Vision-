# Lane-Detection-for-Autonomous-vehicles-

❖ Advanced Driving Assistant Systems, intelligent and autonomous vehicles are promising solutions to enhance road safety, traffic issues and passengers' comfort.
❖ Such applications require advanced computer vision algorithms that demand powerful computers with high-speed processing capabilities.
❖ Keeping intelligent vehicles on the road until its destination, in some cases, remains a great challenge, particularly when driving at high speeds.
❖ The first principle task is robust navigation, which is often based on system vision to acquire RGB images of the road for more advanced processing.
❖ The second task is the vehicle's dynamic controller according to its position, speed and direction. In this project, we tried to implement an efficient road boundaries and detection algorithm for intelligent and autonomous vehicles

IMPLEMENTATION METHODOLOGY:

1. Converting RGB image to Gray scale image:
➢ Using cvtColor transformation form cv2 (OpenCV)
2. Smoothening Image
➢ Using Gaussian filter to reduce noise and Smoothen the image
3. Edge Detection
➢ Using Canny Edge detection
4. Finding Lane lines of interest
➢ Using Hough Transformation
5. Optimization
➢ Using Average slope-intercept method
6. Detecting Lanes in the image file
➢ Combining all the above methods to detect lane lines in an image file
7. Lane Detection in the video file
➢ Applying same methodology but for a continuous set of images, .i.e., A Video file

Implementation Outcomes:
In this project we accomplished our goal of detecting lane lines both in an image file as well as a video file, which is one of the up-most importance for cars which use the lane departure warning system and corrects the position of the vehicle with respect to the detected lane
