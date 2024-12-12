import subprocess
import shutil

# Get the models
print("Getting the models...")
subprocess.run([
    'python3', 
    'src/scripts/generate_model_set.py', 
    '--model_set', 'chocolate',
])

# Run Ansor using different trial counts

trail_counts = ['2500', '5000', '10000']
for num_trials in trail_counts:
    print(f"Running Ansor with {num_trials} trials...")
    subprocess.run([
        'python3', 
        'src/scripts/autoschedule_models.py', 
        '--model_path', 'models/chocolate',
        '--ntrials', num_trials,
        '--device_name', 'my_gpu',
        '--output_dir', f'data_{num_trials}/raw/chocolate',
    ])

    print(f"Copying data...")
    # Copy data to compare TT to TT + Droplet
    shutil.copytree(f'data_{num_trials}/raw/chocolate', f'data_{num_trials}_droplet/raw/chocolate')

    # Also copy the models for TT and TT + Droplet because we edit them later
    shutil.copytree(f'models/chocolate', f'models_{num_trials}/chocolate')
    shutil.copytree(f'models/chocolate', f'models_{num_trials}_droplet/chocolate')

    # Run Droplet on copied data
    print(f"Running droplet search...")
    subprocess.run([
        'python3', 
        'src/scripts/autoschedule_models.py', 
        '--model_path', f'models_{num_trials}_droplet/chocolate',
        '--device_name', 'my_gpu',
        '--output_dir', f'data_{num_trials}_droplet/raw/chocolate',
        '--droplet_search',
    ])

    # Extract the top performing auto-schedules
    print(f"Extracting auto-schedulers...")
    subprocess.run([
        'python3', 
        'src/scripts/distil_logfiles.py', 
        '--log_file_dir', f'data_{num_trials}/raw/chocolate',
    ])

    subprocess.run([
        'python3', 
        'src/scripts/distil_logfiles.py', 
        '--log_file_dir', f'data_{num_trials}_droplet/raw/chocolate',
    ])

    # Save relevant task
    print(f"Saving relevent tasks...")
    subprocess.run([
        'python3', 
        'src/scripts/generate_task_info.py', 
        '--network_dir', f'models_{num_trials}/chocolate',
        '--device_name', 'my_gpu',
    ])

    subprocess.run([
        'python3', 
        'src/scripts/generate_task_info.py', 
        '--network_dir', f'models_{num_trials}_droplet/chocolate',
        '--device_name', 'my_gpu',
    ])

    # split logfiles into individual workloads
    print(f"Splitting log files...")
    subprocess.run([
        'python3', 
        'src/scripts/split_logfiles.py', 
        '--log_file_dir', f'data_{num_trials}/raw/chocolate',
        '--network_dir', f'models_{num_trials}/chocolate',
        '--output_dir', f'data_{num_trials}/processed/split_logs/chocolate',
    ])

    subprocess.run([
        'python3', 
        'src/scripts/split_logfiles.py', 
        '--log_file_dir', f'data_{num_trials}_droplet/raw/chocolate',
        '--network_dir', f'models_{num_trials}_droplet/chocolate',
        '--output_dir', f'data_{num_trials}_droplet/processed/split_logs/chocolate',
    ])

    # run TT with all of our models
    print(f"Running TT...")
    subprocess.run([
        'python3', 
        'src/scripts/tt_multi_models_pact.py', 
        '--split_log_file_dir', f'data_{num_trials}/processed/split_logs/chocolate/ ',
        '--model', f'models_{num_trials}/chocolate',
        '--device_name', 'my_gpu',
    ])

    subprocess.run([
        'python3', 
        'src/scripts/tt_multi_models_pact.py', 
        '--split_log_file_dir', f'data_{num_trials}_droplet/processed/split_logs/chocolate/ ',
        '--model', f'models_{num_trials}_droplet/chocolate',
        '--device_name', 'my_gpu',
    ])
