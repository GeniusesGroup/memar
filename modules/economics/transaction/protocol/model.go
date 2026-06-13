/* For license and copyright information please see the LEGAL file in the code repository */

package transaction_p

import (
	event_p "memar/process/event/protocol"

	thing_p "org/modules/identity/thing/protocol"
)

type Model interface {
	thing_p.Model

	event_p.Target[DataModel]
}
