/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type CommentClassify interface {
	CommentID() CommentUUID     //
	Label() Comment_Classify    //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID //
}
type Comment_Classify uint32

const (
	Comment_Classify_Unset Comment_Classify = 0
	Comment_Classify_Toxic Comment_Classify = (1 << iota)
	Comment_Classify_Spam
	Comment_Classify_Sensitivity
	Comment_Classify_Confidential // if not set mean normal message
)
