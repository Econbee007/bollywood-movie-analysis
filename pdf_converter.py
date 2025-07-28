import subprocess
import os

# Path to Chrome (adjust if needed)
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# Alternate for 32-bit systems:
# chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Input and output file paths
input_html = os.path.abspath("final_report.html")
output_pdf = os.path.abspath("final_report.pdf")

# Convert space to %20 for file URI
file_url = "file:///" + input_html.replace("\\", "/").replace(" ", "%20")

# Command to run
command = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={output_pdf}",
    file_url
]

# Run the command
try:
    subprocess.run(command, check=True)
    print(f"✅ PDF created at: {output_pdf}")
except subprocess.CalledProcessError as e:
    print("❌ Chrome failed to create PDF:", e)
except FileNotFoundError:
    print("❌ Chrome executable not found. Check the chrome_path.")
