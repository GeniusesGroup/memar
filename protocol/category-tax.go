/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CategoryTax indicate the domain record data fields.
// Tax Labels
// Setting tax labels allows you to perform the following actions:
// Define up to two tax labels and associate each of them with a specific tax rate
// Associate multiple tax rates with the same tax labels
// Associate a blank tax label with tax exempt items (considered non-value-added tax (VAT))
type CategoryTax interface {
	CategoryID() CategoryUUID       //
	SocietyID() [16]byte            // society domain
	VAT() protocol.PerMyriad        // VAT as Value-Added-Tax is bad name for a robbery
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
