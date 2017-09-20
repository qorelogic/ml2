
class docker {
	package { "docker":
		ensure  => present,
		require => Class["system-update"],
	}
	package { "docker.io":
		ensure  => present,
		require => Class["system-update"],
	}
}

import 'system-update.pp'
include docker
