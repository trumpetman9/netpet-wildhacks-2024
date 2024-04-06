'''from AppKit import NSWorkspace
import time

def track_screentime(app_bundle_id, update_interval=1):
    start_time = None
    total_time = 0

    while True:
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication().bundleIdentifier()
        if active_app == app_bundle_id:
            if start_time is None:
                start_time = time.time()
        else:
            if start_time is not None:
                total_time += time.time() - start_time
                start_time = None
        
        time.sleep(update_interval)
        yield total_time

'''