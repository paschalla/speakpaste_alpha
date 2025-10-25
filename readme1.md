
# Speakpaste - A Hotkey-Activated Dictation Tool

Speakpaste is a simple, efficient terminal application that allows you to record short audio clips, transcribe them with high accuracy, and automatically copy the resulting text to your clipboard.

## Features

*   **High-Quality Transcription:** Powered by `faster-whisper` for excellent punctuation, capitalization, and accuracy.
*   **Push-to-Talk:** Press a key shortcut to start recording, and the app automatically stops when you go silent.
*   **Clipboard Integration:** Transcribed text is instantly available on your system clipboard for pasting.
*   **Terminal UI:** A clean, lightweight `Textual`-based interface provides a running log of your transcriptions.
*   **Efficient:** Runs effectively on CPU with minimal resource usage.

## Setup Instructions

These instructions are for Kubuntu / KDE Plasma and other Debian-based systems.

### 1. System Prerequisites

First, you need to install a couple of system-level packages: Python's virtual environment tool and the `xclip` utility for clipboard access.

```bash
sudo apt update
sudo apt install python3-venv xclip -y
```

### 2. Application Installation

Follow these steps to set up the application and its dependencies.

```bash
# 1. Clone or download the project files into a directory.
# For example:
# git clone https://github.com/paschalla/speakpaste/
# cd speakpaste

# 2. Create a Python virtual environment in the project directory.
python3 -m venv venv

# 3. Activate the virtual environment.
source venv/bin/activate

# 4. Install the required Python packages from the frozen requirements file.
pip install -r requirements-frozen.txt
```

### 3. Usage

You can run the application directly from your terminal to use it in a focused window.

```bash
# Make sure your virtual environment is activated first!
# (You should see '(venv)' at the start of your terminal prompt)
python main_app.py
```
Inside the app, press **SPACE** to record and **Ctrl+Q** to quit.

## Creating a System-Wide Hotkey (KDE Plasma - Modern UI)

The primary goal of this tool is to be available anywhere in the OS. Follow these steps to bind it to a global hotkey.

1.  Open **System Settings**.
2.  Navigate to the **Shortcuts** section.
3.  Click the **+ Add New** button.
4.  From the menu that appears, select **Command**.
5.  A new entry will be created. Give it a descriptive name (e.g., "Speakpaste").
6.  Configure the new entry:
    *   **Trigger Tab:** Click the button (it might say "None") and press the key combination you want to use. A good choice that avoids conflicts is `Meta+Shift+S` (Meta is the Windows/Super key).
    *   **Action Tab:** This is the most important step. In the "Command/URL" field, you must provide the **absolute paths** to the Python executable inside your virtual environment and to the `main_app.py` script.

    The command will look like this:
    ```
    /home/andy/speakpaste/venv/bin/python /home/andy/speakpaste/main_app.py
    ```
    **You must replace `/home/andy/speakpaste/` with the actual, full path to your project directory.** You can get the full path by navigating to your project folder in the terminal and running the `pwd` command.

7.  Click the **Apply** button in the bottom-right corner of the System Settings window.

Now, whenever you press your chosen hotkey from any application, the Speakpaste window will appear, ready to record.

## Configuration

You can tune the application's behavior by editing the following files:

*   `recorder.py`: Change `SILENCE_DURATION_S` to adjust how many seconds of silence are needed to stop a recording.
*   `transcriber.py`: Change `MODEL_SIZE` to use a different model (e.g., "tiny", "base", "medium"). Larger models are more accurate but slower and use more memory. The base model seems to be effective, but adjust to your needs and system resources. 
```
