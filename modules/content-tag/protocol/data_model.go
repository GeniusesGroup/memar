/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"libgo/protocol"

	cp "org/modules/content/protocol"
)

type DataModel interface {
	Tag() string               //
	ContentID() cp.ContentUUID //
	SaveTime() protocol.Time   //
}

