/* For license and copyright information please see the LEGAL file in the code repository */

package cmp

import (
	"memar/protocol"
)

type SS_EventTarget protocol.EventTarget[SS_EventTarget_Event, SS_EventTarget_Options]

type SS_EventTarget_Event interface {
	DataModel
	protocol.Event
}

type SS_EventTarget_Options interface {
}
