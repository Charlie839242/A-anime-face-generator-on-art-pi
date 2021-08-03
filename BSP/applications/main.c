/*
 * Copyright (c) 2006-2020, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * 2020-09-02     RT-Thread    first version
 */

#include <rtthread.h>
#include <rtdevice.h>
#include "drv_common.h"
#include "drv_spi_ili9488.h"  // spi lcd driver
#include <lcd_spi_port.h>  // lcd ports
#include <logo.h>
#include <rt_ai_network_model.h>
#include <rt_ai.h>
#include <backend_cubeai.h>

#define PIN_KEY    GET_PIN(H, 4)  // 按键

struct rt_event ov2640_event;

int main(void)
{
    /* logo 1s showing */
    lcd_show_image(0, 0, 320, 240, LOGO);
    lcd_show_string(90, 140, 16, "Hello RT-Thread!");
    lcd_show_string(90, 156, 16, "Demo: gc0328c & LCD");
    rt_thread_mdelay(1000);

    rt_kprintf("a\n");

    // AI Part Start
    /* ai:获取模型句柄model*/
    rt_ai_t model = NULL;
    model = rt_ai_find(RT_AI_NETWORK_MODEL_NAME);
    if(!model) {rt_kprintf("ai find err\n"); return -1;}

    /* ai:为模型分配运行空间 */
    rt_uint8_t *work_buf = rt_malloc(RT_AI_NETWORK_WORK_BUFFER_BYTES);
    if(!work_buf) {rt_kprintf("malloc err\n");return -1;}

    /* ai:为模型输出分配储存空间 */
    rt_uint8_t *_out = rt_malloc(RT_AI_NETWORK_OUT_1_SIZE_BYTES);
    if(!_out) {rt_kprintf("malloc err\n"); return -1;}

    /* ai:为模型输入分配相应空间 */
    rt_uint8_t *input_buf       = rt_malloc(RT_AI_NETWORK_IN_1_SIZE_BYTES);
    if(!input_buf) {rt_kprintf("malloc err\n"); return -1;}

    /* ai:初始化并配置ai模型的输入输出空间 */
    if(rt_ai_init(model,work_buf) != 0){rt_kprintf("ai init err\n"); return -1;}
    rt_ai_config(model,CFG_INPUT_0_ADDR,input_buf);
    rt_ai_config(model,CFG_OUTPUT_0_ADDR,_out);
    // AI Part Done

    rt_kprintf("c");

    while(1)
    {
        while(rt_pin_read(PIN_KEY) == PIN_HIGH);

        //// 随机配置模型输入
        //for(int i = 0;i<100;i++)
        //    input_buf[i] = (random()%255);
        //
        //运行模型
        //rt_kprintf("start\n");
        //rt_ai_run(model, NULL, NULL);
        //rt_kprintf("end\n");

        //lcd_show_image(0, 0,48,48, _out);
    }
    return RT_EOK;
}

#include "stm32h7xx.h"
static int vtor_config(void)
{
    /* Vector Table Relocation in Internal QSPI_FLASH */
    SCB->VTOR = QSPI_BASE;
    return 0;
}
INIT_BOARD_EXPORT(vtor_config);


