#!/bin/bash
# Runs the mouse button listener only while a display output is in use, for example
# only while the projector is on. When the output goes off, the listener is stopped and
# an open keyboard is closed.
#
#   examples/listener-while-display.sh CONNECTOR [on|off]
#
#   CONNECTOR   name of the output as the kernel calls it, e.g. HDMI-A-1 or DP-2.
#               Run the script without arguments to see the outputs of this machine.
#   on          (default) listen while that output is switched on
#   off         listen while that output is switched off. Useful when "movie mode" means
#               that the desk monitor is turned off and only the projector remains.
#
# The state comes from /sys/class/drm, so this works on any desktop. Start it with your
# session, e.g. from a systemd user unit, instead of wayland-osk-listener itself.
set -u

here="$(dirname "$(readlink -f "$0")")/.."
connector="${1:-}"
wanted="${2:-on}"

if [ -z "$connector" ]; then
	echo "Usage: $0 CONNECTOR [on|off]"
	echo "Outputs of this machine:"
	for path in /sys/class/drm/card*-*/enabled; do
		name="$(basename "$(dirname "$path")")"
		echo "  ${name#card*-}  ($(cat "$path"))"
	done
	exit 1
fi

state_file="$(ls /sys/class/drm/card*-"$connector"/enabled 2>/dev/null | head -n 1)"
if [ -z "$state_file" ]; then
	echo "$0: no output called '$connector'. Run without arguments to see the names." >&2
	exit 1
fi
case "$wanted" in
	on) wanted_state=enabled ;;
	off) wanted_state=disabled ;;
	*) echo "$0: second argument must be 'on' or 'off'" >&2; exit 1 ;;
esac

listener=""
stop_listener() {
	if [ -n "$listener" ]; then
		kill "$listener" 2>/dev/null
		wait "$listener" 2>/dev/null
		listener=""
		# Close the keyboard if it is still open.
		pidfile="${XDG_RUNTIME_DIR:-/tmp}/wayland-osk.pid"
		[ -f "$pidfile" ] && "$here/wayland-osk-toggle"
	fi
}
trap 'stop_listener; exit 0' INT TERM

while true; do
	if [ "$(cat "$state_file")" = "$wanted_state" ]; then
		if [ -z "$listener" ] || ! kill -0 "$listener" 2>/dev/null; then
			"$here/wayland-osk-listener" &
			listener=$!
		fi
	else
		stop_listener
	fi
	# In the background and waited for, so that a signal ends the script at once.
	sleep 3 &
	wait $!
done
