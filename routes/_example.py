# Copy this file, rename it to your GitHub username, and change both fields.
# The server picks up any file in here that defines PATH and handle().
# Files starting with _ are ignored, so this one never becomes an endpoint.

PATH = "/your-github-username"

def handle():
    return {
        "name": "Your Name",
        "team": "your-team",
        "wants": "one thing you want out of the six weeks",
    }
