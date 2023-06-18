/* For license and copyright information please see the LEGAL file in the code repository */

package cop

import (
	"libgo/protocol"

	op "org/modules/object/protocol"
	cp "org/modules/comment/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Object can be any such as image, video, voice, ...
type DataModel interface {
	CommentID() cp.CommentUUID      //
	ObjectID() op.ObjectUUID        //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
