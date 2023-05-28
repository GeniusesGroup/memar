/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// It can point to any domain records e.g. product, invoice, ...
// It can be use in other way than domain indicate e.g.
// - welcome message by group-associated domain data.
// - Map domain to share static or live location
// - PhotoUpdated
// - Call
// TODO::: prevent from flag set is on with other types like text

// CommentLogActivity indicate the domain record data fields.
type CommentLogActivity interface {
	CommentID() CommentUUID         //
	DomainID() protocol.MediaTypeID // use to detect comment GUI template
	// TODO::: primary key may not be a single field!
	RecordID() [16]byte             // in above domain
	RecordVersion() uint64          // VersionOffset
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentLogActivity_StorageServices interface {
	Save(cm CommentLogActivity) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (cm CommentLogActivity, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

