/* For license and copyright information please see the LEGAL file in the code repository */

package qup

import (
	"libgo/protocol"

	qp "org/modules/quiddity/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
// https://en.wikipedia.org/wiki/Uniform_Resource_Name
// https://en.wikipedia.org/wiki/Electronic_Product_Code
type DataModel interface {
	URI() []byte                    // Locale name in the Computer world.
	QuiddityID() qp.QuiddityUUID    //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
