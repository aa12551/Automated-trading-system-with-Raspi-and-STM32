#include "ILI9341_Touch.h"

uint8_t ili9341_touch_pressed()
{
  if (GPIO_PIN_RESET == HAL_GPIO_ReadPin(LCD_TOUCH_IRQ_PORT, LCD_TOUCH_IRQ_PIN))
    { return itpPressed; }
  else
    { return itpNotPressed; }
}

void ili9341_coordinate_transform(uint32_t * x,uint32_t * y,uint8_t rotation)
{
	if(SCREEN_VERTICAL_1 == rotation)
	{
		uint32_t x_temp = *x;
		uint32_t y_temp = *y;
		*x = (320 > (y_temp-3000)/80) ? 320-(y_temp-3000)/80 :320;
		*y = (240 > (x_temp-3000)/100) ? (x_temp-3000)/100 : 240;
	}

}
 ili9341_touch_pressed_t ili9341_touch_coordinate(uint16_t *x_pos, uint16_t *y_pos,uint8_t rotation)
 {

   // XPT2046 8-bit command patterns
   static uint8_t x_cmd[]  = { 0xD3 };
   static uint8_t y_cmd[]  = { 0x93 };
   static uint8_t sleep[]  = { 0x00 };

   uint32_t x_avg = 0U;
   uint32_t y_avg = 0U;
   uint16_t req_samples = 8U;
   uint16_t sample = req_samples;
   uint16_t num_samples = 0U;
   // change SPI clock to 2MHz, max rate supported by XPT2046
   // TODO: based on STM32G4, which is clocked at 170MHz. support other chips.
   MODIFY_REG(hspi1.Instance->CR1, SPI_CR1_BR, SPI_BAUDRATEPRESCALER_128);

   HAL_GPIO_WritePin(LCD_TOUCH_CS_PORT, LCD_TOUCH_CS_PIN, GPIO_PIN_RESET);

   while ((itpPressed == ili9341_touch_pressed()) && (sample--)) {

     uint8_t x_raw[2];
     uint8_t y_raw[2];

     HAL_SPI_Transmit(HSPI_INSTANCE, (uint8_t*)x_cmd, sizeof(x_cmd), HAL_MAX_DELAY);
     HAL_SPI_TransmitReceive(HSPI_INSTANCE, (uint8_t*)x_cmd, x_raw, sizeof(x_raw), HAL_MAX_DELAY);

     HAL_SPI_Transmit(HSPI_INSTANCE, (uint8_t*)y_cmd, sizeof(y_cmd), HAL_MAX_DELAY);
     HAL_SPI_TransmitReceive(HSPI_INSTANCE, (uint8_t*)y_cmd, y_raw, sizeof(y_raw), HAL_MAX_DELAY);

     x_avg += __LEu16(x_raw) >> 3;
     y_avg += __LEu16(y_raw) >> 3;

     ++num_samples;
   }
   HAL_SPI_Transmit(HSPI_INSTANCE, (uint8_t*)sleep, sizeof(sleep), HAL_MAX_DELAY);

   HAL_GPIO_WritePin(LCD_TOUCH_CS_PORT, LCD_TOUCH_CS_PIN, GPIO_PIN_SET);

   // restore SPI clock to maximum for TFT
   // TODO: based on STM32G4, which is clocked at 170MHz. support other chips.
   MODIFY_REG(hspi1.Instance->CR1, SPI_CR1_BR, SPI_BAUDRATEPRESCALER_2);
   if (num_samples < req_samples)
   {
	   *x_pos = 0;
	   *y_pos = 0;
	   return itpNotPressed;
   }


   ili9341_coordinate_transform(&x_avg,&y_avg,rotation);
   *x_pos = x_avg;
   *y_pos = y_avg;

   return itpPressed;
 }
