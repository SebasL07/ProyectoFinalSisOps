#!/bin/bash

# Function to kill a process by PID
kill_process() {
    # Check if PID is provided
    if [ -z "$1" ]; then
        echo "Error: Please provide a Process ID (PID)"
        echo "Usage: $0 <PID>"
        exit 1
    fi

    # Try to kill the process gracefully first
    echo "Attempting to terminate process with PID $1..."
    kill "$1"

    # Wait a few seconds to see if the process exits
    sleep 2

    # Check if the process was killed successfully
    if [ $? -eq 0 ]; then
        # Check if the process is still running
        if ps -p "$1" > /dev/null; then
            echo "Process $1 did not exit. Forcing termination..."
            # Force kill if the process doesn't respond
            kill -9 "$1"

            # Verify force kill
            if [ $? -eq 0 ]; then
                echo "Process $1 has been forcefully terminated."
            else
                echo "Failed to terminate process $1"
            fi
        else
            echo "Process $1 has been successfully terminated."
        fi
    else
        echo "Failed to send termination signal to process $1"
        exit 1
    fi
}

# Call the function with the provided argument
kill_process "$1"