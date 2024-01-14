/* For license and copyright information please see the LEGAL file in the code repository */

package ltrtp

import (
	ltp "org/modules/language-text/protocol"
)

type BS_CitationsNumbers_Request interface {
	TextID() ltp.TextUUID
}

type BS_CitationsNumbers_Response interface {
	BackLinksNumbers() uint64 // total citations numbers
}
