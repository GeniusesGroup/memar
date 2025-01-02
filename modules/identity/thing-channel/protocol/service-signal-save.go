/* For license and copyright information please see the LEGAL file in the code repository */

package channel_p

import (
	event_p "memar/event/protocol"
)

// DataModel indicate the domain record data fields.
type Service_Signal_Save_Request interface {
	Field_ChannelID
	Field_SignalData
}

type Service_Signal_Save_EventTarget event_p.Target[Service_Signal_Save_Event]

type Service_Signal_Save_Event interface {
	Service_Signal_Save_Request
	event_p.Event
}
