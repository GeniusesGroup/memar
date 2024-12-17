/* For license and copyright information please see the LEGAL file in the code repository */

package tcs_p

import (
	qsp "org/modules/identity/quiddity-status/protocol"
)

type Field_Status interface {
	Status() Status
}

type Status qsp.Quiddity_Status

const (
	// TODO::: below status can indicate in `thing-signal` subdomain as a state of a channel
	// e.g. off state need to change the led state on thing cover.
	Status_Off = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Offline
)
