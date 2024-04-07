from AppKit import NSWorkspace
import time
import subprocess

def get_frontmost_app():
    applescript_command = """
    tell application "System Events"
        name of first application process whose frontmost is true
    end tell
    """
    frontmost_app = subprocess.run(["osascript", "-e", applescript_command], capture_output=True, text=True).stdout.strip()
    return frontmost_app

# Example usage:
print(get_frontmost_app())



# def track_screentime(app_bundle_id, update_interval=1):
#     test_screentime = 0  # Starting value for test screentime
#     while True:
#         test_screentime += update_interval  # Increment screentime by the update interval
#         time.sleep(update_interval)  # Wait for the specified update interval
#         yield test_screentime  # Yield the current test screentime
def track_screentime(app_bundle_id, update_interval=1):
    while True:
        active_app = get_frontmost_app()
        print("Detected active app:", active_app)
        time.sleep(update_interval)

    # print("Starting screentime tracking for:", app_bundle_id)
    # start_time = None
    # total_time = 0

    # while True:
    #     active_app = (
    #         NSWorkspace.sharedWorkspace().frontmostApplication().bundleIdentifier()
    #     )
    #     print(f"Detected active app: {active_app}")

    #     if active_app == app_bundle_id:
    #         print("MATCH - The app is active.")
    #         if start_time is None:
    #             # Start the timer when the app becomes active.
    #             start_time = time.time()
    #             print(f"Started timing: {start_time}")
    #     else:
    #         if start_time is not None:
    #             # Calculate the time the app was active and add it to total_time.
    #             total_time += time.time() - start_time
    #             # Reset start_time since the app is no longer active.
    #             start_time = None
    #             print(f"App is no longer active. Total screentime: {total_time}")

    #     # If the app is still active, update the total_time without resetting the start_time.
    #     if start_time is not None:
    #         # The application is currently active.
    #         current_active_time = time.time() - start_time
    #         current_total_time = total_time + current_active_time
    #         print(
    #             f"Currently active for: {current_active_time} seconds. Total screentime: {current_total_time}"
    #         )
    #     else:
    #         # The application is not currently active.
    #         current_total_time = total_time

    #     time.sleep(update_interval)
    #     yield current_total_time
