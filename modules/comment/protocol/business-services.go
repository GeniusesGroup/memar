/* For license and copyright information please see the LEGAL file in the code repository */

package cp

type (
	BS_Register_Request interface {
		CommentID() CommentUUID
		Type() Type
	}
)
