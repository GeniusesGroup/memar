/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionnaireOtherRelation indicate the domain record data fields.
// TODO::: separate to some domains? product, Marketing, law, invoice, education, department, content, estate,
type QuestionnaireOtherRelation interface {
	QuestionnaireID() QuestionnaireUUID //
	DomainID() protocol.MediaTypeID     //
	// TODO::: primary key may not be a single field!
	RecordID() [16]byte // in above domain
	Type() QuestionnaireOtherRelation_Type
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type QuestionnaireOtherRelation_StorageServices interface {
	Save(dm QuestionnaireOtherRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID QuestionnaireUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID QuestionnaireUUID, vo protocol.VersionOffset) (dm QuestionnaireOtherRelation, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuestionnaireOtherRelation_Type uint8

const (
	QuestionnaireOtherRelation_Type_Unset QuestionnaireOtherRelation_Type = iota
	QuestionnaireOtherRelation_Type_Authorization
)
