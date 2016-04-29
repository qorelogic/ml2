# Set a custom session root path. Default is `$HOME`.
# Must be called before `initialize_session`.
#session_root "~/Projects/rd2"

# Create session with specified name if it does not already exist. If no
# argument is given, session name will be based on layout file name.
if initialize_session "feed"; then

  # Create a new window inline within session layout definition.
  #new_window "misc"

  # Load a defined window layout.
  #load_window "db"
  #load_window "mongo"
  #load_window "ml.dev"
  #load_window "zmq"
  load_window "zmq-simulator"
  load_window "feed"


  # Select the default active window on session creation
  #select_window 1

fi

# Finalize session creation and switch/attach to it.
finalize_and_go_to_session
