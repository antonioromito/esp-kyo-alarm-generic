import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import globals, uart
from esphome.const import CONF_ID

DEPENDENCIES = ["uart", "globals"]
AUTO_LOAD = ["api"]

CONF_ARMED_HOME_ID = "armed_home_id"
CONF_ARMED_AWAY_ID = "armed_away_id"

# C++ class in kyo_alarm.h also inherits api::CustomAPIDevice
KyoAlarmComponent = cg.global_ns.class_(
    "KyoAlarmComponent",
    cg.PollingComponent,
    uart.UARTDevice,
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(KyoAlarmComponent),
            cv.Required(CONF_ARMED_HOME_ID): cv.use_id(globals.GlobalsComponent),
            cv.Required(CONF_ARMED_AWAY_ID): cv.use_id(globals.GlobalsComponent),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(cv.polling_component_schema("2s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    armed_home = await cg.get_variable(config[CONF_ARMED_HOME_ID])
    armed_away = await cg.get_variable(config[CONF_ARMED_AWAY_ID])
    cg.add(var.set_partition_globals(armed_home, armed_away))
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
