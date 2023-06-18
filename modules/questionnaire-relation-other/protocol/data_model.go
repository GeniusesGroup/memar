/* For license and copyright information please see the LEGAL file in the code repository */

package qrop

import (
	"libgo/protocol"

	qp "org/modules/questionnaire/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// TODO::: separate to some domains? product, Marketing, law, invoice, education, department, content, estate,
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID //
	DomainID() protocol.MediaTypeID        //
	// TODO::: primary key may not be a single field!
	RecordID() [16]byte // in above domain
	Type() Type
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Authorization
)
