import json
import os
import sys

config_path = os.path.join(os.path.dirname(__file__), "test_config.json")

with open(config_path, "r", encoding="utf-8") as f:
    config_data = json.load(f)

# Проверяем, включен ли конфиг
if not config_data.get("enabled", False):
    print("Тестовая конфигурация отключена (enabled = false).")
    sys.exit(0)  # или выбросьте исключение, или просто не используйте тестовые данные

active_config = config_data["active_config"]
test_configs = config_data["test_configs"]

# Экспортируем нужные шаги
test_config_step0 = test_configs[active_config]["step_0"]
test_config_step1 = test_configs[active_config]["step_1"]
test_config_step2 = test_configs[active_config]["step_2"]
test_config_step3 = test_configs[active_config]["step_3"]
test_config_step4 = test_configs[active_config]["step_4"]
test_config_step5 = test_configs[active_config]["step_5"]