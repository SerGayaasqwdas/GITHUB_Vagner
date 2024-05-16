from dataclasses import dataclass, asdict
import logging
import json

loger = logging.getLogger(__name__)


def read_file_json(file_name):
    try:
        with open(file_name, 'r') as file:
            value = json.load(file)
        return value
    except Exception as e:
        loger.critical("Can't open or read file", exc_info=e)
        raise Exception(f'Not open or read file {file_name}')


@dataclass(frozen=True)
class DataText:
    MenuCommands: dict
    SSHCommands: dict
    SSHMessage: dict
    GeneralCommands: dict
    BDMessage: dict
    KeyboardsText: dict
    MonitoringMessage: dict
    RegexMessage: dict
    SettingsMessage: dict


tmp = read_file_json('data/text_aiogram_bot.json')
TEXT_BOT = DataText(tmp['commands_menu'], tmp['commands_ssh'], tmp['message_ssh'], tmp['general_commands'],
                    tmp['interaction_bd_message'], tmp['keyboards_text'], tmp['message_monitoring'],
                    tmp['regex_message'], tmp['settings_message'])
