/* For license and copyright information please see the LEGAL file in the code repository */

package tcs_p

import (
	event_p "memar/event/protocol"
)

type SS_EventTarget event_p.Target[SS_EventTarget_Event]

type SS_EventTarget_Event interface {
	DataModel
	event_p.Event
}
