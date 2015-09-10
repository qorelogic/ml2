# Set a custom session root path. Default is `$HOME`.
# Must be called before `initialize_session`.
#session_root "~/Projects/rd2"

# Create session with specified name if it does not already exist. If no
# argument is given, session name will be based on layout file name.
if initialize_session "liquid"; then

  # Create a new window inline within session layout definition.
  #new_window "misc"

  # Load a defined window layout.
  load_window "qlm"
  load_window "babysit"
  #load_window "h2o"
  load_window "equity"
  load_window "datafeeds"

  load_window "ml.live"
  load_window "ml.dev"

  load_window "procsys"

  #load_window "mx-layouts"
  #load_window "qorelogic"
  #load_window "rapidminer"

  #load_window "ipn"
  #load_window "oandapy"


  # Select the default active window on session creation.
  select_window 1

fi

# Finalize session creation and switch/attach to it.
finalize_and_go_to_session

