/* For license and copyright information please see the LEGAL file in the code repository */

package ltp

import (
	qp "org/modules/quiddity/protocol"
)

// TextUUID can be same with any other UUID domains e.g. user, ...
// It MUST be unique ID in all domains.
// Wil be unique in all human languages
type TextUUID qp.QuiddityUUID
