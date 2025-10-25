import pyperclip
import sys

def copy_to_clipboard(text: str):
    """
    Copies the given text string to the system clipboard.

    Handles potential errors if the clipboard mechanism is not available.

    Args:
        text (str): The text to be copied.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        pyperclip.copy(text)
        print("Text successfully copied to clipboard.")
        return True
    except pyperclip.PyperclipException as e:
        print("Error: Could not copy text to clipboard.", file=sys.stderr)
        print("Please ensure 'xclip' is installed on your system (`sudo apt install xclip`).", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        return False

# This block allows for direct testing of the clipboard module.
if __name__ == "__main__":
    print("--- Testing Clipboard Module ---")
    
    test_string = "This is a test. If this text is in your clipboard, the module is working."
    
    print(f"Attempting to copy the following text:\n'{test_string}'")
    
    success = copy_to_clipboard(test_string)
    
    if success:
        print("\nTest successful. Please paste (Ctrl+V) into a text editor to verify.")
    else:
        print("\nTest failed.")