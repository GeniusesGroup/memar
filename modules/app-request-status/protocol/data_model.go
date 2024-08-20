/* For license and copyright information please see the LEGAL file in the code repository */

package arsp

import (
	aap "org/modules/app-audit/protocol"
	sp "org/modules/storage/protocol"
)

// Store user requests as drafts for users to send later

// RequestID of this record use to prove how other records created as a chain to other records or standalone data.
// Prove how this record created in the chain of other records.
type DataModel interface {
	aap.AuditRequest
	Status() Status

	sp.Versioned
	sp.SaveTime
}
