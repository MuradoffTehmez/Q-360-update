import os
import shutil

# 1. Clean local logs folder
logs_dir = 'logs'
if os.path.exists(logs_dir):
    for filename in os.listdir(logs_dir):
        file_path = os.path.join(logs_dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.log'):
            os.remove(file_path)
            print(f"Deleted {filename}")

# Create nginx log folder just in case
os.makedirs('logs/nginx', exist_ok=True)

# 2. Update docker-compose.yml to bind mount logs
dc_path = 'docker-compose.yml'
with open(dc_path, 'r', encoding='utf-8') as f:
    dc = f.read()

dc = dc.replace('- logs_volume:/app/logs', '- ./logs:/app/logs')
dc = dc.replace('- logs_volume:/var/log/nginx', '- ./logs/nginx:/var/log/nginx')
with open(dc_path, 'w', encoding='utf-8') as f:
    f.write(dc)

# 3. Update settings.py to have a separate warning.log
settings_path = 'config/settings.py'
with open(settings_path, 'r', encoding='utf-8') as f:
    settings = f.read()

# Check if warning_file is already there
if "'warning_file':" not in settings:
    warning_handler = """
        # Warning log - separate file for warnings
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'warning.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
"""
    # Insert it right before error_file
    settings = settings.replace("'error_file': {", warning_handler.lstrip() + "        'error_file': {")
    
    # Also add it to the root logger or a specific logger
    # Wait, let's see how root logger is configured.
    if "'handlers': ['console', 'file', 'error_file']" in settings:
        settings = settings.replace("'handlers': ['console', 'file', 'error_file']", "'handlers': ['console', 'file', 'error_file', 'warning_file']")
    
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(settings)

print("Logs cleaned and configured for realtime host binding.")
