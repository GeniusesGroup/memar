/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type ContentTag interface {
	Tag() string         //
	ContentID() [16]byte // content domain
	Time() protocol.Time // save time
}

type ContentTag_StorageServices interface {
}
