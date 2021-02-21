# i3_smart_focus

more intuitive way to change window focus in i3wm

## how to use

1. Add redirect variable in i3 config file (NOTE: must be spelled exactly like this)
   ```bash
   set $i3redirect i3py_redirect
   ```
2. Modify focus commands
   ```bash
   bindsym $mod+Right exec $i3redirect focus right
   bindsym $mod+Left exec $i3redirect focus left
   bindsym $mod+Up exec $i3redirect focus up
   bindsym $mod+Down exec $i3redirect focus down
   ```
3. Execute the script (NOTE: '&' is necesary for the process to run detached in the background)
   ```bash
   exec_always --no-startup-id python /absolute/path/to/i3_smart_focus.py &
   ```
