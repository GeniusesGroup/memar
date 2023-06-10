/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TODO::: Need this domain??

// LabelOtherRelation indicate the domain record data fields.
type LabelOtherRelation interface {
	LabelID() LabelUUID             //
	DomainID() protocol.MediaTypeID //
	// TODO::: primary key may not be a single field!
	RecordID() protocol.UUID        // in above domain
	Status()
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
