# Automated trading system with Raspi and STM32

## Description
  We implement program trading and trading strategies on low-power devices such as Raspi and stm32. We also use a LCD to show the current price and the target price.
  And developed a touch function to interact with users.
  

## Hardware
1. stm32f407
2. raspi 4b 
3. ili9341 2.8 inch touch LCD

## Hardware architecture
- The following picture is the actual status of this system.

![image](https://user-images.githubusercontent.com/94910883/189954992-e7d7dc5f-f16a-47da-a865-a8e1cd7bb37e.png)

- And The following picture is the block diagram of hardware and the protocol of communication between each hardware.

![image](https://user-images.githubusercontent.com/94910883/189955105-e7c7a6ec-6f14-4ba5-abea-2038f2430165.png)

## Software architecture
- We use `Python` to complete the program trading and use `linux` operating system in `Raspi`.
- we use `C` to complete all of the function we need in `STM32` and `ili9341` and use `FreeRTOS` to schedule our task.

## Individual Hardware function
- **Raspi**
  - Automatically determine the price to complete the automatic transaction.
  - Return the current price to stm32.
  - Using the strategy we want to calculate the target price.
  - Record the information about each transaction.
- **stm32f407**
  - Receive current price and send to screen.
  - Receive touch information from the screen.
  - Control screen related functions.
- **ili9341**
  - Show current price and target price
  - Send touch information to stm32f407

## System function
- You can set the target price by yourself or add a strategy to complete the automatic transaction.
- Can display current price and target price on LCD
- Can record transaction information
- If there is a problem with the execution of the program, you can use the touch panel to stop the transaction immediately

## Demonstration
- Send real-time data and display the calculated target price on the LCD screen : [Link1](https://drive.google.com/file/d/1-3HL2YoC4UqSyhcSqwcnd40Iw1uwBT8f/view?usp=share_link)
- Automatically place an order when the target price is reached (I use MAX exchange and set a price to let it place an order) : [Link2](https://drive.google.com/file/d/1BMO069nQI68K2mcI1surpjyYB-8r1zLU/view?usp=share_link)
- Stop the program in time when encountering a problem : [Link3](https://drive.google.com/file/d/1vHneD14yBO0fOCm6lheR3ivz3ThmFFqy/view?usp=share_link)
