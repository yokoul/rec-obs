#!/usr/bin/env python3

import utils
import os
import sys
import time
import toml
import logging
import threading
from obswebsocket import obsws, requests
from concurrent.futures import ThreadPoolExecutor

# Load configuration from file
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, "obs-rec.conf")
def read_config():
    with open(config_file) as f:
        return toml.load(f)

config = read_config()

# Set up logging
utils.setup_logging(config)

# Set variables
try:
    pathName = sys.argv[2]
    fileName = sys.argv[3]
except:
    sys.exit(1)
actualtime = time.strftime("%H:%M:%S", time.localtime())
shortfileName = fileName[21:]

# Access recording settings
should_record = config["recording"]["should_record"]
should_stream = config["recording"]["should_stream"]
should_editrecpath = config["recording"]["should_editrecpath"]
should_editpresenterfilename = config["recording"]["should_editpresenterfilename"]
should_editpresentationfilename = config["recording"]["should_editpresentationfilename"]
should_editstream = config["recording"]["should_editstream"]
recording_path = config["recording"]["recording_path"]
stream_server = config["recording"]["stream_server"]
should_editpresenterstreamname = config["recording"]["should_editpresenterstreamname"]
should_editpresentationstreamname = config["recording"]["should_editpresentationstreamname"]
sequence = config["recording"]["sequence"]

# Access hosts and scenes
hosts = config["hosts"]
addresses = hosts["address"]
ports = hosts["port"]
passwords = hosts["password"]
scenes = hosts["scenes"]
sceneLanding = scenes["sceneLanding"]
sceneLive = scenes["sceneLive"]

# Define functions for different actions
def set_rec(ws, recording_path, fileName, index):
    if should_editrecpath[index] and should_editpresenterfilename[index]:
        logging.info("Setting recording path")
        ws.call(requests.SetRecordingFolder(recording_path + fileName))
        logging.info("Setting presenter file name")
        ws.call(requests.SetFilenameFormatting(f"{fileName}-presenter"))
    if should_editrecpath[index] and should_editpresentationfilename[index]:
        logging.info("Setting recording path")
        ws.call(requests.SetRecordingFolder(recording_path + fileName))
        logging.info("Setting presentation file name")
        ws.call(requests.SetFilenameFormatting(f"{fileName}-presentation"))

def set_stream(ws, stream_server, shortfileName, index):
    if should_editstream[index] and should_editpresenterstreamname[index]:
        logging.info("Setting stream file name")
        ws.call(requests.SetStreamSettings(type="rtmp_custom", settings={"server": f"{stream_server}/{shortfileName}-presenter-delivery"}, save=True))
    if should_editstream[index] and should_editpresentationstreamname[index]:
        logging.info("Setting stream file name")
        ws.call(requests.SetStreamSettings(type="rtmp_custom", settings={"server": f"{stream_server}/{shortfileName}-presentation-delivery"}, save=True))

def switch_to_landing_scene(ws, index):
    scene = sceneLanding[index]
    logging.info(f"Switching to scene '{scene}'")
    ws.call(requests.SetCurrentScene(scene))

def switch_to_live_scene(ws, index):
    scene = sceneLive[index]
    logging.info(f"Switching to scene '{scene}'")
    ws.call(requests.SetCurrentScene(scene))

def start_live(ws, index):
    if should_record[index]:
        logging.info("Starting recording")
        ws.call(requests.StartRecording())
    if should_stream[index]:
        logging.info("Live streaming")
        ws.call(requests.StartStreaming())

def stop_live(ws, index):
    if should_record[index]:
        logging.info("Stopping recording")
        ws.call(requests.StopRecording())
    if should_stream[index]:
        logging.info("Stopping live streaming")
        ws.call(requests.StopStreaming())
class WaitThread(threading.Thread):
    def __init__(self, duration, log_interval):
        super().__init__()
        self.duration = duration
        self.log_interval = log_interval
        self.stopped = False
    
    def run(self):
        logging.info(f"Waiting for recording duration ({self.duration} seconds)")
        start_time = time.monotonic()
        last_log_time = start_time
        remaining_time = self.duration
        while remaining_time > 0 and not self.stopped:
            time.sleep(1)
            elapsed_time = time.monotonic() - start_time
            remaining_time = self.duration - elapsed_time
            current_time = time.monotonic()
        if current_time - last_log_time >= self.log_interval:
            remaining_time = self.duration - elapsed_time
            logging.info(f"Remaining time: {remaining_time:.0f} seconds")
            last_log_time = current_time
        if not self.stopped:
            logging.info("Recording duration complete")
    
    def stop(self):
        self.stopped = True
    
    def update_duration(self, duration):
        self.duration = duration

def wait_for_duration(ws, index):
    config = read_config()
    duration = int(sys.argv[1]) + config["recording"]["extended_time"]
    log_interval = 5
    thread = WaitThread(duration, log_interval)
    thread.start()
    while thread.is_alive():
        time.sleep(0.5)
        config = read_config()
        if "extended_time" in config["recording"]:
            duration = int(sys.argv[1]) + config["recording"]["extended_time"]
            thread.update_duration(duration)
        elapsed_time = time.monotonic() - start_time
        remaining_time = duration - elapsed_time
        logging.info(f"Remaining time: {remaining_time:.0f} seconds")
    thread.stop()
    thread.join()

def perform_actions_on_obs(ws, actions, sequence, index):
    action_functions = {
        "sceneLanding": switch_to_landing_scene,
        "sceneLive": switch_to_live_scene,
        "startLive": start_live,
        "stopLive": stop_live,
        "wait1s": lambda ws, index: time.sleep(1),
        "wait2s": lambda ws, index: time.sleep(2),
        "wait5s": lambda ws, index: time.sleep(5),
        "wait10s": lambda ws, index: time.sleep(10),
        "waitDuration": wait_for_duration,
    }

    for action in actions:
        if action not in sequence:
            logging.warning(f"Action '{action}' is not a possible action. Skipping.")
            continue
        action_functions[action](ws, index)

# Connect to OBS instances
wss = []
for i, (address, port, password) in enumerate(zip(addresses, ports, passwords)):
    ws = obsws(address, port, password)
    try:
        ws.connect()
    except:
        logging.error(f"Failed to connect to OBS {i+1} ({address}:{port})")
        continue
    wss.append(ws)
    logging.info(f"Connected to OBS {i+1} ({address}:{port})")
    
for i, ws in enumerate(wss):
    set_rec(ws, recording_path, fileName, i)
    set_stream(ws, stream_server, shortfileName, i)

# Use ThreadPoolExecutor to run the actions on each OBS instance in parallel
with ThreadPoolExecutor(max_workers=len(addresses)) as executor:
    futures = []
    for i, ws in enumerate(wss):
        actions = sequence[:]
        future = executor.submit(perform_actions_on_obs, ws, actions, sequence, i)
        futures.append(future)
        #time.sleep(0.5)

    # Wait for all futures to complete
    for future in futures:
        future.result()
        #time.sleep(0.5)

# Disconnect from OBS instances
for ws in wss:
    ws.disconnect()

# Reset extended time
config["recording"]["extended_time"] = 0
with open(config_file, "w") as f:
    toml.dump(config, f)
