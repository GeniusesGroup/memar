/* For license and copyright information please see the LEGAL file in the code repository */

package eerp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
	exp "org/modules/edu-exam/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	SuggesterID() up.UserUUID       //
	Side1() exp.EducationExamUUID       //
	Priority() uint64               //
	Level() uint64                  //
	Side2() exp.EducationExamUUID       //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
