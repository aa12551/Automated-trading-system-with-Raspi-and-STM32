#ifndef ILI9341_TOUCH_H
#define ILI9341_TOUCH_H

#include "ILI9341_STM32_Driver.h"
#include "ILI9341_GFX.h"


#define __LEu16(addr)                                      \
    ( ( (((uint16_t)(*(((uint8_t *)(addr)) + 1)))      ) | \
        (((uint16_t)(*(((uint8_t *)(addr)) + 0))) << 8U) ) )
typedef struct
{
  union
  {
    uint16_t x;
    uint16_t width;
  };
  union
  {
    uint16_t y;
    uint16_t height;
  };
}
ili9341_two_dimension_t;

typedef enum
{
  itpNONE = -1,
  itpNotPressed, // = 0
  itpPressed,    // = 1
  itpCOUNT       // = 2
}
ili9341_touch_pressed_t;
#endif

uint8_t ili9341_touch_pressed();
ili9341_two_dimension_t ili9341_project_touch_coordinate(uint16_t x_pos, uint16_t y_pos);
ili9341_touch_pressed_t ili9341_touch_coordinate(uint16_t *x_pos, uint16_t *y_pos,uint8_t rotation);
