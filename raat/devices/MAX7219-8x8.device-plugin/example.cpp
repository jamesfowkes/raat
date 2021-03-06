#include "raat.hpp"

#include "MAX7219.hpp"
#include "MAX7219-8x8.hpp"

#include "raat-oneshot-timer.hpp"
#include "raat-oneshot-task.hpp"
#include "raat-task.hpp"

static MAX7219_8x8 * sp_max7219_8x8;

static const uint8_t NO_CELL = 0xFF;

static uint8_t s_row = 0;
static uint8_t s_col = 0;

void row_column_task_fn(RAATTask& this_task, void * pData)
{
    (void)this_task; (void)pData;

    if (s_row < 8)
    {
        sp_max7219_8x8->set(s_row, s_col, true);
    }
    else
    {
        sp_max7219_8x8->clear_all();
        s_col = 0xFF;
        s_row = 0xFF;
    }

    sp_max7219_8x8->update();

    incrementwithrollover(s_col, 15);
    if (s_col == 0)
    {
        incrementwithrollover(s_row, 8);
    }
}
static RAATTask s_row_column_task(100, row_column_task_fn, NULL);

void raat_custom_setup(const raat_devices_struct& devices, const raat_params_struct& params)
{
    (void)devices; (void)params;
    sp_max7219_8x8 = devices.pMAX7219_Example;
    sp_max7219_8x8->set_shutdown(false);
    sp_max7219_8x8->set_intensity(5);
    sp_max7219_8x8->set_test(false);
    sp_max7219_8x8->clear_all();
}

void raat_custom_loop(const raat_devices_struct& devices, const raat_params_struct& params)
{
    (void)devices; (void)params;
    s_row_column_task.run();
}

