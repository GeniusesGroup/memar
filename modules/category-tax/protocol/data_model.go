/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"libgo/protocol"

	cp "org/modules/category/protocol"
	sp "org/modules/society/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Tax Labels
// Setting tax labels allows you to perform the following actions:
// Define up to two tax labels and associate each of them with a specific tax rate
// Associate multiple tax rates with the same tax labels
// Associate a blank tax label with tax exempt items (considered non-value-added tax (VAT))
type DataModel interface {
	CategoryID() cp.CategoryUUID    //
	SocietyID() sp.SocietyUUID      //
	VAT() protocol.PerMyriad        // VAT as Value-Added-Tax is bad name for a robbery
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
