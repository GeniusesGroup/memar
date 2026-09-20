/* For license and copyright information please see the LEGAL file in the code repository */

package settlement_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_SettlementUUID interface {
	SettlementUUID() UUID
}

type UUID record_p.UUID
