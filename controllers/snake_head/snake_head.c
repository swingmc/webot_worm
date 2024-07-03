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

#include <math.h>
#include <stdio.h>
#include <webots/robot.h>
#include <webots/distance_sensor.h>
#include <webots/motor.h>
#include <webots/keyboard.h>


#define TIME_STEP 64

int main(int argc, char **argv) {
  // 创建机器人实例
  wb_robot_init();

  WbDeviceTag ds[2];
  char dsNames[2][10] = {"ds_right", "ds_left"};
  for (int i = 0; i < 2; i++) {
    ds[i] = wb_robot_get_device(dsNames[i]);
    wb_distance_sensor_enable(ds[i], TIME_STEP);
  }

  // 初始化电机
  WbDeviceTag wheels[4];
  char wheels_names[4][8] = {"wheel1", "wheel2", "wheel3", "wheel4"};
  for (int i = 0; i < 4; i++) {
    wheels[i] = wb_robot_get_device(wheels_names[i]);
    wb_motor_set_position(wheels[i], INFINITY);
    wb_motor_set_velocity(wheels[i], 0.0);
  }
  printf("init success ...\n");

  WbDeviceTag kb = wb_robot_get_device("keyboard");
  wb_keyboard_enable(TIME_STEP);

  double leftSpeed = 0.0;
  double rightSpeed = 0.0;

  // 主循环
  while (wb_robot_step(TIME_STEP) != -1) {
    printf("loop ...\n");
    int key = wb_keyboard_get_key();
    printf("key: %d\n", key);
    switch (key) {
      case 315: // 上
        leftSpeed = 3.0;
        rightSpeed = 3.0;
        break;
      case 317: // 下
        leftSpeed = -3.0;
        rightSpeed = -3.0;
        break;
      case 314: // 左
        leftSpeed = -3.0;
        rightSpeed = 3.0;
        break;
      case 316: // 右
        leftSpeed = 3.0;
        rightSpeed = -3.0;
        break;
      default:
        leftSpeed = 0.0;
        rightSpeed = 0.0;
        break;
    }

    printf("Right Sensor Value: %f  Left Sensor Value: %f\n", wb_distance_sensor_get_value(ds[0]), wb_distance_sensor_get_value(ds[1]));

    wb_motor_set_velocity(wheels[0], leftSpeed);
    wb_motor_set_velocity(wheels[1], rightSpeed);
    wb_motor_set_velocity(wheels[2], leftSpeed);
    wb_motor_set_velocity(wheels[3], rightSpeed);
  }

  // 清理代码
  wb_robot_cleanup();
  return 0;
}