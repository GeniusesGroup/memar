/* For license and copyright information please see the LEGAL file in the code repository */

package ekusp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
	ekup "org/modules/edu-knowledge_unit/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID                              //
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID //
	GivenScoreID() up.UserUUID                        //
	Duration() protocol.Duration                      // time duration to learn
	Score() uint64                                    //
	SaveTime() protocol.Time                          //
	RequestID() urp.UserRequestUUID                   //
}
