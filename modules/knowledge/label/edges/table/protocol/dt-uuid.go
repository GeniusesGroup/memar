/* For license and copyright information please see the LEGAL file in the code repository */

package table_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_TableID interface {
	TableID() UUID
}

type UUID record_p.UUID
