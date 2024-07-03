/*
 * Copyright 1996-2023 Cyberbotics Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <webots/motor.h>
#include <webots/position_sensor.h>
#include <webots/robot.h>
#include <stdlib.h>


#include <stdio.h>
#include <string.h>

#define TIME_STEP 320

int main(int argc, char **argv) {
  printf("muscle controller started\n");
  wb_robot_init();
  WbDeviceTag ps = wb_robot_get_device("position sensor");
  
  double p = 0.0;
  double max = 2.0;
  double step = 0.4;
  


  int rows = 1; // Define the number of rows
  int cols = 6;
  

  WbDeviceTag **devices = malloc(rows * sizeof(WbDeviceTag*)); // Dynamically allocate memory for rows of device pointers

    for (int i = 0; i < rows; i++) {
        devices[i] = malloc(cols * sizeof(WbDeviceTag)); // Dynamically allocate memory for columns of device pointers for each row
        for (int j = 0; j < cols; j++) {
            char deviceName[20]; // Assume device names will not exceed 19 characters
            sprintf(deviceName, "muscle_%d_%d", i, j); // Construct the device name using row and column indices
            devices[i][j] = wb_robot_get_device(deviceName); // Retrieve the device by name and store its tag
            // Assume you need to perform some operations with the device here
        }
    }
  
  WbDeviceTag **sensors = malloc(rows * sizeof(WbDeviceTag*)); // Dynamically allocate memory for rows of device pointers

    for (int i = 0; i < rows; i++) {
        sensors[i] = malloc(cols * sizeof(WbDeviceTag)); // Dynamically allocate memory for columns of device pointers for each row
        for (int j = 0; j < cols; j++) {
            char deviceName[20]; // Assume device names will not exceed 19 characters
            sprintf(deviceName, "muscle_%d_%d_sensor", i, j); // Construct the device name using row and column indices
            sensors[i][j] = wb_robot_get_device(deviceName); // Retrieve the device by name and store its tag
            // Assume you need to perform some operations with the device here
        }
    }

  double dp = step;
  wb_position_sensor_enable(ps, TIME_STEP);
  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      wb_position_sensor_enable(sensors[i][j], TIME_STEP);
    }
  }

  double position_list[] = {0.01, 0.02 ,0.03 ,0.04, 0.05 ,0.06, 0.07, 0.08, 0.09 ,0.1};  

  int cur_loc = 9;
  bool is_increasing = false;

  while (wb_robot_step(TIME_STEP) != -1) {
    //wb_motor_set_position(muscle, p);
    if (cur_loc == 9){
        is_increasing = false;
    }
    else if (cur_loc == 0){
        is_increasing = true;
    }
    if (is_increasing){
        cur_loc += 1;
    }else{
        cur_loc -= 1;
    }
    for (int i = 0; i < 1; i++) {
        for (int j = 0; j < cols; j++) {
            wb_motor_set_position(devices[i][j], position_list[cur_loc]);
            const double pos = wb_position_sensor_get_value(sensors[i][j]);
            printf("Position: %f, j: %d\n", pos, j);
        }
    }

    /*
    wb_motor_set_position(devices[0][5], p);
    const double pos = wb_position_sensor_get_value(sensors[0][5]);
    printf("Position: %f, dp: %f, p: %f\n", pos, dp, p);
    if (pos <= 0.0)
      dp = -step;
    else if (pos >= max)
      dp = step;
    p = pos - dp;
    */
  };



   // Free the allocated memory
    for (int i = 0; i < rows; i++) {
        free(devices[i]); // Free each row of device pointers
    }
    free(devices); // Free the top-level array of row pointers

    for (int i = 0; i < rows; i++) {
        free(sensors[i]); // Free each row of device pointers
    }
    free(sensors); // Free the top-level array of row pointers

  wb_robot_cleanup();
   
  return 0;
}
