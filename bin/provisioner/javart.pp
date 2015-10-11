
import 'system-update.pp'

class javart {
  package { "openjdk-6-jre-headless":
    ensure  => present,
    require => Class["system-update"],
  }
}

include javart

