/* For license and copyright information please see the LEGAL file in the code repository */

package is_p

import (
	event_p "memar/event/protocol"
)

type SS_EventTarget event_p.EventTarget[SS_EventTarget_Event, SS_EventTarget_Options]

type SS_EventTarget_Event interface {
	DataModel
	event_p.Event
}

type SS_EventTarget_Options interface {
}
