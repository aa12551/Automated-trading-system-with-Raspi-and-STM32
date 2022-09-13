################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (9-2020-q2-update)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../FreeRTOS/portable/heap_4.c 

OBJS += \
./FreeRTOS/portable/heap_4.o 

C_DEPS += \
./FreeRTOS/portable/heap_4.d 


# Each subdirectory must supply rules for building sources it contributes
FreeRTOS/portable/%.o: ../FreeRTOS/portable/%.c FreeRTOS/portable/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F407xx -c -I../Core/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/s9400/STM32CubeIDE/workspace_1.8.0/Final_project/FreeRTOS/portable/ARM_CM4F" -I"C:/Users/s9400/STM32CubeIDE/workspace_1.8.0/Final_project/FreeRTOS/include" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-FreeRTOS-2f-portable

clean-FreeRTOS-2f-portable:
	-$(RM) ./FreeRTOS/portable/heap_4.d ./FreeRTOS/portable/heap_4.o

.PHONY: clean-FreeRTOS-2f-portable

