/* For license and copyright information please see the LEGAL file in the code repository */

package ekudp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	ekup "org/modules/edu-knowledge_unit/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID //
	Minimum() protocol.Duration                       // Minimum time duration to learn
	Expected() protocol.Duration                      // Expected time duration to learn
	Maximum() protocol.Duration                       // Maximum time duration to learn
	SaveTime() protocol.Time                          //
	RequestID() urp.UserRequestUUID                   //
}
