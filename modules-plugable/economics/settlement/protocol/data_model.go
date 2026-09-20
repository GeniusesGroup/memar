/* For license and copyright information please see the LEGAL file in the code repository */

package settlement_p

import (
	event_p "memar/process/event/protocol"
)

type DataModel interface {
	Field_SettlementUUID

	event_p.Event
}
