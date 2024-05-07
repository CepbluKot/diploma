from servo_realization.protocol_interface.CanOpen301 import CanOpen301, ReceivedMessage


# params tab 1

def on_read_speed_gui_call(received_message: ReceivedMessage):
    widget = general_params_repo.get(received_message.servo_id, 'speed')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_accel_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'accel')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_mode_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'mode')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_pos_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'position')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_target_pos_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'target position')
    if widget:
        widget.config(text=received_message.decoded_data)
        
def on_read_error_check_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'error code')
    if widget:
        widget.config(text=received_message.decoded_data)
        
def on_voltage_check_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'voltage')
    if widget:
        widget.config(text=received_message.decoded_data/327)
        
def on_temperature_check_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'temperature')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_current_check_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'current')
    if widget:
        widget.config(text=received_message.decoded_data)


# params tab 2

def on_read_modbus_permission_gui_call(received_message: ReceivedMessage):
    widget = general_params_repo.get(received_message.servo_id, 'modbus_permission')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_driver_output_permission_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'driver_output_permission')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_weak_magnet_angle_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'weak_magnet_angle')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_speed_loop_scale_coefficient_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'speed_loop_scale_coefficient')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_speed_loop_integration_time_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'speed_loop_integration_time')
    if widget:
        widget.config(text=received_message.decoded_data)
        
def on_read_position_loop_scale_coefficient_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'position_loop_scale_coefficient')
    if widget:
        widget.config(text=received_message.decoded_data)

# params tab 3

def on_read_speed_control_gui_call(received_message: ReceivedMessage):
    widget = general_params_repo.get(received_message.servo_id, 'speed_control')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_polarity_dir_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'polarity_dir')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_electronic_gear_molecules_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'electronic_gear_molecules')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_transfer_electronic_denominator_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'transfer_electronic_denominator')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_incremental_position_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'incremental_position')
    if widget:
        widget.config(text=received_message.decoded_data)
        
def on_read_system_PWM_output_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'system_PWM_output')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_save_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'save')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_address_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'address')
    if widget:
        widget.config(text=received_message.decoded_data)

# params tab 4

def on_read_stationary_max_power_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'stationary_max_power')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_target_location_cache_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'target_location_cache')
    if widget:
        widget.config(text=received_message.decoded_data)

def on_read_can_connection_sync_speed_word_gui_call(received_message: ReceivedMessage):
    widget =general_params_repo.get(received_message.servo_id, 'can_connection_sync_speed_word')
    if widget:
        widget.config(text=received_message.decoded_data)


